# Generated by Django 3.2.4 on 2021-09-06 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_auto_20210906_0154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
