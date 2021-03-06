from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cars', views.index, name='index'),
    path('test1', views.index, name = "test"),
    path('addemployee/', views.addemployee, name = 'addemployee'),
    path('fireemployee/', views.fireemployee, name = 'fireemployee'),
    path('employeeWorking/', views.employeeWorking, name = 'employeeWorking'),
    path('viewEmployees/', views.viewEmployees, name = 'viewEmployees'),
    path('EmployeesPerStore/', views.employeeperstore, name = 'EmployeesPerStore'),
    path('manageEmployees/', views.manageEmployees, name = 'manageEmployees'),
    path('transaction', views.transaction, name='transaction'),
    path('transaction/report', views.transaction_report, name='transaction_report'),
    path('customerRequest', views.customerRequest, name='customerRequest'),
    path('customerReport', views.customerReport, name='customerReport'),
    path('car_reports/', views.car_reports, name = "car_reports"),
    path('store', views.store, name="store"),
    path('storeReport', views.storeReport, name="storeReport"),
    path('storeInventoryReport', views.storeInventoryReport, name="storeInventoryReport"),
    path('over_under_num_sales', views.overUnderNumSales, name="over_under_num_sales"),
    path('StoresByOwner', views.storesByOwner, name="StoresByOwner"),
    path('StoresByLocation', views.storesByLocation, name="StoresByLocation")
]
