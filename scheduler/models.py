import datetime

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
    task_subject = models.CharField(max_length=128)
    run_date = models.DateTimeField()

    def __str__(self):
        return f'{self.job_name} - {self.task_subject} - {self.run_date}'


class Task(models.Model):
    help_text_day = 'Asterix(*) represents all, comma seperates multiple, IE. "1,10,15" would represent the 1st, ' \
                    '10th and 15th day of the month '
    help_text_month = 'Asterix(*) represents all, comma seperates multiple, IE. "3,6,9,12" would represent March, June, ' \
                      'Sep and Dec '
    id = models.AutoField(primary_key=True)
    subject = models.CharField(max_length=128, unique=True)
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    reoccurrence_day = models.CharField(max_length=32, default='0', help_text=help_text_day)
    reoccurrence_month = models.CharField(max_length=32, default='0', help_text=help_text_month)
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