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


class Task(models.Model):
    recur_help_text = 'If monthly, task will be created on the same day (IE. 1st -> 1st), if weekly or bi-weekly it will be the same week day (IE. Monday -> Monday)'

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    body = models.TextField(max_length=65000)
    engineer = models.ForeignKey(Engineer, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True)
    recur_period = models.ForeignKey(TimePeriod, on_delete=models.CASCADE, help_text=recur_help_text)
    enabled = models.BooleanField(default=True)
    last_run_time = models.DateTimeField(null=True)

    def __str__(self):
        return f'{self.client} - {self.name}'



