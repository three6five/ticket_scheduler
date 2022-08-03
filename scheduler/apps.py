from django.apps import AppConfig
from ticket_scheduler.settings import scheduler_running


class SchedulerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scheduler'
