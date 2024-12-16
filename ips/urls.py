from django.contrib import admin
from django.urls import path
from ips import views
#from app1.views import *

app_main ="ips"

urlpatterns = [

    path('', views.index, name='index'),  # Página principal
    path('save_qr/', views.save_qr, name='save_qr'),  # Ruta para guardar el QR
]