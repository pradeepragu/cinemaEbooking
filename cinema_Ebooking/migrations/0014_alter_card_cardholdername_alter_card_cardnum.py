# Generated by Django 4.1.7 on 2023-03-22 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema_Ebooking', '0013_alter_card_cardholdername_alter_card_cardnum'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='cardHolderName',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='cardNum',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
