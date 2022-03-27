from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('test1', views.index, name = "test"),
]

