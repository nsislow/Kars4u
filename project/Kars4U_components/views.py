from django.http import HttpResponse
from django.shortcuts import render
from .models import Car, Inventory


def index(request):
    if request.method == 'POST' and request.POST["add or delete car"] == "add car" :
        state = request.POST.get("state")
        license_plate = request.POST["license plate"]
        make = request.POST["make"]
        model = request.POST["model"]
        color = request.POST["color"]
        car_type = request.POST["car type"]
        is_available = True
        store_id = request.POST["store id"]
        car_type = car_type.title()
        car = Car(state = state, store_id = store_id, license_plate = license_plate, make = make, model = model, color = color, car_type = car_type, is_available = True)
        car.save()

        # inventory_update = Inventory(sedan_count = 0, truck_count = 0, suv_count = 0, store_id = 0)
        # inventory_update.save()
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

def test1(request):
    return (HttpResponse("Hellooooadfsasfdo"))

def car_reports(request):
    if request.method == 'POST':
        car_type = request.POST.get('car types')
        data = Car.objects.filter(car_type = car_type).values('make', 'model', 'color', 'car_type', 'license_plate', 'store_id')
    else:
        data = Car.objects.all()
    return render(request, "carReport.html", {"cars": data})


    #return HttpResponse("Hello Runtime Terror!")
