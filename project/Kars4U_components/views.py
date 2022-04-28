from django.http import HttpResponse
from django.shortcuts import render
from .models import Car
from .models import Employee
from .models import Store


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


def addemployee(request):
    data = Store.objects.all()
    stores = {"Stores": data}
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
