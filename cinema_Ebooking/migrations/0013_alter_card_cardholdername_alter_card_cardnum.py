# Generated by Django 4.1.7 on 2023-03-22 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema_Ebooking', '0012_rename_ccnum_card_cardnum_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='cardHolderName',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='cardNum',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
