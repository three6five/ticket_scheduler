from django.apps import AppConfig

from scheduler.lib.run_jobs import begin_job_run_checks
from ticket_scheduler.settings import is_running


class SchedulerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scheduler'

    def ready(self):
        import os
        if os.environ.get('RUN_MAIN', None) != 'true' and is_running():
            begin_job_run_checks()

