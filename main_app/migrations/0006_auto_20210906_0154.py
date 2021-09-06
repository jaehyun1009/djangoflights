# Generated by Django 3.2.4 on 2021-09-06 01:54

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_auto_20210906_0145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 6, 1, 54, 4, 131232)),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='seat',
            field=models.CharField(max_length=3, validators=[django.core.validators.RegexValidator('^0[1-4][A-D]|0[5-9][A-G]|1[0-5][A-G]|1[6-9][A-J]|[2-3][0-9][A-J]$', code='invalid_seat', message='Please follow the instructions in picking a seat number.')]),
        ),
    ]
