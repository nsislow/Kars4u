from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('store', views.store, name="store"),
    path('storeReport', views.storeReport, name="storeReport"),
    path('storeInventoryReport', views.storeInventoryReport, name="storeInventoryReport")
]

