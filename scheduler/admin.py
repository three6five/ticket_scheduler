from django.contrib import admin
from .models import Task
from django.contrib.admin import AdminSite


admin.site.site_header = 'Ticket Scheduler'


class TaskInline(admin.TabularInline):
    model = Task

    def get_readonly_fields(self, request, obj=None):
        return ["last_run_time"]


class TaskAdmin(admin.ModelAdmin):
    date_hierarchy = 'start_date'
  #  inlines = TaskInline,


admin.site.register(Task, TaskAdmin)
