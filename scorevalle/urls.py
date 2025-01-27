from django.contrib import admin
from django.urls import path
from scorevalle import views
#from app1.views import *

app_main ="scorevalle"

urlpatterns = [

    path('', views.index, name='index'),  # Página principal
    
    path('ajax/obtener-nombre-usuario-scoresdc/', views.obtener_nombre_usuario_scoresdc, name='obtener_nombre_usuario_scoresdc'),
    
    path('ajax/guardar-scorecosecha/', views.guardar_score, name='guardar_score'),
    path('scoremanejo', views.scorecosecha, name='guardar_scorecosecha'),
    path('scorecosecha/', views.scoremanejo, name='guardar_scorecosecha'),
]