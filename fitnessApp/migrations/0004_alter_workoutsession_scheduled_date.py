# Generated by Django 5.1.6 on 2025-04-20 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitnessApp', '0003_alter_workoutsession_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workoutsession',
            name='scheduled_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
