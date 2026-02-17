from django.urls import path
from iotappweb import views
#from app1.views import *

app_main ="iotappweb"

urlpatterns = [
    path("homepage/", views.homepage, name="homepage"),
    path("iot/accion",views.enviarinstruccion,name='enviarinstruccion'),
    path("planta/",views.plantadashboard,name='plantadashboard'),
    path('api/sensores/', views.sensor_api, name='sensor_api'),
    path('tanque/', views.tanquedashboard, name='tanquedashboard'),
    path('api/tanque/', views.tanque_api, name='tanque_api'),

]
