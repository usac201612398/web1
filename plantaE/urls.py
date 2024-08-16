from django.urls import path
from plantaE import views
#from app1.views import *

app_main ="plantaE"

urlpatterns = [
#    path("homepage/", views.homepage, name="homepage"),
#    path('logout/', views.logout_view, name='logout'),
    path("",views.article_list,name='salidasFruta_list'),
    path('ajax/load-dataUsuario/', views.load_dataUsuario, name='load_dataUsuario'),
    path('ajax/load-dataUsuario2/', views.load_dataUsuario2, name='load_dataUsuario2'),
    path('ajax/obtener-nombre-usuario/', views.obtener_nombre_usuario, name='obtener_nombre_usuario'),
    path('ajax/obtener-llave-recepcion/', views.obtener_llave_recepcion, name='obtener_llave_recepcion'),
    path('ajax/load-ccalidadparam/', views.load_ccalidadparam, name='load_ccalidadparam'),
    path('ajax/load-ccalidadaux/', views.ccalidad_update_aux, name='load_ccalidad_update_aux'),
    path('salidasFruta/<int:pk>/', views.article_detail, name='salidasFruta_detail'),
    path('salidasFruta/new/', views.article_create, name='salidasFruta_create'),
    path('salidasFruta/<int:pk>/edit/', views.article_update, name='salidasFruta_update'),
    path('salidasFruta/<int:pk>/delete/', views.article_delete, name='salidasFruta_delete'),
    path('recepcionesFruta/<int:pk>/edit/', views.recepciones_update, name='recepcionesFruta_update'),
    path("recepcionesFruta",views.recepciones_list,name='recepcionesFruta_list'),
    path('recepcionesFruta/<int:pk>/', views.recepciones_detail, name='recepcionesFruta_detail'),
    path("ccalidad",views.ccalidad_list,name='ccalidad_list'),
    path('ccalidad/<int:pk>/', views.ccalidad_detail, name='ccalidad_detail'),
    path('ccalidad/new/', views.ccalidad_create, name='ccalidad_create'),
    path('ccalidad/<int:pk>/edit/', views.ccalidad_update, name='ccalidad_update'),
    path('ccalidad/<int:pk>/delete/', views.ccalidad_delete, name='ccalidad_delete'),
    
]
