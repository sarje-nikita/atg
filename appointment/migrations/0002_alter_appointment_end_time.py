# Generated by Django 5.0.2 on 2024-02-20 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='end_time',
            field=models.TimeField(null=True),
        ),
    ]