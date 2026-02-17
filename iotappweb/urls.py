from django.urls import path
from iotappweb import views
#from app1.views import *

app_main ="iotappweb"

urlpatterns = [
    path("homepage/", views.homepage, name="homepage"),
    path("iot/accion",views.enviarinstruccion,name='enviarinstruccion'),
    path("iot/sensor",views.dashboard,name='sensor'),
    path('api/sensores/', views.sensor_api, name='sensor_api'),


]
