from datetime import datetime, timedelta
from dateutil import relativedelta
import pytz
from scheduler.lib.async_scheduler import Scheduler
from scheduler.lib.freshdesk.create_ticket import create_fd_ticket
from scheduler.lib.logger import log_msg
from scheduler.models import Job

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


def begin_job_run_checks():
    check_time_mins = 1
    scheduler = Scheduler()
    scheduler.every(check_time_mins).minutes.do(run_job_tasks)
    scheduler.run_continuously()
    log_msg(f'Tasks scheduled to run every {check_time_mins} mins...')


def run_job_tasks():
    log_msg('running job checks...')
    jobs = Job.objects.all()

    current_date = datetime.now()
    utc = pytz.UTC
    current_date = utc.localize(current_date, dt=utc)

    for job in jobs:
        log_msg(f'Checking job {job} for running...')
        last_run_time = job.last_run_time
        next_run_time = job.next_run_time

        run_conditions = [last_run_time and last_run_time < current_date and next_run_time < current_date,
                          not last_run_time and next_run_time < current_date]

        if any(run_conditions):
            for task in job.task_group.tasks.all():
                full_subject = f'[{job.company}]: {task.subject}'
                log_msg(f'Creating ticket: {full_subject}')
                result = create_fd_ticket(subject=full_subject,
                                          company_id=job.fd_company_id,
                                          group_id=job.fd_group_id,
                                          task_body=task.body,
                                          task_type_name=task.task_type.name,
                                          agent_id=int(job.engineer.freshdesk_id))
                if not result:
                    log_msg(f'Job failed to create ticket: {job}')

            run_count = job.run_count + 1
            job.next_run_time = get_next_run_period(start_time=job.start_date, run_count=run_count,
                                                    recur_period=job.recur_period)
            job.last_run_time = datetime.now()
            job.run_count = run_count

            job.save()
        else:
            log_msg(f'No tasks to run for job {job}, continuing...')
