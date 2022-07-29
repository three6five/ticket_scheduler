# Generated by Django 4.0.6 on 2022-07-29 08:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0004_remove_job_end_date_job_run_count_alter_job_engineer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='recur_period',
        ),
        migrations.AddField(
            model_name='task',
            name='recur_period',
            field=models.ForeignKey(default='Monthly', help_text='If monthly, task will be created on the same day (IE. 1st -> 1st), if weekly or bi-weekly it will be the same week day (IE. Monday -> Monday)', on_delete=django.db.models.deletion.CASCADE, to='scheduler.timeperiod'),
            preserve_default=False,
        ),
    ]
