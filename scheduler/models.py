import datetime

from django.core.exceptions import ValidationError
from django.db import models


class Engineer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    freshdesk_id = models.CharField(max_length=64, default=0)

    def __str__(self):
        return self.name


class Group(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    freshdesk_id = models.CharField(max_length=64, default=0)

    def __str__(self):
        return self.name


class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    freshdesk_id = models.CharField(max_length=64, default=0)

    def __str__(self):
        return self.name


class TimePeriod(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class TaskType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class SubTask(models.Model):
    task_group = models.ForeignKey("TaskGroup", related_name='task_group_through', on_delete=models.CASCADE)
    task = models.ForeignKey("Task", related_name='task_group_through', on_delete=models.CASCADE)

    class Meta:
        ordering = ['task_group']

    def __str__(self):
        return self.task_group.name


class TaskRunHistory(models.Model):
    id = models.AutoField(primary_key=True)
    job_name = models.CharField(max_length=128)
    company = models.CharField(max_length=128)
    task_subject = models.CharField(max_length=128)
    run_date = models.DateTimeField()

    def __str__(self):
        return f'{self.job_name} {self.company} - {self.task_subject} - {self.run_date}'


def task_validator(value: str):
    if value != '*':
        if ',' in value:
            for val in value.split(','):
                if not val.isnumeric() or val == 0:
                    raise ValueError(f'{val} is not a valid value, must be numeric above 0')
        else:
            if not value.isnumeric():
                raise ValueError(f'{value} is not a valid value, must be numeric above 0')


def day_validator(value: str):
    if value != '*':
        if ',' in value:
            for val in value.split(','):
                if not val.isnumeric():
                    raise ValidationError(f'{val} is not a valid value, must be numeric')
                if 0 >= int(val) > 31:
                    raise ValidationError(f'{val} is not a valid value, must be below 1-31')
        else:
            if 0 >= int(value) > 31:
                raise ValidationError(f'{value} is not a valid value, must be below 1-31')

    return value


def month_validator(value: str):
    if value != '*':
        if ',' in value:
            for val in value.split(','):
                if 0 >= int(val) > 12:
                    raise ValidationError(f'{val} is not a valid value, must be 1-12')
        else:
            if 0 >= int(value) > 12:
                raise ValidationError(f'{value} is not a valid value, must be 1-12')

    return value


def day_of_week_validator(value: str):
    if value != '*':
        if ',' in value:
            for val in value.split(','):
                if int(val) > 7:
                    raise ValueError(f'{val} is not a valid value, must be 1-7')
        else:
            if int(value) > 7:
                raise ValueError(f'{value} is not a valid value, must be 1-7')

    return value


class Task(models.Model):
    help_text_day = 'Asterix(*) represents all, comma seperates multiple, IE. "1,10,15" would represent the 1st, ' \
                    '10th and 15th day of the month'
    help_text_month = 'Asterix(*) represents all, comma seperates multiple, IE. "1,6,12" would represent January, June ' \
                      'and December'
    help_text_day_of_week = 'Asterix(*) represents all, comma seperates multiple, IE. "1,3,5" would represent Monday, ' \
                            'Wednesday and Friday.'
    id = models.AutoField(primary_key=True)
    subject = models.CharField(max_length=128, unique=True)
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    day = models.CharField(max_length=32, default='*', help_text=help_text_day,
                           validators=[day_validator])
    month = models.CharField(max_length=32, default='*', help_text=help_text_month,
                             validators=[month_validator])
    day_of_week = models.CharField(max_length=32, default='*', help_text=help_text_day_of_week,
                                   validators=[day_of_week_validator])
    body = models.TextField(max_length=65000)

    def __str__(self):
        return f'{self.subject}'


class TaskGroup(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    tasks = models.ManyToManyField(Task, related_name='tasks', through=SubTask)

    def __str__(self):
        return self.name


class Job(models.Model):
    optional_help_text = 'Optional'

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, unique=True)
    task_group = models.ForeignKey(TaskGroup, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    fd_company_id = models.CharField(max_length=64)
    engineer = models.ForeignKey(Engineer, on_delete=models.CASCADE, null=True, blank=True, help_text=optional_help_text)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    fd_group_id = models.CharField(max_length=64)
    start_date = models.DateTimeField()
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.fd_company_id = Company.objects.get(name=self.company).freshdesk_id
        self.fd_group_id = Group.objects.get(name=self.group).freshdesk_id

        super().save()