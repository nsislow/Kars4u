from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('test1', views.index, name = "test"),
    path('transaction', views.transaction, name='transaction'),
    path('transaction/report', views.transaction_report, name='transaction_report'),
    path('customerRequest', views.customerRequest, name='customerRequest'),
    path('customerReport', views.customerReport, name='customerReport')
]
