from datetime import datetime, timedelta

from scheduler.models import Task


def get_next_run_period(start_time, recur_period, last_run_time):
    if recur_period == 'Monthly':
        pass
        #We'll need the day and hour of start time
    elif recur_period == 'Weekly':
        pass
        #We'll need the day of week from start_time

    return 0


def run_tasks():
    tasks = Task.objects.all()

    current_date = datetime.now()

    for task in tasks:
        next_run_time = get_next_run_period(task.last_run_time, task.recur_period, task.last_run_time)
