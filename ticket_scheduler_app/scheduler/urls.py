from django.urls import path
from ticket_scheduler.settings import scheduler_running
from . import views
from .lib.run_jobs import begin_job_run_checks

urlpatterns = [
    path('', views.index, name='index')
]

#if scheduler_running():
#    begin_job_run_checks()