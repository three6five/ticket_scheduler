from django.urls import path
from ticket_scheduler.settings import scheduler_running
from . import views

urlpatterns = [
    path('', views.index, name='index')
]