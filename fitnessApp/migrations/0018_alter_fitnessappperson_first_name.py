# Generated by Django 5.1.6 on 2025-06-12 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitnessApp', '0017_fitnessappperson_email_fitnessappperson_phone_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fitnessappperson',
            name='first_name',
            field=models.CharField(max_length=500),
        ),
    ]
