# Generated by Django 5.1.5 on 2025-03-24 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seatallocs', '0002_alter_bus_total_seats'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bus',
            name='total_seats',
            field=models.PositiveIntegerField(default=5),
        ),
    ]
