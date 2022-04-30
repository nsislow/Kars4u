from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('test1', views.index, name = "test"),
    path('customerRequest', views.customerRequest, name='customerRequest'),
    path('customerReport', views.customerReport, name='customerReport')
]

