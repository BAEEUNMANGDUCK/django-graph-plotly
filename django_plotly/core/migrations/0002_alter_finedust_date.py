# Generated by Django 4.0.3 on 2023-10-10 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finedust',
            name='date',
            field=models.IntegerField(),
        ),
    ]
