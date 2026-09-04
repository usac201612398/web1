from django.contrib import admin
from django.urls import path
from mantenimiento import views
#from app1.views import *

app_main ="mantenimiento"

urlpatterns = [

    path("", views.Tablero.as_view(), name="tablero"),
    path("agenda/", views.Agenda.as_view(), name="agenda"),

    # Áreas
    path("areas/", views.AreaList.as_view(), name="area_list"),
    path("areas/nueva/", views.AreaCreate.as_view(), name="area_create"),
    path("areas/<int:pk>/editar/", views.AreaUpdate.as_view(), name="area_update"),
    path("areas/<int:pk>/eliminar/", views.AreaDelete.as_view(), name="area_delete"),

    # Máquinas
    path("maquinas/", views.MaquinaList.as_view(), name="maquina_list"),
    path("maquinas/nueva/", views.MaquinaCreate.as_view(), name="maquina_create"),
    path("maquinas/<int:pk>/", views.MaquinaDetail.as_view(), name="maquina_detail"),
    path("maquinas/<int:pk>/editar/", views.MaquinaUpdate.as_view(), name="maquina_update"),
    path("maquinas/<int:pk>/eliminar/", views.MaquinaDelete.as_view(), name="maquina_delete"),

    # Actividades
    path("actividades/", views.ActividadList.as_view(), name="actividad_list"),
    path("actividades/nueva/", views.ActividadCreate.as_view(), name="actividad_create"),
    path("actividades/<int:pk>/editar/", views.ActividadUpdate.as_view(), name="actividad_update"),
    path("actividades/<int:pk>/eliminar/", views.ActividadDelete.as_view(), name="actividad_delete"),

    # Programación
    path("programas/nuevo/", views.ProgramaCreate.as_view(), name="programa_create"),
    path("programas/<int:pk>/editar/", views.ProgramaUpdate.as_view(), name="programa_update"),
    path("programas/<int:pk>/eliminar/", views.ProgramaDelete.as_view(), name="programa_delete"),

    # Servicios
    path("servicios/", views.ServicioList.as_view(), name="servicio_list"),
    path("servicios/nuevo/", views.ServicioCreate.as_view(), name="servicio_create"),
    path("servicios/<int:pk>/", views.ServicioDetail.as_view(), name="servicio_detail"),
    path("servicios/<int:pk>/editar/", views.ServicioUpdate.as_view(), name="servicio_update"),
    path("servicios/<int:pk>/eliminar/", views.ServicioDelete.as_view(), name="servicio_delete"),

    # Exportación
    path("exportar/servicios.csv", views.exportar_servicios, name="exportar_servicios"),
    path("exportar/pendientes.csv", views.exportar_pendientes, name="exportar_pendientes"),
    
]