# Generated by Django 4.0.6 on 2022-07-22 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0002_taskgrouptask_remove_taskgroup_tasks_taskgroup_tasks_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TaskGroupTask',
            new_name='SubTask',
        ),
    ]
