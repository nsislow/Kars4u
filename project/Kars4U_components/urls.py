from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('test1', views.index, name = "test"),
    path('addemployee/', views.addemployee, name = 'addemployee'),
    path('fireemployee/', views.fireemployee, name = 'fireemployee'),
    path('employeeWorking/', views.employeeWorking, name = 'employeeWorking'),
    path('viewEmployees/', views.viewEmployees, name = 'viewEmployees'),
    path('EmployeesPerStore/', views.employeeperstore, name = 'EmployeesPerStore'),
    path('manageEmployees/', views.manageEmployees, name = 'manageEmployees')
]

