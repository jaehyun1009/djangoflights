# Generated by Django 3.2.4 on 2021-09-06 05:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0007_alter_ticket_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='seat',
            field=models.CharField(max_length=3, validators=[django.core.validators.RegexValidator('^0[1-4][A-D]|0[5-9][A-G]|1[0-5][A-G]|1[6-9][A-J]|2[0-9][A-J]|3[0-4][A-J]$', code='invalid_seat', message='Please follow the instructions in picking a seat number.')]),
        ),
    ]
