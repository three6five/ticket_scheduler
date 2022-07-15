from django.core.management import BaseCommand
from scheduler.models import TimePeriod


class Command(BaseCommand):
    help = 'Seed database'

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')
        run_seed()


def seed_time_period():
    for period in ['Monthly', 'Bi-Weekly', 'Weekly', 'Daily']:
        obj = TimePeriod(name=period)
        obj.save()


def seed_freshdesk_data():
    pass
    # todo - Create Companies, Groups, Engineers from Freshdesk database


def run_seed():
    seed_time_period()
    seed_freshdesk_data()
