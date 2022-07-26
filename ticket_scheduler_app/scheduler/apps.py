from django.apps import AppConfig
from ticket_scheduler.settings import scheduler_running


class SchedulerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scheduler'

    def ready(self):
        import os
        if os.environ.get('RUN_MAIN', None) != 'true' and scheduler_running():
            from scheduler.lib.run_jobs import begin_job_run_checks
            begin_job_run_checks()

