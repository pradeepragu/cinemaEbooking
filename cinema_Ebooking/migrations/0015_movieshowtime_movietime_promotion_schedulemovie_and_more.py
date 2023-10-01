# Generated by Django 4.1.7 on 2023-03-23 18:42

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cinema_Ebooking', '0014_alter_card_cardholdername_alter_card_cardnum'),
    ]

    operations = [
        migrations.CreateModel(
            name='MovieShowTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('showTimes', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='MovieTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('showDateTime', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount', models.IntegerField()),
                ('user_notified', models.BooleanField(default=False, editable=False)),
                ('promo_code', models.CharField(max_length=10, unique=True)),
                ('valid_upto', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='ScheduleMovie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('showDate', models.DateField(db_index=True)),
                ('MovieTime', models.TextField(choices=[('10:00AM', '10:00AM'), ('13:00PM', '13:00PM'), ('16:00PM', '16:00PM'), ('19:00PM', '19:00PM'), ('22:00PM', '22:00PM')], max_length=10)),
                ('child_cost', models.FloatField(default=5.99)),
                ('adult_cost', models.FloatField(default=9.99)),
                ('senior_cost', models.FloatField(default=6.99)),
                ('booked_seats', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(50), django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.CreateModel(
            name='ShowRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theatre', models.CharField(max_length=50, unique=True)),
                ('seatNum', models.IntegerField(default=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='movie',
            name='description',
        ),
        migrations.AddField(
            model_name='movie',
            name='sypnopsis',
            field=models.TextField(default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='movie',
            name='archived',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='cast',
            field=models.CharField(default='', max_length=400),
        ),
        migrations.AlterField(
            model_name='movie',
            name='status',
            field=models.CharField(choices=[('Now Playing', 'Now Playing'), ('Coming Soon', 'Coming Soon')], default='', max_length=50),
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_01', models.CharField(choices=[['seat', 'seat'], ['seat selected', 'seat selected'], ['seat occupied', 'seat occupied']], default='seat', max_length=15)),
                ('seat_02', models.CharField(choices=[['seat', 'seat'], ['seat selected', 'seat selected'], ['seat occupied', 'seat occupied']], default='seat', max_length=15)),
                ('seat_03', models.CharField(choices=[['seat', 'seat'], ['seat selected', 'seat selected'], ['seat occupied', 'seat occupied']], default='seat', max_length=15)),
                ('seat_04', models.CharField(choices=[['seat', 'seat'], ['seat selected', 'seat selected'], ['seat occupied', 'seat occupied']], default='seat', max_length=15)),
                ('seat_05', models.CharField(choices=[['seat', 'seat'], ['seat selected', 'seat selected'], ['seat occupied', 'seat occupied']], default='seat', max_length=15)),
                ('seat_06', models.CharField(choices=[['seat', 'seat'], ['seat selected', 'seat selected'], ['seat occupied', 'seat occupied']], default='seat', max_length=15)),
                ('seat_07', models.CharField(choices=[['seat', 'seat'], ['seat selected', 'seat selected'], ['seat occupied', 'seat occupied']], default='seat', max_length=15)),
                ('seat_08', models.CharField(choices=[['seat', 'seat'], ['seat selected', 'seat selected'], ['seat occupied', 'seat occupied']], default='seat', max_length=15)),
                ('seat_09', models.CharField(choices=[['seat', 'seat'], ['seat selected', 'seat selected'], ['seat occupied', 'seat occupied']], default='seat', max_length=15)),
                ('seat_10', models.CharField(choices=[['seat', 'seat'], ['seat selected', 'seat selected'], ['seat occupied', 'seat occupied']], default='seat', max_length=15)),
                ('seat_11', models.CharField(choices=[['seat', 'seat'], ['seat selected', 'seat selected'], ['seat occupied', 'seat occupied']], default='seat', max_length=15)),
                ('seat_12', models.CharField(choices=[['seat', 'seat'], ['seat selected', 'seat selected'], ['seat occupied', 'seat occupied']], default='seat', max_length=15)),
                ('seat_13', models.CharField(choices=[['seat', 'seat'], ['seat selected', 'seat selected'], ['seat occupied', 'seat occupied']], default='seat', max_length=15)),
                ('seat_14', models.CharField(choices=[['seat', 'seat'], ['seat selected', 'seat selected'], ['seat occupied', 'seat occupied']], default='seat', max_length=15)),
                ('seat_15', models.CharField(choices=[['seat', 'seat'], ['seat selected', 'seat selected'], ['seat occupied', 'seat occupied']], default='seat', max_length=15)),
                ('seat_16', models.CharField(choices=[['seat', 'seat'], ['seat selected', 'seat selected'], ['seat occupied', 'seat occupied']], default='seat', max_length=15)),
                ('seat_17', models.CharField(choices=[['seat', 'seat'], ['seat selected', 'seat selected'], ['seat occupied', 'seat occupied']], default='seat', max_length=15)),
                ('seat_18', models.CharField(choices=[['seat', 'seat'], ['seat selected', 'seat selected'], ['seat occupied', 'seat occupied']], default='seat', max_length=15)),
                ('seat_19', models.CharField(choices=[['seat', 'seat'], ['seat selected', 'seat selected'], ['seat occupied', 'seat occupied']], default='seat', max_length=15)),
                ('seat_20', models.CharField(choices=[['seat', 'seat'], ['seat selected', 'seat selected'], ['seat occupied', 'seat occupied']], default='seat', max_length=15)),
                ('seat_21', models.CharField(choices=[['seat', 'seat'], ['seat selected', 'seat selected'], ['seat occupied', 'seat occupied']], default='seat', max_length=15)),
                ('seat_22', models.CharField(choices=[['seat', 'seat'], ['seat selected', 'seat selected'], ['seat occupied', 'seat occupied']], default='seat', max_length=15)),
                ('seat_23', models.CharField(choices=[['seat', 'seat'], ['seat selected', 'seat selected'], ['seat occupied', 'seat occupied']], default='seat', max_length=15)),
                ('seat_24', models.CharField(choices=[['seat', 'seat'], ['seat selected', 'seat selected'], ['seat occupied', 'seat occupied']], default='seat', max_length=15)),
                ('seat_25', models.CharField(choices=[['seat', 'seat'], ['seat selected', 'seat selected'], ['seat occupied', 'seat occupied']], default='seat', max_length=15)),
                ('seat_26', models.CharField(choices=[['seat', 'seat'], ['seat selected', 'seat selected'], ['seat occupied', 'seat occupied']], default='seat', max_length=15)),
                ('seat_27', models.CharField(choices=[['seat', 'seat'], ['seat selected', 'seat selected'], ['seat occupied', 'seat occupied']], default='seat', max_length=15)),
                ('seat_28', models.CharField(choices=[['seat', 'seat'], ['seat selected', 'seat selected'], ['seat occupied', 'seat occupied']], default='seat', max_length=15)),
                ('seat_29', models.CharField(choices=[['seat', 'seat'], ['seat selected', 'seat selected'], ['seat occupied', 'seat occupied']], default='seat', max_length=15)),
                ('seat_30', models.CharField(choices=[['seat', 'seat'], ['seat selected', 'seat selected'], ['seat occupied', 'seat occupied']], default='seat', max_length=15)),
                ('seat_31', models.CharField(choices=[['seat', 'seat'], ['seat selected', 'seat selected'], ['seat occupied', 'seat occupied']], default='seat', max_length=15)),
                ('seat_32', models.CharField(choices=[['seat', 'seat'], ['seat selected', 'seat selected'], ['seat occupied', 'seat occupied']], default='seat', max_length=15)),
                ('seat_33', models.CharField(choices=[['seat', 'seat'], ['seat selected', 'seat selected'], ['seat occupied', 'seat occupied']], default='seat', max_length=15)),
                ('seat_34', models.CharField(choices=[['seat', 'seat'], ['seat selected', 'seat selected'], ['seat occupied', 'seat occupied']], default='seat', max_length=15)),
                ('seat_35', models.CharField(choices=[['seat', 'seat'], ['seat selected', 'seat selected'], ['seat occupied', 'seat occupied']], default='seat', max_length=15)),
                ('seat_36', models.CharField(choices=[['seat', 'seat'], ['seat selected', 'seat selected'], ['seat occupied', 'seat occupied']], default='seat', max_length=15)),
                ('seat_37', models.CharField(choices=[['seat', 'seat'], ['seat selected', 'seat selected'], ['seat occupied', 'seat occupied']], default='seat', max_length=15)),
                ('seat_38', models.CharField(choices=[['seat', 'seat'], ['seat selected', 'seat selected'], ['seat occupied', 'seat occupied']], default='seat', max_length=15)),
                ('seat_39', models.CharField(choices=[['seat', 'seat'], ['seat selected', 'seat selected'], ['seat occupied', 'seat occupied']], default='seat', max_length=15)),
                ('seat_40', models.CharField(choices=[['seat', 'seat'], ['seat selected', 'seat selected'], ['seat occupied', 'seat occupied']], default='seat', max_length=15)),
                ('seat_41', models.CharField(choices=[['seat', 'seat'], ['seat selected', 'seat selected'], ['seat occupied', 'seat occupied']], default='seat', max_length=15)),
                ('seat_42', models.CharField(choices=[['seat', 'seat'], ['seat selected', 'seat selected'], ['seat occupied', 'seat occupied']], default='seat', max_length=15)),
                ('seat_43', models.CharField(choices=[['seat', 'seat'], ['seat selected', 'seat selected'], ['seat occupied', 'seat occupied']], default='seat', max_length=15)),
                ('seat_44', models.CharField(choices=[['seat', 'seat'], ['seat selected', 'seat selected'], ['seat occupied', 'seat occupied']], default='seat', max_length=15)),
                ('seat_45', models.CharField(choices=[['seat', 'seat'], ['seat selected', 'seat selected'], ['seat occupied', 'seat occupied']], default='seat', max_length=15)),
                ('seat_46', models.CharField(choices=[['seat', 'seat'], ['seat selected', 'seat selected'], ['seat occupied', 'seat occupied']], default='seat', max_length=15)),
                ('seat_47', models.CharField(choices=[['seat', 'seat'], ['seat selected', 'seat selected'], ['seat occupied', 'seat occupied']], default='seat', max_length=15)),
                ('seat_48', models.CharField(choices=[['seat', 'seat'], ['seat selected', 'seat selected'], ['seat occupied', 'seat occupied']], default='seat', max_length=15)),
                ('seat_49', models.CharField(choices=[['seat', 'seat'], ['seat selected', 'seat selected'], ['seat occupied', 'seat occupied']], default='seat', max_length=15)),
                ('seat_50', models.CharField(choices=[['seat', 'seat'], ['seat selected', 'seat selected'], ['seat occupied', 'seat occupied']], default='seat', max_length=15)),
                ('show', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cinema_Ebooking.schedulemovie')),
            ],
        ),
        migrations.AddField(
            model_name='schedulemovie',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema_Ebooking.movie'),
        ),
        migrations.AddField(
            model_name='schedulemovie',
            name='theatre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema_Ebooking.showroom'),
        ),
        migrations.AlterUniqueTogether(
            name='schedulemovie',
            unique_together={('theatre', 'showDate', 'MovieTime')},
        ),
    ]