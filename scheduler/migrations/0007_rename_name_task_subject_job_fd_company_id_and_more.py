# Generated by Django 4.0.6 on 2022-07-20 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0006_remove_task_company_remove_task_enabled_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='name',
            new_name='subject',
        ),
        migrations.AddField(
            model_name='job',
            name='fd_company_id',
            field=models.CharField(default='0', max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='job',
            name='fd_group_id',
            field=models.CharField(default='0', max_length=64),
            preserve_default=False,
        ),
    ]
