# Generated by Django 3.1.1 on 2020-11-26 10:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_auto_20201126_1200'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='stockk',
        ),
        migrations.AlterField(
            model_name='activity',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 26, 12, 1, 12, 728069)),
        ),
        migrations.AlterField(
            model_name='notification',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 26, 12, 1, 12, 733055)),
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 26, 12, 1, 12, 731061)),
        ),
    ]
