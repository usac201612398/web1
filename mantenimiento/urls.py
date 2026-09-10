from django.contrib import admin
from django.urls import path
from mantenimiento import views
#from app1.views import *

app_main ="mantenimiento"

urlpatterns = [

    path("", views.index, name="tablero"),
    
    path("crud/gestor/ubicacion/",views.ubicaciones_list,name='ubicaciones_list'),
    path('crud/gestor/ubicacion/new/', views.ubicaciones_create, name='ubicaciones_create'),
    path('crud/gestor/ubicacion/<int:pk>/edit/', views.ubicaciones_update, name='ubicaciones_update'),
    path('crud/gestor/ubicacion/<int:pk>/delete/', views.ubicaciones_confirm_delete, name='ubicaciones_delete'),
    
]