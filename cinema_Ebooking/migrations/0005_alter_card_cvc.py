# Generated by Django 4.1.7 on 2023-03-20 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema_Ebooking', '0004_remove_card_cardname_remove_user_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='cvc',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]
