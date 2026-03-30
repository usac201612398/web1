from django.urls import path
from plantaE import views
from .view.boletas_views import *
from .view.recepciones_views import *
from .view.actpeso_views import *
from .view.itemsenvios_views import *
from .view.itemsprodterm_views import *
from .view.ccalidad_views import *
from .view.envioslocal_views import *
from .view.contenedores_views import *
from .view.controlcajas_views import *
from .view.pedidoscarreta_views import *
from .view.supervisioncultivos_views import *
from .view.supervisionfito_views import *
from .view.salidasfruta_views import *
from .view.cargacontenedor_views import *
from .view.inventarioprodterm_views import *
from .view.acumfruta_views import *
from .view.reportetecnicos_views import *
from .view.reportegerencial_views import *

from .view.inventarioprodtermaux_views import *
from .view.home_views import *

#from app1.views import *

app_main ="plantaE"

urlpatterns = [
#    path("homepage/", views.homepage, name="homepage"),
#    path('logout/', views.logout_view, name='logout'),

    #Urls de home
    path("",views.plantaEhomepage,name='plantaE_home'),
    path("gerencial/",views.plantaEhomepageger,name='plantaE_homeger'),

    #Urls de ajax
    path('ajax/load-dataUsuario/', views.load_dataUsuario, name='load_dataUsuario'),
    path('ajax/load-dataUsuario2/', views.load_dataUsuario2, name='load_dataUsuario2'),
    path('ajax/load-dataUsuario3/', views.load_dataUsuario3, name='load_dataUsuario3'),
    path('ajax/load-dataUsuario4/', views.load_dataUsuario4, name='load_dataUsuario4'),
    path('ajax/load-dataUsuario5/', views.load_dataUsuario5, name='load_dataUsuario5'),
    path('ajax/load-dataUsuario6/', views.load_dataUsuario6, name='load_dataUsuario6'),
    path('ajax/load-dataUsuario7/', views.load_dataUsuario7, name='load_dataUsuario7'),
    path('ajax/load-dataUsuario8/', views.load_dataUsuario8, name='load_dataUsuario8'),
    path('ajax/load-dataUsuario9/', views.load_dataUsuario9, name='load_dataUsuario9'),
    path('ajax/obtener-nombre-usuario/', views.obtener_nombre_usuario, name='obtener_nombre_usuario'),
    path('ajax/obtener-fecha-invFruta/', views.obtenerfecha_invFruta, name='obtenerfecha_invFruta'),
    path('ajax/guardar-plantilla/', views.guardar_plantilla, name='guardar_plantilla'),
    path('ajax/guardar-plantillaRio/', views.guardar_plantillaRio, name='guardar_plantillaRio'),
    path('ajax/guardar-plantillaValle/', views.guardar_plantillaValle, name='guardar_plantillaValle'),
    path('ajax/load-inventarioProdparam/', views.load_inventarioProdparam, name='load_inventarioProdparam'),
    path('api/ordenes/', views.get_ordenes_por_finca, name='api_ordenes_por_finca'),
    path('api/estructuras/', views.get_estructuras_por_orden, name='api_estructuras_por_orden'),
    path('api/variedad/', views.get_variedades_por_estructura, name='api_variedades_por_estructura'),
    path('api/ordenes2/', views.get_ordenes_por_finca2, name='api_ordenes_por_finca2'),
    path('api/estructuras2/', views.get_estructuras_por_orden2, name='api_estructuras_por_orden2'),
    path('api/variedad2/', views.get_variedades_por_estructura2, name='api_variedades_por_estructura2'),
    
    #Urls de recepciones
    path('recepcionesFruta',RecepcionesListView.as_view(),name='recepcionesFruta_list'),
    path('recepcionesFruta/<int:pk>/delete/', RecepcionesFrutaDeleteView.as_view(), name='recepcionesFruta_delete'),
    path('recepcionesFruta/<int:pk>/', RecepcionesDetailView.as_view(), name='recepcionesFruta_detail'),
    path('recepcionesFruta/<int:pk>/edit/', RecepcionesUpdateView.as_view(), name='recepcionesFruta_update'),

    #Urls de boletas
    path('boletasFruta',BoletasListView.as_view(),name='boletasFruta_list'),
    path('boletasFruta/<int:pk>/edit/', BoletasUpdateView.as_view(), name='boletas_update'),
    path('boletasFruta/<int:pk>/', BoletasDetailView.as_view(), name='boletas_detail'),
    path('boletasFruta/<int:pk>/delete/', BoletasDeleteView.as_view(), name='boletas_delete'),
    path('boletasFruta/<int:pk>/devolver/', BoletasDevolverView.as_view(), name='boletas_devolver'),
    path("boletasFruta/productor",BoletasListProductorView.as_view(),name='boletasFruta_listproductor'),
    
    #Urls de actpeso
    path("pesos",PesosListView.as_view(),name='pesos_list'),
    path('pesos/<int:pk>/', PesosDetailView.as_view(), name='pesos_detail'),
    path('pesos/<int:pk>/delete/', PesosDeleteView.as_view(), name='pesos_delete'),

    #Urls de itemsprodterm
    path("items",ItemsListView.as_view(),name='items_list'),
    path('items/new/', ItemsCreateView.as_view(), name='items_create'),
    path('items/<int:pk>/edit/', ItemsUpdateView.as_view(), name='items_update'),
    path('items/<int:pk>/delete/', ItemsDeleteView.as_view, name='items_delete'),

    #Urls de itemsenvios
    path("itemsenvios",ItemsEnviosListView.as_view(),name='itemsenvios_list'),
    path('itemsenvios/new/', ItemsEnviosCreateView.as_view(), name='itemsenvios_create'),
    path('itemsenvios/<int:pk>/edit/', ItemsEnviosUpdateView.as_view(), name='itemsenvios_update'),
    path('itemsenvios/<int:pk>/delete/', ItemsEnviosDeleteView.as_view(), name='itemsenvios_delete'),

    #Urls de ccalidad
    path("ccalidad",CcalidadListView.as_view(),name='ccalidad_list'),
    path('ccalidad/<int:pk>/', CcalidadDetailView.as_view(), name='ccalidad_detail'),
    path('ccalidad/new/', CcalidadCreateView.as_view(), name='ccalidad_create'),
    path('ccalidad/<int:pk>/edit/', CcalidadUpdateView.as_view(), name='ccalidad_update'),
    path('ccalidad/<int:pk>/delete/', CcalidadDeleteView.as_view(), name='ccalidad_delete'),
    #Ajax de ccalidad
    path('ajax/load-ccalidadaux/', CcalidadUpdateAuxView.as_view(), name='load_ccalidad_update_aux'),
    path('ajax/load-ccalidadparam/', LoadCcalidadParamView.as_view(), name='load_ccalidadparam'),
    path('ajax/obtener-llave-recepcion/', ObtenerLlaveRecepcionView.as_view(), name='obtener_llave_recepcion'),

    #Urls de enviolocal
    path("envioslocal",views.EnviosLocalListView.as_view(),name='envioslocal_list'),
    path('envioslocal/<int:pk>/delete/', EnviosLocalDeleteView.as_view(), name='envioslocal_delete'),
    path('envioslocal/<int:pk>/', views.EnviosLocalDetailView.as_view(), name='envioslocal_detail'),
    path('envioslocal/<int:pk>/edit/', EnviosLocalUpdateView.as_view(), name='envioslocal_update'),

    #Urls de contenedores
    path("contenedores",ContenedoresListView.as_view(),name='contenedores_list'),
    path("contenedores2",ContenedoresListView2.as_view(),name='contenedores_list2'),
    path('contenedores/new/', ContenedoresCreateView.as_view(), name='contenedores_create'),
    path('contenedores/<int:pk>/edit/', ContenedoresUpdateView.as_view(), name='contenedores_update'),
    path('contenedores2/<int:pk>/edit/', ContenedoresUpdateView2.as_view(), name='contenedores_update2'),
    path('contenedores/<int:pk>/delete/',ContenedoresDeleteView.as_view(), name='contenedores_delete'),

    #Urls de controlcajas
    path("controlcajasmanual",ControlCajasListView.as_view(),name='controlcajas_list'),
    path("controlcajasmanualinventario",ControlCajasInventarioView.as_view(),name='controlcajas_inventario'),
    path('controlcajasmanual/new/', ControlCajasCreateView.as_view(), name='controlcajas_create'),
    path('controlcajasmanual/<int:pk>/edit/', ControlCajasUpdateView.as_view(), name='controlcajas_update'),
    path('controlcajasmanual/<int:pk>/delete/', ControlCajasDeleteView.as_view(), name='controlcajas_delete'),
    #Ajax
    path('ajax/obtener-item/', ObtenerItemsRelacionadosView.as_view(), name='obtener_items'),

    #Urls de pedidocarreta
    path('pedidos/<int:pk>/delete/', PedidosDeleteView.as_view(), name='pedidos_delete'),
    path('pedidos/<int:pk>/cancel/', PedidosCancelView.as_view(), name='pedidos_cancel'),
    path("pedidos",PedidosListView.as_view(),name='pedidos_list'),
    path("pedidos/historico",PedidosHistoricoView.as_view(),name='pedidos_list_historico'),
    path('pedidos/new/plantilla', PedidosCarretaView.as_view(), name='create_pedidos'),
    path('pedidos/<int:pk>/edit/', PedidosUpdateView.as_view(), name='pedidos_update'),
    #Ajax
    path('ajax/guardar-pedido/', GuardarPedidoView.as_view(), name='guardar_pedido'),

    #Urls de supervisioncultivos
    path("supervision/<int:pk>/delete/",views.supervision_delete,name='supervision_delete'),
    path("supervision",views.supervision_list,name='supervision_list'),
    path('supervision/new/', views.supervision_create, name='supervision_create'),
    path("supervision/plantilla",views.supervision_grabar,name='supervision_grabar'),
    path("supervisionproduccion/plantilla",views.supervisionproduccion_grabar,name='supervisionproduccion_grabar'),
    path('supervisiontomates/new/', views.supervisiontomates_create, name='supervisiontomates_create'),
    path('supervisionchiles/new/', views.supervisionchiles_create, name='supervisionchiles_create'),
    path("supervisionproduccion",views.supervisionproduccion_list,name='supervisionproduccion_list'),
    path("supervisionproduccion/<int:pk>/delete/",views.supervisionproduccion_delete,name='supervisionproduccion_delete'),
    path('supervisionproduccion/detalle/<str:fecha>/<str:cultivo>/<str:estructura>/<str:zona>/<str:finca>/',views.supervisionproduccion_detalle,name='supervisionproduccion_detalle'),
    path('supervisionproducion/reporte-semanal/', views.reporte_semanal_supervision,name='reporte_semanal_supervision'),
    path('supervisionproduccion/reporte-semanal/view',views.reporte_semanal_view,name='reporte_semanal_view'),
    path('supervisionproduccion/reporte-general/',views.reporte_general,name='reporte_general_supervision'),
    path('supervisionproduccion/reporte-semanal/seguimiento',views.reporte_semanal_seguimiento,name='reporte_semanal_seguimiento'),
    path('supervisionproduccion/reporte-semanal/detalleseguimiento',views.reporte_seguimiento_api,name='reporte_seguimiento_api'),
    
    #Urls de supervisionfito
    path('supervisionfitotomatescob/new/', views.supervisionfitotomatescob_create, name='supervisionfitotomatescob_create'),
    path('supervisionfitotomatestizon/new/', views.supervisionfitotomatestizon_create, name='supervisionfitotomatestizon_create'),
    path("supervisionfito",views.supervisionfito_list,name='supervisionfito_list'),
    path("supervisionfito/<int:pk>/delete/",views.supervisionfito_delete,name='supervisionfito_delete'),
    path('supervisionfito/detalle/<str:fecha>/<str:cultivo>/<str:estructura>/<str:zona>/<str:finca>/',views.supervisionfito_detalle,name='supervisionfito_detalle'), 
    path('supervisionfito/reporte-general/',views.reporte_general_fito,name='reporte_general_supervision_fito'),
    path('supervisionfito/reporte-semana/detalleseguimiento',views.reporte_seguimiento_api,name='reporte_seguimiento_api_fito'),
    path('supervisionfito/reporte-semanal/', views.reporte_semanal_supervision_fito,name='reporte_semanal_supervision_fito'),
    path("supervisionfito/plantilla",views.supervisionfito_grabar,name='supervisionfito_grabar'),
    
    path('supervisionfito/reporte-semanal/view',views.reporte_semanal_view_fito,name='reporte_semanal_view_fito'),
    path('supervisionfito/reporte-semanal/seguimiento',views.reporte_semanal_seguimiento_fito,name='reporte_semanal_seguimiento_fito'),
    
    #Urls de salidasfruta
    path('salidasFruta/<int:pk>/', views.article_detail, name='salidasFruta_detail'),
    path('salidasFruta2/<int:pk>/', views.salidasFruta_detail2, name='salidasFruta_detail2'),
    path("salidasFruta/cuadre",views.cuadrar_RioDia,name='salidasFruta_cuadre'),
    path("salidasFruta/cuadreValle",views.cuadrar_ValleDia,name='salidasFruta_cuadreValle'),
    path("salidasFrutaView",views.salidasFruta_list,name='salidasFruta_list2'),
    path("salidasFruta",views.article_list,name='salidasFruta_list'),
    path("salidasFrutaValle",views.article_listValle,name='salidasFruta_listValle'),
    path('ajax/get_correos/', views.get_correos_por_encargado, name='get_correos_por_encargado'),
    path('salidasFruta2/new/', views.article_create, name='salidasFruta_create2'),
    path('salidasFruta/new/', views.article_formPlantilla, name='salidasFruta_create'),
    path('salidasFruta/new/plantilla', views.article_create_plantilla, name='salidasFruta_create_plantilla'),
    path('salidasFruta/new/plantillaValle', views.article_create_plantillaValle, name='salidasFruta_create_plantillaValle'),
    path('salidasFruta/<int:pk>/edit/', views.article_update, name='salidasFruta_update'),
    path('salidasFruta/<int:pk>/delete/', views.article_delete, name='salidasFruta_delete'),
    path('salidasFruta2/<int:pk>/delete/', views.article_delete2, name='salidasFruta_delete2'),
    path('salidasFruta/<int:pk>/delete/Valle', views.article_deleteValle, name='salidasFruta_deleteValle'),
    
    #Urls de inventarioprodterm
    path("inventarioProd/plantilla",views.inventarioProd_grabarplantilla,name='inventarioProd_grabar'),
    path("inventarioProd",views.inventarioProd_list,name='inventarioProd_list'),
    path("inventarioProd2",views.inventarioProd_list2,name='inventarioProd_list2'),
    path('inventarioProd/<int:pk>/', views.inventarioProd_detail, name='inventarioProd_detail'),
    path('inventarioProd/new/', views.inventarioProd_create, name='inventarioProd_create'),
    path('inventarioProd/<int:pk>/edit/', views.inventarioProd_update, name='inventarioProd_update'),
    path('inventarioProd/<int:pk>/delete/', views.inventarioProd_delete, name='inventarioProd_delete'),
    path('inventarioProd2/<int:pk>/edit/', views.inventarioProd_update2, name='inventarioProd_update2'),
    path('inventarioProd2/<int:pk>/delete/', views.inventarioProd_delete2, name='inventarioProd_delete2'),
    path('inventarioProd/reporteInv', views.reporteInventario, name='reporte_inventario'),

    #Urls de inventarioprodterm
    path("inventarioProdAux",views.inventarioProdAux_list,name='inventarioProdAux_list'),
    path('inventarioProdAux/<int:pk>/edit/', views.inventarioProdAux_update, name='inventarioProdAux_update'),
    path('inventarioProdAux/<int:pk>/delete/', views.inventarioProdAux_delete, name='inventarioProdAux_delete'),

    #Urls de cargacontenedor
    path("inventarioProd/cargacontenedor",views.cargacontenedores_list,name='inventarioProd_contenlist'),
    path("inventarioProd/cargacontenedorv2",views.cargacontenedores_listv2,name='inventarioProd_contenlistv2'),
    path("inventarioProd/packinglist",views.contenedorpacking_list,name='inventarioProd_packinglist'),
    path("inventarioProd/packinglist_detail",views.contenedorpacking_list_detail,name='inventarioProd_packinglist_detail'),
    path('inventarioProd/packinglist_detail/<int:pk>/edit/', views.packinglist_update, name='inventarioProd_packinglist_update'),
    path('inventarioProd/packinglist_detail/<int:pk>/delete/', views.packinglist_delete, name='inventarioProd_packinglist_delete'),
    path('inventarioProd/validaroventa', views.validaroventa, name='inventarioProd_validaroventa'),
    path('ajax/load-contenedores/', views.load_contenedores, name='load_contenedores'),
    path('generate_packing_list_pdf/', views.generate_packing_list_pdf, name='generate_packing_list_pdf'),
    path('generate_packing_list_pdf2/', views.generate_packing_list_pdf2, name='generate_packing_list_pdf2'),
    path("inventarioProd/process/",views.procesarinvprodconten,name='inventarioProd_contprocess'),
    path("inventarioProd/processv2/",views.procesarinvprodcontenv2,name='inventarioProd_contprocessv2'),

    #Urls de Acumfruta
    path("acumFrutaView",views.acumFruta_list2,name='acumFruta_list2'),
    path("acumFruta",views.acumFruta_list,name='acumFruta_list'),
    path("acumFruta/Valle",views.acumFruta_list,name='acumFruta_listValle'),
    path('acumFruta/<int:pk>/', views.acumFruta_detail, name='acumFruta_detail'),
    path('acumFruta2/<int:pk>/', views.acumFruta_detail2, name='acumFruta_detail2'),
    path('acumFruta/new/', views.acumFruta_create, name='acumFruta_create'),
    path('acumFruta/<int:pk>/edit/', views.acumFruta_update, name='acumFruta_update'),
    path('acumFruta/<int:pk>/delete/', views.acumFruta_delete, name='acumFruta_delete'),
    path('acumFruta2/<int:pk>/delete/', views.acumFruta_delete2, name='acumFruta_delete2'),
    path('acumFruta/consulta/', views.acumFruta_consulta, name='acumFruta_consulta'),
    path('acumFruta/consultaValle/', views.acumFruta_consultaValle, name='acumFruta_consultaValle'),

    #Urls de reportes gerencial
    path("boletasFruta/reporterecepcion",views.boletas_reporterecepcion,name='boletasFruta_reporterecepcion'),
    path("boletasFruta/reportetraza",views.boletas_reportetraza,name='boletasFruta_reportetraza'),
    path("boletasFruta/reportetrazaexpo",views.boletas_reportetrazaexpo,name='boletasFruta_reportetrazaexpo'),
    path("boletasFruta/trazarecepcion",views.boletas_trazarecepcion,name='boletasFruta_trazarecepcion'),
    path("boletasFruta/constanciatrazarecepcion",views.boletas_constanciatrazarecepcion,name='boletasFruta_constanciatrazarecepcion'),
    path("boletasFruta/constanciatraza",views.boletas_constanciatraza,name='boletasFruta_constanciatraza'),
    path("boletasFruta/constanciatrazaexpo",views.boletas_constanciatrazarexpo,name='boletasFruta_constanciatrazaexpo'),
    path("boletasFruta/constanciarecepcion",views.boletas_constanciarecepcion,name='boletasFruta_constanciarecepcion'),
    
    path("inventarioProd/inventariogeneral",views.inventariogeneral_list,name='inventarioProd_inventariogeneral'),
    path("inventarioProd/inventariogeneralger",views.inventariogeneralger_list,name='inventarioProd_inventariogeneralger'),
    path("gerencial/reportedemermas",views.reporte_mermas_view,name='gerencial_reportedemermas'),
    path("gerencial/graficocontenedores",views.contenedores_grafico_view,name='gerencial_graficocontenedores'),
    path("inventarioProd/inventariogeneralfruta",views.inventariogeneralfruta_list,name='inventarioProd_inventariogeneralfruta'),
    path('inventarioProd/reportesemanalprodterm_pivot', views.semanalprodterm_pivot, name='reporte_reportesemanalprodterm_pivot'),
    path('reporte-pivote/', views.reporte_tabla_pivote, name='reporte_tabla_pivote'),
    path('dashboard/', views.dashboard_acumfruta, name='dashboard_acumfruta'),
    path('dashboardkgxm2/', views.dashboard_acumfrutakgxm2, name='dashboard_acumfrutakgxm2'),
    path('salidasFruta/consultaaprovechamientos', views.poraprovechamientos, name='salidasFruta_aprovechamietos'),
    path('salidasFruta/consultaaprovechamientosger', views.poraprovechamientosger, name='salidasFruta_aprovechamietosger'),
    path('salidasFruta/consultaaprovechamientosempger', views.poraprovechamientosempger, name='salidasFruta_aprovechamietosempger'),
    path('salidasFruta/consultaaprovechamientosemp', views.poraprovechamientosemp, name='salidasFruta_poraprovechamietosemp'),
    path('salidasFruta/consultaaprovechamientosempgersem', views.kgm2_semanal_aprovechamiento, name='salidasFruta_aprovechamietosempgersem'),
    path("recepcionesFruta/reporteAcum/loadgrafico",views.graficas,name='load_grafico'),

    #Urls de reportetecnicos
    path('exportar_excel/', views.exportar_excel, name='exportar_excel'),
    path('dashboard/tecnicos', views.dashboard_tecnicos, name='dashboard_acumfruta2'),
    path('inventarioProd/reportesemanalprodterm_pivot_productor', views.semanalprodterm_pivot_productor, name='reporte_reportesemanalprodterm_pivot_productor'),
    path("recepcionesFruta/reporteAcum",views.recepciones_reporteAcum,name='recepcionesFruta_reporteAcum'),
    path("recepcionesFruta/reporteAcumKgm2Orden",views.recepciones_reporteAcumKgm2Orden,name='recepcionesFruta_reporteAcumKgm2Orden'),
    path("recepcionesFruta/reporteAcumKgm2Estruc",views.recepciones_reporteAcumKgm2Estruc,name='recepcionesFruta_reporteAcumKgm2Estruc'),  
    path("recepcionesFruta/reporteAcumKgm2Variedad",views.recepciones_reporteAcumKgm2Variedad,name='recepcionesFruta_reporteAcumKgm2Variedad'),
    path("recepcionesFruta/reporteAcum/semanal",views.recepciones_reporteAcumSem,name='recepcionesFruta_reporteAcumSem'),
    path("salidasFrutaPublic/reporteAcum/semanal",views.recepciones_reporteAcumSemPublic,name='salidasFrutaPublic_reporteAcumSem'),
    path("recepcionesFruta/reporteAcum/grafico",views.recepciones_reportecurva,name='recepcionesFruta_reportecurva'),
    path("salidasFrutaPublic/graficoPublic",views.recepciones_reportecurva2,name='recepcionesFruta_reportecurva2'),
    path('reporte-pivote/tecnicos', views.reporte_tabla_pivote2, name='reporte_tabla_pivote2'),
    path('reporte-pivote/produccionsem', views.reporte_tabla_pivote_produccionsem, name='reporte_tabla_pivote_produccionsem'),
    path("inventarioProd/aprovechamientos",views.aprovechamientos,name='inventarioProd_aprovechamientos'),
    
]

'''
    path("boletasFruta",views.boletas_list,name='boletasFruta_list'),
    path('boletasFruta/<int:pk>/edit/', views.boletas_update, name='boletas_update'),
    path('boletasFruta/<int:pk>/', views.boletas_detail, name='boletas_detail'),
    path('boletasFruta/<int:pk>/delete/', views.boletas_delete, name='boletas_delete'),
    path('boletasFruta/<int:pk>/devolver/', views.boletas_devolver, name='boletas_devolver'),
    path("boletasFruta/productor",views.boletas_listproductor,name='boletasFruta_listproductor'),
'''