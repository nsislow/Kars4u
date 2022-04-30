from django.http import HttpResponse
from django.shortcuts import render
from .models import Car, Transaction
import sqlite3
from django.utils.datastructures import MultiValueDictKeyError

def index(request):
    if request.method == 'POST':
        state = request.POST.get("state")
        license_plate = request.POST.get("license_plate")
        make = request.POST.get("make")
        model = request.POST.get("model")
        color = request.POST.get("color")
        car_type = request.POST.get("car_type")
        is_available = True

        car = Car(state = state, license_plate = license_plate, make = make, model = model, color = color, car_type = car_type, is_available = True)
        car.save()

    return render(request,"insertCars.html")

def customerRequest(request):
    return render(request,"customerRequest.html")

def customerReport(request):
    if request.method == 'POST':
        store = request.POST.get("store")
        isAvailable = request.POST.get("is_available")

        if isAvailable == 'on':
            isAvailable = True
        else:
            isAvailable == False

        try:
            minPrice = request.POST["minPrice"]
        except MultiValueDictKeyError:
            minPrice = None

        try:
            maxPrice = request.POST["maxPrice"]
        except MultiValueDictKeyError:
            maxPrice = None

        #assume min and max price are null as default
        query = """
            SELECT * FROM Kars4U_components_car
            WHERE (?) = store_id AND (?) = is_available;
            """
        data = (store, isAvailable)

        if minPrice == '' and maxPrice != '':
            query = """
            SELECT * FROM Kars4U_components_car
            WHERE (?) = store_id AND (?) = is_available AND (?) >= price;
            """
            data = (store, isAvailable, maxPrice)
        elif minPrice != '' and maxPrice == '':
            query = """
            SELECT * FROM Kars4U_components_car
            WHERE (?) = store_id AND (?) = is_available AND (?) <= price;
            """
            data = (store, isAvailable, minPrice)
        elif minPrice != '' and maxPrice != '':
            query = """
            SELECT * FROM Kars4U_components_car
            WHERE (?) = store_id AND (?) = is_available AND (?) <= price AND (?) >= price;
            """
            data = (store, isAvailable, maxPrice, minPrice)

        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        request_list = list(cursor.execute(query, data))
        print(request_list)
        return render(request,"customerReport.html", {"request_list": request_list})


    return render(request,"customerReport.html")

def transaction(request):

    if request.method == 'POST':
        employee_id = request.POST.get("employee_id")
        customer_id = request.POST["customer_id"]
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]
        car_id = request.POST["car_id"]
        cost = request.POST["cost"]

        transaction = Transaction(employee_id = employee_id, customer_id = customer_id, start_date = start_date,
        end_date = end_date, car_id = car_id, cost =  cost)
        car = Car.objects.get(car_id = car_id)
        if (car != None):
            car.price = cost
        print(transaction)
        transaction.save()
    return render(request,"newTransaction.html")

def transaction_report(request):

    if request.method == 'POST':
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        date_query = """SELECT e.name, cust.name, c.make, c.model, c.color, c.car_type, c.license_plate, t.cost
        FROM Kars4U_components_transaction t left outer join Kars4U_components_employee e on e.employee_id = t.employee_id
        left outer join Kars4U_components_customer cust on cust.customer_id = t.customer_id
        left outer join Kars4U_components_car c on c.car_id = t.car_id
        WHERE (?) <= t.start_date AND (?) >= end_date;
        """
        data = (start_date, end_date)
        transaction_list = list(cursor.execute(date_query, data))
        print(transaction_list)
        return render(request,"transactionReport.html", {"transaction_list": transaction_list})


    return render(request,"transactionReport.html")