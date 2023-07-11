from django.conf import settings
from django.core.management import BaseCommand
from scheduler.lib.logger import log_msg
from scheduler.lib.run_jobs import run_job_tasks


class Command(BaseCommand):
    help = 'Runs checks on all jobs and generates tickets if appropriate.'

    def handle(self, *args, **options):
        log_msg('Checking jobs to run...')
        run_job_tasks()


if __name__ == '__main__':
    settings.configure()
    Command().handle()