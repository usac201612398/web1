from django.contrib import admin
from django.urls import path
from scorevalle import views
#from app1.views import *

app_main ="scorevalle"

urlpatterns = [

    path('', views.index, name='index'),  # Página principal
    
]