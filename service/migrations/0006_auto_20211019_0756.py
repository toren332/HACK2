# Generated by Django 3.1 on 2021-10-19 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0005_auto_20211019_0751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='nagruzka',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='school',
            name='nagruzka_2025year',
            field=models.FloatField(),
        ),
    ]
