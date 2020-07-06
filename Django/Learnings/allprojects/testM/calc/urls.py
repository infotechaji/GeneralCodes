
from django.contrib import admin
from django.urls import path
from . import views # the views file is imported here

urlpatterns = [
    path('test', views.home,name='Index'),
]
