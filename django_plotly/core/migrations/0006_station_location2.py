# Generated by Django 4.0.3 on 2023-10-12 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_station_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='STATION_LOCATION2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('station_name', models.CharField(max_length=250)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
            ],
        ),
    ]
