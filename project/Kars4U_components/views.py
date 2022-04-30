import sqlite3
from django.http import HttpResponse
from django.shortcuts import render
from .models import Car, Transaction


def index(request):
    if request.method == 'POST':
        state = request.POST.get("state")
        license_plate = request.POST["license plate"]
        make = request.POST["make"]
        model = request.POST["model"]
        color = request.POST["color"]
        car_type = request.POST["car type"]
        is_available = True

        car = Car(state = state, license_plate = license_plate, make = make, model = model, color = color, car_type = car_type, is_available = True)
        car.save()


    #return HttpResponse("Hello Runtime Terror!")
    return render(request,"insertCars.html")

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
