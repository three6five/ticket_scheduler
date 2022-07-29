from django.core.management import BaseCommand
from scheduler.lib.freshdesk.update_fd_data import update_fd_data
from scheduler.models import TimePeriod, TaskType


class Command(BaseCommand):
    help = 'Seed database'

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')
        run_seed()


def seed_time_period():
    for period in ['Yearly', 'Quarterly', 'Monthly', 'Weekly', 'Daily']:
        if TimePeriod.objects.filter(name=period):
            continue
        obj = TimePeriod(name=period)
        obj.save()


def seed_task_type():
    for task_type in ['Issue', 'Internal', 'Project', 'Change', 'Alert', 'Question', 'Scheduled Maintenance', 'Sales']:
        if TaskType.objects.filter(name=task_type):
            continue
        obj = TaskType(name=task_type)
        obj.save()


def run_seed():
    seed_time_period()
    seed_task_type()
    update_fd_data()
