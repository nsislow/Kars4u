import webbrowser

from django.http import HttpResponse
from django.shortcuts import render
from .models import Car, Store, Inventory
import sqlite3


def index(request):
    if request.method == 'POST':
        state = request.POST.get("state")
        license_plate = request.POST["license plate"]
        make = request.POST["make"]
        model = request.POST["model"]
        color = request.POST["color"]
        car_type = request.POST["car type"]
        is_available = True

        car = Car(state=state, license_plate=license_plate, make=make, model=model, color=color, car_type=car_type,
                  is_available=True)
        car.save()
        return render(request, "insertCars.html")
    return render(request, "insertCars.html")


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
                if car_type == "all":
                    car_list = list(cursor.execute("""SELECT S.store_id, S.name, S.location, I.suv_count, I.sedan_count, 
                                                    I.truck_count 
                                                    FROM Kars4U_components_store as S left outer join 
                                                    Kars4U_components_inventory as I on S.store_id = I.store_id 
                                                    WHERE S.name = (?);""", [inventory_store_name]))
                cursor.close()



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
                    store_list_sales = list(cursor.execute("""Select * FROM Kars4U_components_store 
                                                            WHERE number_of_sales >= ?""", [amount_sales]))
                if over_under == "under":
                    store_list_sales = list(cursor.execute("""Select * FROM Kars4U_components_store 
                                                            WHERE number_of_sales < ?""", [amount_sales]))
                print(store_list_sales)



        return render(request, "storeInventoryReport.html")
    return render(request, "storeReport.html")


def storeInventoryReport(request):
    if request.methond == 'POST':
        return render(request, "storeInventoryReport.html")
    return render(request, "storeInventoryReport.html")
