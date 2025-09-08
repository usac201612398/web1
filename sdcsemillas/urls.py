# semillassdc/urls.py
from django.urls import path
from . import views


app_main = 'sdcsemillas'

urlpatterns = [

    path('', views.sdcsemillashomepage, name='sdcsemillas_home'),  # Página principal

    path("lotes",views.lotes_list,name='lotes_list'),
    path('lotes/<int:pk>/', views.lotes_detail, name='lotes_detail'),
    path('lotes/new/', views.lotes_create, name='lotes_create'),
    path('lotes/<int:pk>/edit/', views.lotes_update, name='lotes_update'),
    path('lotes/<int:pk>/delete/', views.lotes_delete, name='lotes_delete'),

    path("monitorear",views.consulta_list,name='consultas_list'),
    path('reporte-lote/<int:lote_id>/', views.reporte_lote, name='reporte_lote'),

    path("variedades",views.variedades_list,name='variedades_list'),
    path('variedades/<int:pk>/', views.variedades_detail, name='variedades_detail'),
    path('variedades/new/', views.variedades_create, name='variedades_create'),
    path('variedades/<int:pk>/edit/', views.variedades_update, name='variedades_update'),
    path('variedades/<int:pk>/delete/', views.variedades_delete, name='variedades_delete'),

    path("operarios",views.operarios_list,name='operarios_list'),
    path('operarios/<int:pk>/', views.operarios_detail, name='operarios_detail'),
    path('operarios/new/', views.operarios_create, name='operarios_create'),
    path('operarios/<int:pk>/edit/', views.operarios_update, name='operarios_update'),
    path('operarios/<int:pk>/delete/', views.operarios_delete, name='operarios_delete'),

    path("conteoplantas/",views.conteoplantas_list,name='conteoplantas_list'),
    path('conteoplantas/<int:pk>/', views.conteoplantas_detail, name='conteoplantas_detail'),
    path('conteoplantas/new/', views.conteoplantas_create, name='conteoplantas_create'),
    path('conteoplantas/<int:pk>/edit/', views.conteoplantas_update, name='conteoplantas_update'),
    path('conteoplantas/<int:pk>/delete/', views.conteoplantas_delete, name='conteoplantas_delete'),

    path("conteosemillas/",views.conteosemillas_list,name='conteosemillas_list'),
    path('conteosemillas/<int:pk>/', views.conteosemillas_detail, name='conteosemillas_detail'),
    path('conteosemillas/new/', views.conteosemillas_create, name='conteosemillas_create'),
    path('conteosemillas/<int:pk>/edit/', views.conteosemillas_update, name='conteosemillas_update'),
    path('conteosemillas/<int:pk>/delete/', views.conteosemillas_delete, name='conteosemillas_delete'),

    path("conteofrutos/",views.conteofrutos_list,name='conteofrutos_list'),
    path('conteofrutos/<int:pk>/', views.conteofrutos_detail, name='conteofrutos_detail'),
    path('conteofrutos/new/', views.conteofrutos_create, name='conteofrutos_create'),
    path('conteofrutos/<int:pk>/edit/', views.conteofrutos_update, name='conteofrutos_update'),
    path('conteofrutos/<int:pk>/delete/', views.conteofrutos_delete, name='conteofrutos_delete'),

    path("conteofrutosplan/",views.conteofrutosplan_list,name='conteofrutosplan_list'),
    path('conteofrutosplan/<int:pk>/', views.conteofrutosplan_detail, name='conteofrutosplan_detail'),
    path('conteofrutosplan/new/', views.conteofrutosplan_create, name='conteofrutosplan_create'),
    path('conteofrutosplan/<int:pk>/edit/', views.conteofrutosplan_update, name='conteofrutosplan_update'),
    path('conteofrutosplan/<int:pk>/delete/', views.conteofrutosplan_delete, name='conteofrutosplan_delete'),

    path("etapasdelote/",views.etapasdelote_list,name='etapasdelote_list'),
    path('etapasdelote/<int:pk>/', views.etapasdelote_detail, name='etapasdelote_detail'),
    path('etapasdelote/new/', views.etapasdelote_create, name='etapasdelote_create'),
    path('etapasdelote/<int:pk>/edit/', views.etapasdelote_update, name='etapasdelote_update'),
    path('etapasdelote/<int:pk>/delete/', views.etapasdelote_delete, name='etapasdelote_delete'),

    path("ccalidadpolen/",views.ccalidadpolen_list,name='ccalidadpolen_list'),
    path('ccalidadpolen/<int:pk>/', views.ccalidadpolen_detail, name='ccalidadpolen_detail'),
    path('ccalidadpolen/new/', views.ccalidadpolen_create, name='ccalidadpolen_create'),
    path('ccalidadpolen/<int:pk>/edit/', views.ccalidadpolen_update, name='ccalidadpolen_update'),
    path('ccalidadpolen/<int:pk>/delete/', views.ccalidadpolen_delete, name='ccalidadpolen_delete'),

    path("indexpolinizacion/",views.indexpolinizacion_list,name='indexpolinizacion_list'),
    path('indexpolinizacion/<int:pk>/', views.indexpolinizacion_detail, name='indexpolinizacion_detail'),
    path('indexpolinizacion/new/', views.indexpolinizacion_create, name='indexpolinizacion_create'),
    path('indexpolinizacion/<int:pk>/edit/', views.indexpolinizacion_update, name='indexpolinizacion_update'),
    path('indexpolinizacion/<int:pk>/delete/', views.indexpolinizacion_delete, name='indexpolinizacion_delete'),
    
    path("conteoflores/",views.conteoflores_list,name='conteoflores_list'),
    path('conteoflores/<int:pk>/', views.conteoflores_detail, name='conteoflores_detail'),
    path('conteoflores/new/', views.conteoflores_create, name='conteoflores_create'),
    path('conteoflores/<int:pk>/edit/', views.conteoflores_update, name='conteoflores_update'),
    path('conteoflores/<int:pk>/delete/', views.conteoflores_delete, name='conteoflores_delete'),
    
    path("controlcosecha/",views.controlcosecha_list,name='controlcosecha_list'),
    path('controlcosecha/<int:pk>/', views.controlcosecha_detail, name='controlcosecha_detail'),
    path('controlcosecha/new/', views.controlcosecha_create, name='controlcosecha_create'),
    path('controlcosecha/<int:pk>/edit/', views.controlcosecha_update, name='controlcosecha_update'),
    path('controlcosecha/<int:pk>/delete/', views.controlcosecha_delete, name='controlcosecha_delete'),

    path('api/lote/', views.obtener_datos_lote, name='obtener_datos_lote'),
    path('ajax/obtener-variedad/', views.obtener_variedad_relacionada, name='obtener_variedad'),
    path('api/empleado/', views.obtener_datos_empleado_post, name='obtener_datos_empleado_post'),
    path('obtener_semana_polinizacion/', views.obtener_semana_desde_polinizacion, name='obtener_semana_polinizacion'),
    path('obtener_semana_cosecha/', views.obtener_semana_desde_cosecha, name='obtener_semana_cosecha'),
    path('exportar/<str:nombre_modelo>/', views.exportar_excel_generico, name='exportar_excel_generico'),

    path("cosecha/",views.cosecha_list,name='cosecha_list'),
    path('cosecha/<int:pk>/', views.cosecha_detail, name='cosecha_detail'),
    path('cosecha/new/', views.cosecha_create, name='cosecha_create'),
    path('cosecha/<int:pk>/edit/', views.cosecha_update, name='cosecha_update'),
    path('cosecha/<int:pk>/delete/', views.cosecha_delete, name='cosecha_delete'),



]