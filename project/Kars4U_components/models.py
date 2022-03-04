from django.db import models

# Create your models here.
class Car(models.Model):
    car_id = models.IntegerField( primary_key=True)
    license_plate_number = models.CharField(max_length=10)
    state = models.CharField(max_length=25)
    make = models.CharField(max_length=25)
    model = models.CharField(max_length=25)
    color = models.CharField(max_length=25)
    car_type = models.CharField(max_length=25)
    is_available = models.BooleanField(max_length=10)


class Employee(models.Model):
    employee_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=25)
    store_id = models.IntegerField()