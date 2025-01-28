from django.contrib import admin
from django.urls import path
from scorevalle import views
#from app1.views import *

app_main ="scorevalle"

urlpatterns = [

    path('', views.index, name='index'),  # Página principal
    
    path('ajax/obtener-nombre-usuario-scoresdc/', views.obtener_nombre_usuario_scoresdc, name='obtener_nombre_usuario_scoresdc'),
    
    path('ajax/guardar-scorecosecha/', views.guardar_score, name='guardar_score'),
    path('scoremanejo', views.scorecosecha_, name='scorevalle_cosecha'),
    path('scorecosecha', views.scoremanejo_, name='scorevalle_manejo'),

    path('<int:pk>/edit/', views.actualizar_scorepersonal, name='scorepersonal_update'),  # Ruta para guardar el QR
    path('scoremanejo/<int:pk>/edit/', views.actualizar_scoremanejo, name='scoremanejo_update'),
    path('scorecosecha/<int:pk>/edit/', views.actualizar_scorecosecha, name='scorecosecha_update'),

]