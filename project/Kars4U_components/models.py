from django.db import models

# Create your models here.
class Car(models.Model):
    car_id = models.IntegerField( primary_key=True)
    license_plate = models.CharField(max_length=10)
    state = models.CharField(max_length=25)
    make = models.CharField(max_length=25)
    model = models.CharField(max_length=25)
    color = models.CharField(max_length=25)
    car_type = models.CharField(max_length=25)
    is_available = models.BooleanField(max_length=10)
    price = models.IntegerField(default= 0)
    store_id = models.IntegerField(default=0)


class Employee(models.Model):
    employee_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=25)
    store_id = models.IntegerField()
    currentlyworking = models.BooleanField(default=0)

class Store(models.Model):
    store_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=25)
    owner = models.CharField(max_length = 25)
    location = models.CharField(max_length= 25)
    number_of_sales = models.CharField(max_length= 25)


class Inventory(models.Model):
    store_id = models.IntegerField(default= 0)
    sedan_count = models.IntegerField(default= 0)
    suv_count = models.IntegerField(default= 0)
    truck_count = models.IntegerField(default= 0)


class Transaction(models.Model):
    transaction_id = models.IntegerField(primary_key= True)
    customer_id = models.IntegerField(default=0)
    employee_id = models.IntegerField(default = 0)
    start_date = models.DateField()
    end_date = models.DateField()
    cost = models.IntegerField(default= 0)
    car_id = models.IntegerField(default= 0)

class Customer(models.Model):
    customer_id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length= 25)
    age = models.IntegerField(default= 0)
    max_price = models.IntegerField(default= 0)
    car_type = models.CharField(max_length= 25)
