# Generated by Django 4.0.4 on 2022-04-18 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Kars4U_components', '0008_rename_license_plate_number_car_license_plate'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='currentlyworking',
            field=models.BooleanField(default=0),
        ),
    ]
