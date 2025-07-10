# semillassdc/urls.py
from django.urls import path
from . import views


app_main = 'sdcsemillas'

urlpatterns = [

#    path('', views.index, name='index'),  # Página principal
    path("lotes",views.lotes_list,name='lotes_list'),
    path('lotes/<int:pk>/', views.lotes_detail, name='lotes_detail'),
    path('lotes/new/', views.lotes_create, name='lotes_create'),
    path('lotes/<int:pk>/edit/', views.lotes_update, name='lotes_update'),
    path('lotes/<int:pk>/delete/', views.lotes_delete, name='lotes_delete'),

    path("variedades",views.variedades_list,name='variedades_list'),
    path('variedades/<int:pk>/', views.variedades_detail, name='variedades_detail'),
    path('variedades/new/', views.variedades_create, name='variedades_create'),
    path('variedades/<int:pk>/edit/', views.variedades_update, name='variedades_update'),
    path('variedades/<int:pk>/delete/', views.variedades_delete, name='variedades_delete'),

    path("conteoplantas/",views.conteoplantas_list,name='conteoplantas_list'),
    path('conteoplantas/<int:pk>/', views.conteoplantas_detail, name='conteoplantas_detail'),
    path('conteoplantas/new/', views.conteoplantas_create, name='conteoplantas_create'),
    path('conteoplantas/<int:pk>/edit/', views.conteoplantas_update, name='conteoplantas_update'),
    path('conteoplantas/<int:pk>/delete/', views.conteoplantas_delete, name='conteoplantas_delete'),
    
]