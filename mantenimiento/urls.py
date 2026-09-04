from django.contrib import admin
from django.urls import path
from mantenimiento import views
#from app1.views import *

app_main ="mantenimiento"

urlpatterns = [

    path('', views.index, name='index'),  # Login
    
    path('home/', views.home, name='home'),  # Página principal
    
]