# Generated by Django 4.1.7 on 2023-04-25 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema_Ebooking', '0023_booking'),
    ]

    operations = [
        migrations.AddField(
            model_name='tickets',
            name='price',
            field=models.TextField(blank=True, null=True),
        ),
    ]
