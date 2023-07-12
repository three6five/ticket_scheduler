# Generated by Django 4.0.9 on 2023-07-12 08:24

from django.db import migrations, models
import scheduler.models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0008_alter_task_reoccurrence_day_of_week'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='reoccurrence_day',
            field=models.CharField(default='*', help_text='Asterix(*) represents all, comma seperates multiple, IE. "1,10,15" would represent the 1st, 10th and 15th day of the month', max_length=32, validators=[scheduler.models.day_validator]),
        ),
        migrations.AlterField(
            model_name='task',
            name='reoccurrence_day_of_week',
            field=models.CharField(default='*', help_text='Asterix(*) represents all, comma seperates multiple, IE. "1,3,5" would represent Monday, Wednesday and Friday.', max_length=32, validators=[scheduler.models.day_of_week_validator]),
        ),
        migrations.AlterField(
            model_name='task',
            name='reoccurrence_month',
            field=models.CharField(default='*', help_text='Asterix(*) represents all, comma seperates multiple, IE. "1,6,12" would represent January, June and December', max_length=32, validators=[scheduler.models.month_validator]),
        ),
    ]
