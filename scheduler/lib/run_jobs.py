from datetime import datetime, timedelta
from dateutil import relativedelta
import pytz
from scheduler.lib.async_scheduler import Scheduler
from scheduler.lib.freshdesk.create_ticket import create_fd_ticket
from scheduler.models import Job

sleep_time = 1800


def get_next_run_period(base_time, recur_period):
    if recur_period.name == 'Monthly':
        next_run_time = base_time + relativedelta.relativedelta(months=1)
    elif recur_period.name == 'Weekly':
        next_run_time = base_time + relativedelta.relativedelta(weeks=1)
    elif recur_period.name == 'Bi-Weekly':
        next_run_time = base_time + relativedelta.relativedelta(weeks=2)
    elif recur_period.name == 'Daily':
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
    utc = pytz.UTC
    current_date = utc.localize(current_date)

    for job in jobs:
        last_run_time = job.last_run_time
        next_run_time = job.next_run_time

        run_conditions = [last_run_time and last_run_time < current_date and next_run_time < current_date,
                          not last_run_time and next_run_time < current_date]

        if any(run_conditions):
            for task in job.task_group.tasks.all():
                full_subject = f'[{job.company}]: {task.subject}'
                print(f'Creating ticket: {full_subject}')
                if result := create_fd_ticket(subject=full_subject,
                                              company_id=job.fd_company_id,
                                              group_id=job.fd_group_id,
                                              task_body=task.body,
                                              task_type_name=task.task_type.name,
                                              agent_id=job.engineer_id):

                    last_run_time = datetime.now()
                    job.next_run_time = get_next_run_period(base_time=last_run_time, recur_period=job.recur_period)
                    job.last_run_time = last_run_time

                    job.save()
                else:
                    print(f'Job failed to create ticket: {job}')
