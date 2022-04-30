from django.http import HttpResponse
from django.shortcuts import render
from .models import Employee
from .models import Store
from .models import Car, Transaction
import sqlite3
from django.utils.datastructures import MultiValueDictKeyError


def index(request):
    if request.method == 'POST' and request.POST["add or delete car"] == "add car" :
        state = request.POST.get("state")
        license_plate = request.POST.get("license_plate")
        make = request.POST.get("make")
        model = request.POST.get("model")
        color = request.POST.get("color")
        car_type = request.POST.get("car_type")
        is_available = True
        store_id = request.POST["store id"]
        car_type = car_type.title()
        car = Car(state = state, store_id = store_id, license_plate = license_plate, make = make, model = model, color = color, car_type = car_type, is_available = True)
        car.save()
        current_inven = Inventory.objects.filter(store_id = store_id).values('store_id').values_list('store_id')
            #print(current_inven[0][0])
        if len(current_inven) == 0:
                if car_type == "Sedan":
                    new_inventory = Inventory(store_id = store_id, sedan_count = 1, truck_count = 0, suv_count = 0)
                    new_inventory.save()
                if car_type == "Suv":
                    new_inventory = Inventory(store_id = store_id, sedan_count = 0, truck_count = 0, suv_count = 1)
                    new_inventory.save()
                if car_type == "Truck":
                    new_inventory = Inventory(store_id = store_id, sedan_count = 0, truck_count = 1, suv_count = 0)
                    new_inventory.save()
        else:
            if car_type == "Sedan":
                    old_count = Inventory.objects.filter(store_id = store_id).values('sedan_count').values_list('sedan_count')
                    old_count = old_count[0][0]
                    new_count = old_count + 1
                    Inventory.objects.filter(store_id = store_id).update(sedan_count= new_count)
            if car_type == "Suv":
                old_count = Inventory.objects.filter(store_id = store_id).values('suv_count').values_list('suv_count')
                old_count = old_count[0][0]
                new_count = old_count + 1
                Inventory.objects.filter(store_id = store_id).update(suv_count= new_count)
            if car_type == "Truck":
                    old_count = Inventory.objects.filter(store_id = store_id).values('truck_count').values_list('truck_count')
                    old_count = old_count[0][0]
                    new_count = old_count + 1
                    Inventory.objects.filter(store_id = store_id).update(truck_count= new_count)
    elif request.method == "POST" and request.POST["add or delete car"] == "delete car":
            car_id = request.POST["car id"]


            car_type = Car.objects.filter(car_id = car_id).values('car_type').values_list('car_type')
            store_id = Car.objects.filter(car_id = car_id).values('store_id').values_list('store_id')
            print(store_id)
            store_id = store_id[0][0]
            car_type= car_type[0][0]
            if car_type == "Sedan":
                old_count = Inventory.objects.filter(store_id=store_id).values('sedan_count').values_list('sedan_count')
                old_count = old_count[0][0]
                new_count = max(old_count -1, 0)
                Inventory.objects.filter(store_id = store_id).update(sedan_count = new_count)
            if car_type == "Suv":
                old_count = Inventory.objects.filter(store_id=store_id).values('suv_count').values_list('suv_count')
                old_count = old_count[0][0]
                new_count = max(old_count -1, 0)
                Inventory.objects.filter(store_id = store_id).update(suv_count = new_count)
            if car_type == "Truck":
                old_count = Inventory.objects.filter(store_id=store_id).values('truck_count').values_list('truck_count')
                old_count = old_count[0][0]
                new_count = max(old_count -1, 0)
                Inventory.objects.filter(store_id = store_id).update(truck_count = new_count)

            Car.objects.filter(car_id=car_id).delete()





            return render(request, "insertCars.html")
    return render(request, "insertCars.html")


def addemployee(request):
    data = Store.objects.all()
    stores = {"Stores": data}
    print(data)
    if request.method == 'POST':
        name = request.POST.get("Name")
        store_id = request.POST.get("Store_id")
        employee = Employee(name = name, store_id = store_id)
        employee.save()
    return render(request, "addemployee.html", stores)

def fireemployee(request):
    data = Employee.objects.all()
    employees = {"employees": data}
    if request.method == 'POST':
        employee_id = request.POST.get("employee_id")
        Employee.objects.filter(employee_id=employee_id).delete()
    return render(request, "fireemployee.html", employees)

def employeeWorking(request):
    data = Employee.objects.all()
    employees = {"employees": data}
    if request.method == 'POST':
        employee_id = request.POST.get("employee_id")
        instatus = request.POST.get("Clock In")
        outstatus = request.POST.get("Clock Out")
        employee = Employee.objects.get(employee_id = employee_id)
        if instatus:
            employee.currentlyworking = True
        if outstatus:
            employee.currentlyworking = False
        employee.save()
    return render(request, "employeeworking.html", employees)

def viewEmployees(request):
    storedata = Store.objects.all()
    global data
    if request.method == 'POST':
        store_id = request.POST.get("Store_id")
        data = Employee.objects.filter(store_id = store_id)
    else:
        data = Employee.objects.all()
    return render(request, "viewEmployees.html", {'employees': data, 'stores':storedata})

def manageEmployees(request):
    return render(request, "manageEmployees.html")

def employeeperstore(request):
    connection = sqlite3.connect("db.sqlite3")
    cursor = connection.cursor()
    data = list(cursor.execute("SELECT s.store_id, s.name, COUNT(e.employee_id) as 'Total Employees'"
                               "From Kars4U_components_store s Left JOIN Kars4U_components_employee e ON s.store_id = "
                               "e.store_id GROUP BY s.store_id, s.name;"))
    cursor.close()
    return render(request, "EmployeesPerStore.html", {'stores': data})

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
           


def car_reports(request):
    if request.method == 'POST':
            car_type = request.POST.get('car types')
            data = Car.objects.filter(car_type = car_type).values('make', 'model', 'color', 'car_type', 'license_plate', 'store_id')
    else:
            data = Car.objects.all()
    return render(request, "carReport.html", {"cars": data})
