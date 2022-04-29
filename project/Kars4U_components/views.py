from django.http import HttpResponse
from django.shortcuts import render
from .models import Car


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

def customerRequest(request):
    return HttpResponse("yoooooooooooooooo")
