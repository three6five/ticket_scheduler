from django.db import models

from scheduler.lib.freshdesk.local_requests import get_company_id_from_name


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


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    subject = models.CharField(max_length=128)
    body = models.TextField(max_length=65000)

    def __str__(self):
        return f'{self.subject}'


class TaskGroup(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    tasks = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Job(models.Model):
    recur_help_text = 'If monthly, task will be created on the same day (IE. 1st -> 1st), if weekly or bi-weekly it will be the same week day (IE. Monday -> Monday)'

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    task_group = models.ForeignKey(TaskGroup, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    fd_company_id = models.CharField(max_length=64)
    engineer = models.ForeignKey(Engineer, on_delete=models.CASCADE, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    fd_group_id = models.CharField(max_length=64)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True)
    recur_period = models.ForeignKey(TimePeriod, on_delete=models.CASCADE, help_text=recur_help_text)
    enabled = models.BooleanField(default=True)
    last_run_time = models.DateTimeField(null=True)
    next_run_time = models.DateTimeField(null=True)

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        from scheduler.lib.run_jobs import get_next_run_period

        base_date = self.start_date if self.last_run_time is None else self.last_run_time
        self.next_run_time = get_next_run_period(base_date, self.recur_period)
        self.fd_company_id = Company.objects.get(name=self.company).freshdesk_id
        self.fd_group_id = Group.objects.get(name=self.group).freshdesk_id


