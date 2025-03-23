# Generated by Django 5.1.7 on 2025-03-22 15:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_plate', models.CharField(default='KL-15-1234', max_length=15, unique=True)),
                ('total_seats', models.PositiveIntegerField(default=40)),
            ],
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_number', models.PositiveIntegerField()),
                ('is_available', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passenger_name', models.CharField(max_length=100)),
                ('start_stop', models.CharField(choices=[('Thrissur', 'Thrissur'), ('Irinjalakuda', 'Irinjalakuda'), ('Chalakudy', 'Chalakudy'), ('Angamaly', 'Angamaly'), ('Aluva', 'Aluva'), ('Ernakulam', 'Ernakulam'), ('Tripunithura', 'Tripunithura'), ('Piravom', 'Piravom'), ('Ettumanoor', 'Ettumanoor'), ('Kottayam', 'Kottayam'), ('Changanassery', 'Changanassery'), ('Thiruvalla', 'Thiruvalla'), ('Kayamkulam', 'Kayamkulam'), ('Kollam', 'Kollam'), ('Trivandrum', 'Trivandrum')], max_length=50)),
                ('end_stop', models.CharField(choices=[('Thrissur', 'Thrissur'), ('Irinjalakuda', 'Irinjalakuda'), ('Chalakudy', 'Chalakudy'), ('Angamaly', 'Angamaly'), ('Aluva', 'Aluva'), ('Ernakulam', 'Ernakulam'), ('Tripunithura', 'Tripunithura'), ('Piravom', 'Piravom'), ('Ettumanoor', 'Ettumanoor'), ('Kottayam', 'Kottayam'), ('Changanassery', 'Changanassery'), ('Thiruvalla', 'Thiruvalla'), ('Kayamkulam', 'Kayamkulam'), ('Kollam', 'Kollam'), ('Trivandrum', 'Trivandrum')], max_length=50)),
                ('booking_time', models.DateTimeField(auto_now_add=True)),
                ('seat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seatallocs.seat')),
            ],
        ),
        migrations.CreateModel(
            name='SeatAllocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_stop', models.CharField(choices=[('Thrissur', 'Thrissur'), ('Irinjalakuda', 'Irinjalakuda'), ('Chalakudy', 'Chalakudy'), ('Angamaly', 'Angamaly'), ('Aluva', 'Aluva'), ('Ernakulam', 'Ernakulam'), ('Tripunithura', 'Tripunithura'), ('Piravom', 'Piravom'), ('Ettumanoor', 'Ettumanoor'), ('Kottayam', 'Kottayam'), ('Changanassery', 'Changanassery'), ('Thiruvalla', 'Thiruvalla'), ('Kayamkulam', 'Kayamkulam'), ('Kollam', 'Kollam'), ('Trivandrum', 'Trivandrum')], max_length=50)),
                ('end_stop', models.CharField(choices=[('Thrissur', 'Thrissur'), ('Irinjalakuda', 'Irinjalakuda'), ('Chalakudy', 'Chalakudy'), ('Angamaly', 'Angamaly'), ('Aluva', 'Aluva'), ('Ernakulam', 'Ernakulam'), ('Tripunithura', 'Tripunithura'), ('Piravom', 'Piravom'), ('Ettumanoor', 'Ettumanoor'), ('Kottayam', 'Kottayam'), ('Changanassery', 'Changanassery'), ('Thiruvalla', 'Thiruvalla'), ('Kayamkulam', 'Kayamkulam'), ('Kollam', 'Kollam'), ('Trivandrum', 'Trivandrum')], max_length=50)),
                ('seat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seatallocs.seat')),
            ],
        ),
    ]
