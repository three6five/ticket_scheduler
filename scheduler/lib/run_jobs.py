from datetime import datetime
import pandas as pd
import pytz
from scheduler.lib.freshdesk.create_ticket import create_fd_ticket
from scheduler.lib.helpers import replace_key_words
from scheduler.lib.logger import log_msg
from scheduler.models import Job, TaskRunHistory




def should_run_now(last_run_time, reoccurrence_periods):
    day = reoccurrence_periods['day']
    month = reoccurrence_periods['month']

    reoccurrence_days = day.split(',')
    reoccurrence_months = month.split(',')

    try:
        reoccurrence_days = list(map(lambda x: int(x), reoccurrence_days.split(',')))
        reoccurrence_months = list(map(lambda x: int(x), reoccurrence_months.split(',')))

    except Exception as e:
        log_msg(f'Error converting days/months to int: {e}')
        raise ValueError(e)

    last_run_day = 0
    last_run_month = 0

    if last_run_time:
        last_run_day = last_run_time.day
        last_run_month = last_run_time.month

    now = datetime.now()
    now_day = now.day
    now_month = now.month

    day_passes = any(now_day == day for day in reoccurrence_days)
    month_passes = any(now_month == month for month in reoccurrence_months)

    last_run_passes = last_run_day != now_day and last_run_month != now_month

    return all((day_passes, month_passes, last_run_passes))


def run_job_tasks():
    try:
        log_msg('running job checks...')
        jobs = Job.objects.all()

        if not any(job.enabled for job in jobs):
            log_msg('No enabled jobs found...')
            return

        current_date = datetime.now()
        utc = pytz.UTC
        current_date = utc.localize(current_date)

        all_run_history_df = pd.DataFrame(TaskRunHistory.objects.all().values())

        for job in jobs:
            log_msg(f'Checking job {job} for tasks to run..')

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
                    'month': task.reoccurrence_month
                }

                if should_run_now(last_run_time=last_run_time, reoccurrence_periods=reoccurrence_periods):
                    full_subject = f'[{job.company}]: {task.subject}'
                    full_subject = replace_key_words(full_subject)

                    log_msg(f'Creating ticket: {full_subject}')
                    agent_freshdesk_id = int(job.engineer.freshdesk_id) if job.engineer else 0
                    if result := create_fd_ticket(subject=full_subject, company_id=job.fd_company_id, group_id=job.fd_group_id,
                                                  task_body=task.body, task_type_name=task.task_type.name, agent_id=agent_freshdesk_id):

                        TaskRunHistory(job_name=job.name, task_subject=task.subject,
                                       run_date=datetime.now()).save()

                        log_msg(f'Ticket created: {task}')
                    else:
                        log_msg(f'Job failed to create ticket: {job} - {task}')

    except Exception as e:
        log_msg(e)