# Generated by Django 4.0.6 on 2022-07-22 08:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('freshdesk_id', models.CharField(default=0, max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Engineer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('freshdesk_id', models.CharField(default=0, max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('freshdesk_id', models.CharField(default=0, max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('subject', models.CharField(max_length=128)),
                ('body', models.TextField(max_length=65000)),
            ],
        ),
        migrations.CreateModel(
            name='TaskType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='TimePeriod',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='TaskGroup',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('tasks', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scheduler.task')),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='task_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scheduler.tasktype'),
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('fd_company_id', models.CharField(max_length=64)),
                ('fd_group_id', models.CharField(max_length=64)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField(null=True)),
                ('enabled', models.BooleanField(default=True)),
                ('last_run_time', models.DateTimeField(null=True)),
                ('next_run_time', models.DateTimeField(null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scheduler.company')),
                ('engineer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='scheduler.engineer')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scheduler.group')),
                ('recur_period', models.ForeignKey(help_text='If monthly, task will be created on the same day (IE. 1st -> 1st), if weekly or bi-weekly it will be the same week day (IE. Monday -> Monday)', on_delete=django.db.models.deletion.CASCADE, to='scheduler.timeperiod')),
                ('task_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scheduler.taskgroup')),
            ],
        ),
    ]