# Generated by Django 4.0.3 on 2022-03-04 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Kars4U_components', '0002_rename_available_car_is_available'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='id',
        ),
        migrations.AlterField(
            model_name='car',
            name='license_plate_number',
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
    ]
