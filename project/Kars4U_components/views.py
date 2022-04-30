from asyncio.windows_events import NULL
from django.http import HttpResponse
from django.shortcuts import render
from .models import Car
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
            minPrice = NULL
        
        try:
            maxPrice = request.POST["maxPrice"]
        except MultiValueDictKeyError:
            maxPrice = NULL

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
        return render(request,"customerReport.html", {"customerData": request_list})
        
        
    return render(request,"customerReport.html")
