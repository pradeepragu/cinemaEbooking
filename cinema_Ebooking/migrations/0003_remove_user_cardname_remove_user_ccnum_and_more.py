# Generated by Django 4.1.7 on 2023-03-19 18:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cinema_Ebooking', '0002_user_apartnumber'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='cardname',
        ),
        migrations.RemoveField(
            model_name='user',
            name='ccnum',
        ),
        migrations.RemoveField(
            model_name='user',
            name='valid',
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cardname', models.CharField(blank=True, max_length=100, null=True)),
                ('ccnum', models.CharField(blank=True, max_length=150, null=True)),
                ('valid', models.TextField(blank=True, null=True)),
                ('last_four', models.CharField(blank=True, max_length=4, null=True)),
                ('cvc', models.CharField(blank=True, max_length=3, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
