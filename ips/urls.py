from django.contrib import admin
from django.urls import path
from ips import views
#from app1.views import *

app_main ="ips"

urlpatterns = [

    path('', views.index, name='index'),  # Página principal
    path('qr/save_qr/', views.save_qr, name='save_qr'),  # Ruta para guardar el QR
    path('qr/visualizar/', views.ips_visualizar, name='ips_visualizar'),  # Ruta para guardar el QR
    path('qr/visualizarall/', views.ips_visualizarall, name='ips_visualizarall'),  # Ruta para guardar el QR
    path('qr/<int:pk>/delete/', views.ips_borrar, name='ips_delete'),  # Ruta para guardar el QR
    path('qr/exportar_excel/', views.exportar_excel, name='ips_exportar'),  # Ruta para guardar el QR
    path('qr/<int:pk>/edit/', views.actualizar_registro, name='ips_actualizar'),  # Ruta para guardar el QR
    
]