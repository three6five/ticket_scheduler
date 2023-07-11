# Generated by Django 3.2 on 2022-10-24 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0005_auto_20221024_1452'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='recur_period',
        ),
        migrations.AlterField(
            model_name='task',
            name='reoccurrence_month',
            field=models.CharField(default='0', help_text='Asterix(*) represents all, comma seperates multiple, IE. "3,6,9,12" would represent March, June, Sep and Dec ', max_length=32),
        ),
    ]