# Generated by Django 4.1 on 2023-03-21 04:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "cinema_Ebooking",
            "0009_remove_card_expiry_date_card_cvc_card_last_four_and_more",
        ),
    ]

    operations = [
        migrations.DeleteModel(
            name="Card",
        ),
    ]
