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
    path('crud/gestor/ubicacion/<int:pk>/delete/', views.ubicaciones_delete, name='ubicaciones_delete'),

    # ======================================================
    # MAQUINAS
    # ======================================================

    path(
        "crud/gestor/maquina/",
        views.maquinas_list,
        name="maquinas_list"
    ),

    path(
        "crud/gestor/maquina/new/",
        views.maquinas_create,
        name="maquinas_create"
    ),

    path(
        "crud/gestor/maquina/<int:pk>/edit/",
        views.maquinas_update,
        name="maquinas_update"
    ),

    path(
        "crud/gestor/maquina/<int:pk>/delete/",
        views.maquinas_delete,
        name="maquinas_delete"
    ),

    # ======================================================
    # CENTRODECOSTO
    # ======================================================

    path(
        "crud/gestor/centrodecosto/",
        views.centrodecosto_list,
        name="centrodecosto_list"
    ),

    path(
        "crud/gestor/centrodecosto/new/",
        views.centrodecosto_create,
        name="centrodecosto_create"
    ),

    path(
        "crud/gestor/centrodecosto/<int:pk>/edit/",
        views.centrodecosto_update,
        name="centrodecosto_update"
    ),

    path(
        "crud/gestor/centrodecosto/<int:pk>/delete/",
        views.centrodecosto_delete,
        name="centrodecosto_delete"
    ),

    # ======================================================
    # USUARIOS
    # ======================================================

    path(
        "crud/gestor/personal/",
        views.personal_list,
        name="personal_list"
    ),

    path(
        "crud/gestor/personal/new/",
        views.personal_create,
        name="personal_create"
    ),

    path(
        "crud/gestor/personal/<int:pk>/edit/",
        views.personal_update,
        name="personal_update"
    ),

    path(
        "crud/gestor/personal/<int:pk>/delete/",
        views.personal_delete,
        name="personal_delete"
    ),

    # ======================================================
    # CATALOGO DE MANTENIMIENTOS
    # ======================================================

    path(
        "crud/gestor/listamantenimientos/",
        views.listamantenimientos_list,
        name="listamantenimientos_list"
    ),

    path(
        "crud/gestor/listamantenimientos/new/",
        views.listamantenimientos_create,
        name="listamantenimientos_create"
    ),

    path(
        "crud/gestor/listamantenimientos/<int:pk>/edit/",
        views.listamantenimientos_update,
        name="listamantenimientos_update"
    ),

    path(
        "crud/gestor/listamantenimientos/<int:pk>/delete/",
        views.listamantenimientos_delete,
        name="listamantenimientos_delete"
    ),

]