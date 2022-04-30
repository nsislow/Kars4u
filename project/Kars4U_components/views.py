import webbrowser

from django.http import HttpResponse
from django.shortcuts import render
from .models import Employee, Inventory
from .models import Store
from .models import Car, Transaction, Customer
import sqlite3
from django.utils.datastructures import MultiValueDictKeyError

def home(request):
    return render(request, "home.html")


def index(request):
    if request.method == 'POST' and request.POST["add or delete car"] == "add car" :
        state = request.POST.get("state")
        license_plate = request.POST.get("license_plate")
        make = request.POST.get("make")
        model = request.POST.get("model")
        color = request.POST.get("color")
        car_type = request.POST.get("car_type1")
        print(car_type)
        is_available = True
        store_id = request.POST["store_id"]
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
        car_id1 = request.POST["car_id"]
        cost = request.POST["cost"]

        transaction = Transaction(employee_id = employee_id, customer_id = customer_id, start_date = start_date,
        end_date = end_date, car_id = car_id1, cost =  cost)
        transaction.save()

        car = Car.objects.get(car_id = car_id1)
        if (car != None):
            car.price = cost
        car.save()
        print(transaction)
        
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
            car_type = request.POST.get('car_type')
            data = Car.objects.filter(car_type = car_type).values('make', 'model', 'color', 'car_type', 'license_plate', 'store_id')
    else:
            data = Car.objects.all()
    return render(request, "carReport.html", {"cars": data})

def store(request):
    if request.method == 'POST':
        # add information
        if request.POST.get("Add"):
            store_name = request.POST.get("store name")
            owner = request.POST["owner"]
            location = request.POST["location"]

            store_name = store_name.title()
            owner = owner.title()
            location = location.title()

            store_add = Store(name=store_name, owner=owner, location=location, number_of_sales=0)
            store_add.save()

        # update information
        if request.POST.get("Update"):
            update_store_id = request.POST.get("store_id")
            update_item = request.POST.get("update")
            new_info = request.POST.get("new_info")

            update_store_id = update_store_id.title()
            update_item = update_item.title()
            new_info = new_info.title()

            store_list = Store.objects.filter(store_id=update_store_id).values("store_id").values_list("store_id")
            if (len(store_list) != 0):
                store_to_update = Store.objects.get(store_id=update_store_id)

                if update_item == "Name":
                    store_to_update.name = new_info
                elif update_item == "Location":
                    store_to_update.location = new_info
                elif update_item == "Owner":
                    store_to_update.owner = new_info
                store_to_update.save()
        # remove information
        if request.POST.get("Remove"):
            remove_store_id = request.POST.get("store_id2")
            remove_list = Store.objects.filter(store_id=remove_store_id).values("store_id").values_list("store_id")
            if (len(remove_list) != 0):
                store_to_remove = Store.objects.get(store_id=remove_store_id)
                store_to_remove.delete()

        return render(request, "store.html")
    return render(request, "store.html")


def storeReport(request):
    if request.method == 'POST':
        # inventory
        if request.POST.get("inventory"):
            inventory_store_name = request.POST.get("name")
            inventory_store_name.title()

            store_inventory_list = Store.objects.filter(name=inventory_store_name).values("name").values_list("name")
            if len(store_inventory_list) != 0:
                conn = sqlite3.connect('db.sqlite3')
                cursor = conn.cursor()
                car_type = request.POST.get("car type")
                if car_type == "truck":
                    car_list = list(cursor.execute("""SELECT S.store_id, S.name, S.location, I.truck_count 
                                                   FROM Kars4U_components_store as S left outer join 
                                                   Kars4U_components_inventory as I on S.store_id = I.store_id 
                                                   WHERE S.name = (?);""", [inventory_store_name]))
                if car_type == "suv":
                    car_list = list(cursor.execute("""SELECT S.store_id, S.name, S.location, I.suv_count 
                                                    FROM Kars4U_components_store as S left outer join 
                                                    Kars4U_components_inventory as I on S.store_id = I.store_id 
                                                    WHERE S.name = (?);""", [inventory_store_name]))
                if car_type == "sedan":
                    car_list = list(cursor.execute("""SELECT S.store_id, S.name, S.location, I.sedan_count 
                                                    FROM Kars4U_components_store as S left outer join 
                                                    Kars4U_components_inventory as I on S.store_id = I.store_id 
                                                    WHERE S.name = (?);""", [inventory_store_name]))


                car_list_copy = {"stores": car_list}
                return render(request, "storeInventoryReport.html", car_list_copy)


        # under or over given number of sales
        if request.POST.get("amount"):
            amount_sales = request.POST.get("sales")
            amount_sales = int(amount_sales)
            if amount_sales >= 0:
                over_under = request.POST.get("update")
                conn = sqlite3.connect('db.sqlite3')
                cursor = conn.cursor()
                store_list_sales = "error has occurred"
                if over_under == "over":
                    store_list_sales = list(cursor.execute("""Select name, number_of_sales FROM Kars4U_components_store 
                                                            WHERE number_of_sales >= ?""", [amount_sales]))
                if over_under == "under":
                    store_list_sales = list(cursor.execute("""Select name, number_of_sales FROM Kars4U_components_store 
                                                            WHERE number_of_sales < ?""", [amount_sales]))

            store_list_copy = {"sales": store_list_sales}
            return render(request, "over_under_num_sales.html", store_list_copy)
        #owner of stores
        if request.POST.get("owner"):
            owner_name = request.POST.get("owner name")
            owner_name.title()
            conn = sqlite3.connect('db.sqlite3')
            cursor = conn.cursor()

            stores_with_owner = list(cursor.execute("""Select name, owner, number_of_sales FROM Kars4U_components_store 
                                                                        WHERE owner == ?""", [owner_name]))
            stores_copy = {"sales": stores_with_owner}
            return render(request, "StoresByOwner.html", stores_copy)

        #stores in same location
        if request.POST.get("location"):
            location_name = request.POST.get("location name")
            location_name.title()
            storeData = Store.objects.all()
            data = Store.objects.filter(location=location_name)
            return render(request, "StoresByLocation.html", {'location': data, 'store': storeData})


    return render(request, "storeReport.html")


def storeInventoryReport(request):
    if request.methond == 'POST':
        return render(request, "storeInventoryReport.html")
    return render(request, "storeInventoryReport.html")
def overUnderNumSales(request):
    if request.methond == 'POST':
        return render(request, "over_under_num_sales.html")
    return render(request, "over_under_num_sales.html")
def storesByOwner(request):
    if request.methond == 'POST':
        return render(request, "StoresByOwner.html")
    return render(request, "StoresByOwner.html")
def storesByLocation(request):
    if request.methond == 'POST':
        return render(request, "StoresByLocation.html")
    return render(request, "StoresByLocation.html")
