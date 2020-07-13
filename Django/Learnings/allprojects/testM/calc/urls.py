
from django.contrib import admin
from django.urls import path
from . import views # the views file is imported here

urlpatterns = [
    path('', views.home,name='Index'),
    path('test-template', views.home_template,name='Template-Index'),
    path('test-template-dy', views.home_template_dynamic,name='Template-Index-DYM'),
    path('add', views.add,name='add'),
]
