from django.urls import path
from app1 import views
#from app1.views import *

app_main ="app1"

urlpatterns = [
    path("homepage/", views.homepage, name="homepage"),
#    path("login/", views.login_page, name="login"),
#    path("logout/", views.LogoutView.as_view(), name="logout"),
    path('logout/', views.logout_view, name='logout'),
    path('ajax/load-dataUsuario-rf/', views.load_dataUsuario_rf, name='load_dataUsuario_rf'),
    path('ajax/obtener-nombre-usuario-rf/', views.obtener_nombre_usuario_rf, name='obtener_nombre_usuario_rf'),
#    path('logout-complete/', views.logout_complete, name='logout_complete'),  # Puedes crear una vista personalizada para confirmar el logout si lo deseas
#    path("about/",views.AboutView.as_view(),name='about'),
#    path("", views.index, name="index"),
#    path("json/random/",views.random_json,name='random_json'),
#    path("files/imagen/",views.transferir_archivos,name='transferir_archivos'),
#    path("mostrar/sensores/",views.mostrar_sensores,name='mostrar_sensores'),
#    path("ajax/ejemplo/",views.ajax_ejemplo,name='ajax_ejemplo'),
#    path("iniciar/pedido/",views.vector_prueba,name='iniciar_pedido'),
#    path("iniciar/pedido/completo",views.repuesta,name='respuesta'),
#    path("iniciar/pedido/masivo",views.vector_prueba2,name='pedido_masivo'),
#    path("iniciar/pedido/convencional/carrito",views.vector_prueba3,name='iniciar_pedido_conv_carrito'),
#    path("iniciar/pedido/convencional",views.vector_prueba4,name='iniciar_pedido_conv_panel'),
    path("registro",views.registroPhotoMejorado,name='reconocimientof'),
    path("registro/confirmacion",views.almacenarIdentidadConfirmada,name='confirmacionrecfacial'),
    path("registro/consulta",views.consultaRegistros,name='registroConsulta'),
#    path("registro/consultaR",views.consultarR.as_view(), name = 'registroConsulta'),
    path('exportar_excel/', views.exportar_excel, name='exportar_excel'),
    
    path("iot/accion",views.enviarinstruccion,name='enviarinstruccion'),
    path("iot/sensor",views.dashboard,name='sensor'),
]
