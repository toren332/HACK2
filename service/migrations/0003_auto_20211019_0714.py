# Generated by Django 3.1 on 2021-10-19 07:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_auto_20211017_1449'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poly',
            name='live_humans_2030',
        ),
        migrations.RemoveField(
            model_name='poly',
            name='potreb_2030',
        ),
        migrations.RemoveField(
            model_name='poly',
            name='transports',
        ),
    ]