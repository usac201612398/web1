from django.urls import path
from app1 import views
#from app1.views import *

app_main ="iotappweb"

urlpatterns = [
    path("homepage/", views.homepage, name="homepage"),
    path("iot/accion",views.enviarinstruccion,name='enviarinstruccion'),
    path("iot/sensor",views.dashboard,name='sensor'),

]
