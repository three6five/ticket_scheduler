# Generated by Django 4.0.6 on 2022-10-06 13:24

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0003_alter_job_engineer'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2022, 10, 6, 13, 24, 0, 833042, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='job',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]