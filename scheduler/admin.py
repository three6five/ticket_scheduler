from django.contrib import admin
from django.core.exceptions import ValidationError

from .models import Task, TaskGroup, Job, SubTask, TaskRunHistory
from django.contrib.admin import AdminSite
from django.forms import ModelForm


admin.site.site_header = 'Ticket Scheduler'


class TaskForm(ModelForm):
    def clean(self):
        errors = {}

        validation_values = {
            'day': self['day'],
            'month': self['month'],
            'day_of_week': self['day_of_week']
        }
        for key, value in validation_values.items():
            real_value = value.value()
            if real_value == '' and self['month'].value() == '':
                errors.update({key: 'Values cannot be empty. Use an asterisk (*) to indicate all values.'})
                continue

            if key == 'day':
                if real_value != '*':
                    if ',' in real_value:
                        for val in real_value.split(','):
                            if not val.isnumeric():
                                errors.update({key: f'{val} is not a valid value, must be numeric'})
                                break
                            if int(val) > 31 or int(val) <= 0:
                                errors.update({key: f'{val} is not a valid value, must be 1-31'})
                    else:
                        if int(real_value) > 31 or int(real_value) <= 0:
                            errors.update({key: f'{real_value} is not a valid value, must be 1-31'})

            elif key == 'month':
                if real_value != '*':
                    if ',' in real_value:
                        for val in real_value.split(','):
                            if not val.isnumeric():
                                errors.update({key: f'{val} is not a valid value, must be numeric'})
                                break
                            if int(val) > 12 or int(val) <= 0:
                                errors.update({key: f'{val} is not a valid value, must be 1-12'})
                    else:
                        if int(real_value) > 12 or int(real_value) <= 0:
                            errors.update({key: f'{real_value} is not a valid value, must be 1-12'})

            elif key == 'day_of_week':
                if real_value != '*':
                    if ',' in real_value:
                        for val in real_value.split(','):
                            if not val.isnumeric():
                                errors.update({key: f'{val} is not a valid value, must be numeric'})
                                break
                            if int(val) > 7 or int(val) <= 0:
                                errors.update({key: f'{val} is not a valid value, must be 1-7'})
                    else:
                        if int(real_value) > 7 or int(real_value) <= 0:
                            errors.update({key: f'{real_value} is not a valid value, must be 1-7'})

        if errors:
            raise ValidationError(message=errors)


class TaskAdmin(admin.ModelAdmin):
    list_display = ('subject', 'day', 'month', 'day_of_week')
    form = TaskForm


class SubTaskInline(admin.TabularInline):
    model = SubTask
    can_delete = True
    extra = 0


class TaskGroupAdmin(admin.ModelAdmin):
    inlines = (SubTaskInline,)


class JobAdmin(admin.ModelAdmin):
    list_display = ('name', 'enabled', 'task_group')
    def get_readonly_fields(self, request, obj=None):
        return ['fd_group_id', 'fd_company_id']


class TaskRunHistoryAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        return ['job_name', 'task_subject', 'run_date']


admin.site.register(TaskGroup, TaskGroupAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(TaskRunHistory, TaskRunHistoryAdmin)
