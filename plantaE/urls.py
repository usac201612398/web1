from django.urls import path
from plantaE import views
#from app1.views import *

app_main ="plantaE"

urlpatterns = [
#    path("homepage/", views.homepage, name="homepage"),
#    path('logout/', views.logout_view, name='logout'),
    path("",views.plantaEhomepage,name='plantaE_home'),
    path('exportar_excel/', views.exportar_excel, name='exportar_excel'),
    path('ajax/load-dataUsuario/', views.load_dataUsuario, name='load_dataUsuario'),
    path('ajax/load-dataUsuario2/', views.load_dataUsuario2, name='load_dataUsuario2'),
    path('ajax/load-dataUsuario3/', views.load_dataUsuario3, name='load_dataUsuario3'),
    path('ajax/load-dataUsuario4/', views.load_dataUsuario4, name='load_dataUsuario4'),
    path('ajax/obtener-nombre-usuario/', views.obtener_nombre_usuario, name='obtener_nombre_usuario'),
    path('ajax/obtener-fecha-invFruta/', views.obtenerfecha_invFruta, name='obtenerfecha_invFruta'),
    path('ajax/obtener-llave-recepcion/', views.obtener_llave_recepcion, name='obtener_llave_recepcion'),
    path('ajax/load-ccalidadparam/', views.load_ccalidadparam, name='load_ccalidadparam'),
    path('ajax/load-ccalidadaux/', views.ccalidad_update_aux, name='load_ccalidad_update_aux'),
    path('ajax/guardar-plantilla/', views.guardar_plantilla, name='guardar_plantilla'),
    path('ajax/guardar-plantillaRio/', views.guardar_plantillaRio, name='guardar_plantillaRio'),
    path('ajax/guardar-plantillaValle/', views.guardar_plantillaValle, name='guardar_plantillaValle'),
    path('ajax/load-inventarioProdparam/', views.load_inventarioProdparam, name='load_inventarioProdparam'),
    path("pesos",views.pesos_list,name='pesos_list'),
    path('pesos/<int:pk>/', views.pesos_detail, name='pesos_detail'),
    path('pesos/<int:pk>/delete/', views.pesos_delete, name='pesos_delete'),
    path('salidasFruta/<int:pk>/', views.article_detail, name='salidasFruta_detail'),
    path("salidasFruta/cuadre",views.cuadrar_RioDia,name='salidasFruta_cuadre'),
    path("salidasFruta/cuadreValle",views.cuadrar_ValleDia,name='salidasFruta_cuadreValle'),
    path("salidasFruta",views.article_list,name='salidasFruta_list'),
    path("salidasFrutaValle",views.article_listValle,name='salidasFruta_listValle'),
    path('salidasFruta/new/', views.article_formPlantilla, name='salidasFruta_create'),
    path('salidasFruta/new/plantilla', views.article_create_plantilla, name='salidasFruta_create_plantilla'),
    path('salidasFruta/new/plantillaValle', views.article_create_plantillaValle, name='salidasFruta_create_plantillaValle'),
    path('salidasFruta/<int:pk>/edit/', views.article_update, name='salidasFruta_update'),
    path('salidasFruta/<int:pk>/delete/', views.article_delete, name='salidasFruta_delete'),
    path('salidasFruta/<int:pk>/delete/Valle', views.article_deleteValle, name='salidasFruta_deleteValle'),
    path("acumFruta",views.acumFruta_list,name='acumFruta_list'),
    path("acumFruta/Valle",views.acumFruta_list,name='acumFruta_listValle'),
    path('acumFruta/<int:pk>/', views.acumFruta_detail, name='acumFruta_detail'),
    path('acumFruta/new/', views.acumFruta_create, name='acumFruta_create'),
    path('acumFruta/<int:pk>/edit/', views.acumFruta_update, name='acumFruta_update'),
    path('acumFruta/<int:pk>/delete/', views.acumFruta_delete, name='acumFruta_delete'),
    path('acumFruta/consulta/', views.acumFruta_consulta, name='acumFruta_consulta'),
    path('acumFruta/consultaValle/', views.acumFruta_consultaValle, name='acumFruta_consultaValle'),
    path('recepcionesFruta/<int:pk>/edit/', views.recepciones_update, name='recepcionesFruta_update'),
    path("recepcionesFruta/process",views.procesarrecepcion,name='recepcionesFruta_process'),
    path("recepcionesFruta",views.recepciones_list,name='recepcionesFruta_list'),
    path("recepcionesFruta/reporteAcum",views.recepciones_reporteAcum,name='recepcionesFruta_reporteAcum'),
    path("recepcionesFruta/reporteAcumKgm2Orden",views.recepciones_reporteAcumKgm2Orden,name='recepcionesFruta_reporteAcumKgm2Orden'),
    path("salidasFrutaPublic/reporteAcum/semanal",views.recepciones_reporteAcumSemPublic,name='salidasFrutaPublic_reporteAcumSem'),
    path("recepcionesFruta/reporteAcum/semanal",views.recepciones_reporteAcumSem,name='recepcionesFruta_reporteAcumSem'),
    path("recepcionesFruta/reporteAcum/grafico",views.recepciones_reportecurva,name='recepcionesFruta_reportecurva'),
    path("salidasFrutaPublic/graficoPublic",views.recepciones_reportecurva2,name='recepcionesFruta_reportecurva2'),
    path("recepcionesFruta/reporteAcum/loadgrafico",views.graficas,name='load_grafico'),
    path("boletasFruta",views.boletas_list,name='boletasFruta_list'),
    path('recepcionesFruta/<int:pk>/', views.recepciones_detail, name='recepcionesFruta_detail'),
    path("ccalidad",views.ccalidad_list,name='ccalidad_list'),
    path('ccalidad/<int:pk>/', views.ccalidad_detail, name='ccalidad_detail'),
    path('ccalidad/new/', views.ccalidad_create, name='ccalidad_create'),
    path('ccalidad/<int:pk>/edit/', views.ccalidad_update, name='ccalidad_update'),
    path('ccalidad/<int:pk>/delete/', views.ccalidad_delete, name='ccalidad_delete'),
    path("inventarioProd/plantilla",views.inventarioProd_grabarplantilla,name='inventarioProd_grabar'),
    path("inventarioProd",views.inventarioProd_list,name='inventarioProd_list'),
    path('inventarioProd/<int:pk>/', views.inventarioProd_detail, name='inventarioProd_detail'),
    path('inventarioProd/new/', views.inventarioProd_create, name='inventarioProd_create'),
    path('inventarioProd/<int:pk>/delete/', views.inventarioProd_delete, name='inventarioProd_delete'),
    
]
