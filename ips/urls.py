from django.contrib import admin
from django.urls import path
from ips import views
#from app1.views import *

app_main ="ips"

urlpatterns = [

    path('', views.index, name='index'),  # Página principal
    path('save_qr/', views.save_qr, name='save_qr'),  # Ruta para guardar el QR
    path('visualizar/', views.ips_visualizar, name='ips_visualizar'),  # Ruta para guardar el QR
    path('eliminar/', views.ips_borrar, name='ips_delete'),  # Ruta para guardar el QR
    path('exportar_excel/', views.exportar_excel, name='ips_exportar'),  # Ruta para guardar el QR
    
]