from django.urls import path
from iotappweb import views
#from app1.views import *

app_main ="iotappweb"

urlpatterns = [
    path("homepage/", views.homepage, name="homepage"),
    path("iot/accion",views.enviarinstruccion,name='enviarinstruccion'),
    path("planta/",views.plantadashboard,name='plantadashboard'),
    path('api/planta/', views.planta_api, name='planta_api'),
    path('tanque/', views.tanquedashboard, name='tanquedashboard'),
    path('api/tanque/', views.tanque_api, name='tanque_api'),
    path('riegos/historial', views.historial_riegos, name='riegoshistorial'),
    path('consumo/', views.consumo_acumulado, name='consumo_acumulado'),
    path('api/histograma/', views.histograma_api, name='histograma_api'),
    path('aranet-data/', views.aranet_webhook, name='aranet-data'),       # POST desde el sensor
    path('aranet-live/', views.aranet_live_page, name='aranet-live'),  # template HTML
    path('aranet-resumen/', views.aranet_resumen_page, name='aranet_resumen_page'),  # template HTML
    
    path('aranet-resumen-json/', views.aranet_resumen_json, name='aranet_resumen_json'),
    path('aranet-data-json/', views.aranet_data_json, name='aranet_data_json'),
]
