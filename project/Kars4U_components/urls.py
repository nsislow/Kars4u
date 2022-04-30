from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('store', views.store, name="store"),
    path('storeReport', views.storeReport, name="storeReport"),
    path('storeInventoryReport', views.storeInventoryReport, name="storeInventoryReport"),
    path('over_under_num_sales', views.overUnderNumSales, name="over_under_num_sales"),
    path('StoresByOwner', views.storesByOwner, name="StoresByOwner"),
    path('StoresByLocation', views.storesByLocation, name="StoresByLocation")
]

