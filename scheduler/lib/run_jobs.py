from datetime import date, datetime
import pandas as pd
import pytz
from scheduler.lib.freshdesk.create_ticket import create_fd_ticket
from scheduler.lib.helpers import replace_key_words
from scheduler.lib.logger import log_msg
from scheduler.models import Job, TaskRunHistory


def should_run_now(last_run_time, reoccurrence_periods):
    reoccurrence_days = reoccurrence_periods['day'].replace(' ', '')
    reoccurrence_months = reoccurrence_periods['month'].replace(' ', '')
    reoccurrence_days_of_week = reoccurrence_periods['day_of_week'].replace(' ', '')
    print(f'{reoccurrence_days}, {reoccurrence_months}, {reoccurrence_days_of_week}')

    reoccurrence_days = reoccurrence_days.split(',')
    reoccurrence_months = reoccurrence_months.split(',')
    reoccurrence_days_of_week = reoccurrence_days_of_week.split(',')

    if reoccurrence_days and '*' not in reoccurrence_days:
        try:
            reoccurrence_days = list(map(lambda x: int(x), reoccurrence_days))
        except Exception as e:
            log_msg(f'Error converting days to int: {e}')
            raise ValueError(e)

    if reoccurrence_months and '*' not in reoccurrence_months:
        try:
            reoccurrence_months = list(map(lambda x: int(x), reoccurrence_months))
        except Exception as e:
            log_msg(f'Error converting months to int: {e}')
            raise ValueError(e)

    if reoccurrence_days_of_week and '*' not in reoccurrence_days_of_week:
        try:
            reoccurrence_days_of_week = list(map(lambda x: int(x), reoccurrence_days_of_week))
        except Exception as e:
            log_msg(f'Error converting day of week to int: {e}')
            raise ValueError(e)

    last_run_day = 0
    last_run_month = 0
    last_run_day_of_week = 0

    if last_run_time:
        last_run_day = last_run_time.day
        last_run_month = last_run_time.month
        last_run_day_of_week = last_run_time.weekday() + 1  # Monday is 1, Sunday is 7

    now = date.today()
    now_day = now.day
    now_month = now.month
    now_day_of_week = now.weekday() + 1  # Monday is 1, Sunday is 7

    day_passes = any(now_day == day or day == '*'
                     for day in reoccurrence_days) or (len(reoccurrence_days) == 1
                                                       and reoccurrence_days[0] == 0)
    month_passes = any(now_month == month or month == '*'
                       for month in reoccurrence_months) or (len(reoccurrence_months) == 1
                                                             and reoccurrence_months[0] == 0)
    day_of_week_passes = any(now_day_of_week == day_of_week or day_of_week == '*'
                             for day_of_week in reoccurrence_days_of_week) or (len(reoccurrence_days_of_week) == 1
                                                                               and reoccurrence_days_of_week[0] == 0)

    last_run_passes = all([last_run_day != now_day,
                           last_run_month != now_month,
                           last_run_day_of_week != now_day_of_week])

    print(f'{day_passes=}')
    print(f'{month_passes=}')
    print(f'{day_of_week_passes=}')
    print(f'{last_run_passes=}')

    return all((day_passes, month_passes, day_of_week_passes, last_run_passes))


def run_job_tasks():
    try:
        log_msg('running job checks...')
        jobs = Job.objects.all()

        if not any(job.enabled for job in jobs):
            log_msg('No enabled jobs found...')
            return

        all_run_history_df = pd.DataFrame(TaskRunHistory.objects.all().values())
        utc = pytz.UTC

        for job in jobs:
            log_msg(f'Checking job {job} for tasks to run..')

            #  if datetime.now() > job.start_date.replace(tzinfo=pytz.UTC):
            #      continue

            for task in job.task_group.tasks.all():
                if len(all_run_history_df):
                    task_run_history_df = all_run_history_df[(all_run_history_df.job_name == job.name) &
                                                             (all_run_history_df.task_subject == task.subject)]
                    task_run_history_df = task_run_history_df.sort_values('run_date', ascending=False)

                    if len(task_run_history_df):
                        last_run_time = task_run_history_df.iloc[0].run_date
                    else:
                        last_run_time = None
                else:
                    last_run_time = None

                reoccurrence_periods = {
                    'day': task.reoccurrence_day,
                    'month': task.reoccurrence_month,
                    'day_of_week': task.reoccurrence_day_of_week
                }

                run_now = should_run_now(last_run_time=last_run_time, reoccurrence_periods=reoccurrence_periods)
                log_msg(f'Run now: {task.subject} - {run_now}')
                if run_now:
                    full_subject = f'[{job.company}]: {task.subject}'
                    full_subject = replace_key_words(full_subject)

                    log_msg(f'Creating ticket: {full_subject}')
                    agent_freshdesk_id = int(job.engineer.freshdesk_id) if job.engineer else 0
                    if result := create_fd_ticket(subject=full_subject, company_id=job.fd_company_id,
                                                  group_id=job.fd_group_id,
                                                  task_body=task.body, task_type_name=task.task_type.name,
                                                  agent_id=agent_freshdesk_id):

                        TaskRunHistory(job_name=job.name, task_subject=task.subject,
                                       run_date=datetime.now()).save()

                        log_msg(f'Ticket created: {task}')
                    else:
                        log_msg(f'Job failed to create ticket: {job} - {task}')

    except Exception as e:
        log_msg(e)
