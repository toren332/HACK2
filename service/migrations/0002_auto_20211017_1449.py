# Generated by Django 3.1 on 2021-10-17 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='poly',
            name='optima',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='poly',
            name='potreb_2021',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='poly',
            name='potreb_2025',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='poly',
            name='potreb_2030',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='poly',
            name='school',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
