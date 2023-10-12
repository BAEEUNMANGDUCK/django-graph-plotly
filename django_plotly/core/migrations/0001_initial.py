# Generated by Django 4.0.3 on 2023-10-10 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FINEDUST',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('weighted_average', models.FloatField()),
            ],
            options={
                'ordering': ('date',),
            },
        ),
    ]
