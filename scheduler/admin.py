from django.contrib import admin
from .models import Task, TaskGroup, Job, SubTask, TaskRunHistory
from django.contrib.admin import AdminSite


admin.site.site_header = 'Ticket Scheduler'


#class TaskAdmin(admin.ModelAdmin):
   # date_hierarchy = 'start_date'

  #  def get_readonly_fields(self, request, obj=None):
  #      return ["last_run_time"]


class SubTaskInline(admin.TabularInline):
    model = SubTask
    can_delete = True
    extra = 0


class TaskGroupAdmin(admin.ModelAdmin):
    inlines = (SubTaskInline,)


class JobAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        return ['fd_group_id', 'fd_company_id']


class TaskRunHistoryAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        return ['job_name', 'task_subject', 'run_date']


admin.site.register(TaskGroup, TaskGroupAdmin)
admin.site.register(Task)
admin.site.register(Job, JobAdmin)
admin.site.register(TaskRunHistory, TaskRunHistoryAdmin)
