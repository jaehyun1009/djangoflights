# Generated by Django 3.2.4 on 2021-09-03 17:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=3)),
                ('iso', models.CharField(max_length=2)),
                ('lat', models.DecimalField(decimal_places=6, max_digits=10)),
                ('lon', models.DecimalField(decimal_places=6, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('airport', models.ManyToManyField(to='main_app.Airport')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('seat_class', models.CharField(choices=[('E', 'Economy'), ('B', 'Business'), ('F', 'First Class')], default='E', max_length=1)),
                ('destination', models.ManyToManyField(related_name='destination_airport', to='main_app.Airport')),
                ('origin', models.ManyToManyField(related_name='origin_airport', to='main_app.Airport')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.profile')),
            ],
        ),
    ]