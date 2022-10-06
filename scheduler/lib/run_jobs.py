from datetime import datetime, timedelta

import pandas as pd
from dateutil import relativedelta
import pytz
from scheduler.lib.freshdesk.create_ticket import create_fd_ticket
from scheduler.lib.helpers import replace_key_words
from scheduler.lib.logger import log_msg
from scheduler.models import Job, TaskRunHistory

sleep_time = 1800


def get_next_run_period(start_time, run_count, recur_period):
    if recur_period.name == 'Yearly':
        next_run_time = start_time + relativedelta.relativedelta(months=run_count * 12)
    elif recur_period.name == 'Quarterly':
        next_run_time = start_time + relativedelta.relativedelta(months=run_count * 3)
    elif recur_period.name == 'Monthly':
        next_run_time = start_time + relativedelta.relativedelta(months=run_count)
    elif recur_period.name == 'Weekly':
        next_run_time = start_time + relativedelta.relativedelta(weeks=run_count)
    elif recur_period.name == 'Daily':
        next_run_time = start_time + relativedelta.relativedelta(days=run_count)
    else:
        raise ValueError(f'Unknown recur period: {recur_period}')

    return next_run_time


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

                    run_count = len(task_run_history_df)
                    last_run_time = task_run_history_df.iloc[0].run_date if run_count else None
                else:
                    run_count = 0
                    last_run_time = None

                recur_period = task.recur_period

                next_run_time = get_next_run_period(start_time=job.start_date, run_count=run_count,
                                                      recur_period=recur_period)
                log_msg(f'Next run time for {job} - {task} : {next_run_time}')
                run_conditions = [last_run_time and last_run_time < current_date and next_run_time < current_date,
                                  not last_run_time and next_run_time < current_date]

                if any(run_conditions):
                    full_subject = f'[{job.company}]: {task.subject}'
                    full_subject = replace_key_words(full_subject)

                    log_msg(f'Creating ticket: {full_subject}')
                    if job.engineer:
                        agent_freshdesk_id = int(job.engineer.freshdesk_id)
                    else:
                        agent_freshdesk_id = 0
                    if result := create_fd_ticket(subject=full_subject, company_id=job.fd_company_id, group_id=job.fd_group_id,
                                                  task_body=task.body, task_type_name=task.task_type.name, agent_id=agent_freshdesk_id):
                        TaskRunHistory(job_name=job.name, task_subject=task.subject,
                                       run_date=datetime.now()).save()

                        log_msg(f'Ticket created: {task}')
                    else:
                        log_msg(f'Job failed to create ticket: {job} - {task}')

    except Exception as e:
        log_msg(e)