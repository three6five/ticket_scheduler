from datetime import datetime, timedelta
from dateutil import relativedelta

from scheduler.lib.async_scheduler import Scheduler
from scheduler.lib.freshdesk.create_ticket import create_fd_ticket
from scheduler.models import Job

sleep_time = 1800


def get_next_run_period(base_time, recur_period):
    if recur_period == 'Monthly':
        next_run_time = base_time + relativedelta.relativedelta(months=1)
    elif recur_period == 'Weekly':
        next_run_time = base_time + relativedelta.relativedelta(weeks=1)
    elif recur_period == 'Bi-Weekly':
        next_run_time = base_time + relativedelta.relativedelta(weeks=2)
    elif recur_period == 'Daily':
        next_run_time = base_time + relativedelta.relativedelta(days=1)
    else:
        raise ValueError(f'Unknown recur period: {recur_period}')

    return next_run_time


def begin_job_run_checks():
    run_job_tasks()

    check_time_mins = 1
    scheduler = Scheduler()
    scheduler.every(check_time_mins).minutes.do(run_job_tasks)
    scheduler.run_continuously()


def run_job_tasks():
    print('running job checks...')
    jobs = Job.objects.all()

    current_date = datetime.now()

    for job in jobs:
        last_run_time = job.last_run_time
        next_run_time = job.next_run_time
        if last_run_time < current_date and next_run_time < current_date:
            for task in job.task_group.tasks:
                full_subject = f'[{job.company}]: {task.subject}'
                print(f'Creating ticket: {full_subject}')
                if result := create_fd_ticket(subject=full_subject,
                                              company_id=job.fd_company_id,
                                              group_id=job.fd_group_id,
                                              task_body=task.body,
                                              task_type=task.task_type):

                    last_run_time = datetime.now()
                    job.next_run_time = get_next_run_period(base_time=last_run_time, recur_period=job.recur_period)
                    job.last_run_time = last_run_time

                    job.save()
