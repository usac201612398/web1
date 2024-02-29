from django.urls import path
from app1 import views


app_main ="app1"

urlpatterns = [
    path("homepage/", views.homepage, name="homepage"),
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_view, name="logout"),
#    path("about/",views.AboutView.as_view(),name='about'),
#    path("", views.index, name="index"),
#    path("json/random/",views.random_json,name='random_json'),
#    path("files/imagen/",views.transferir_archivos,name='transferir_archivos'),
#    path("mostrar/sensores/",views.mostrar_sensores,name='mostrar_sensores'),
#    path("ajax/ejemplo/",views.ajax_ejemplo,name='ajax_ejemplo'),
    path("iniciar/pedido/",views.vector_prueba,name='iniciar_pedido'),
    path("iniciar/pedido/completo",views.repuesta,name='respuesta'),
    path("iniciar/pedido/masivo",views.vector_prueba2,name='pedido_masivo'),
    path("iniciar/pedido/convencional/carrito",views.vector_prueba3,name='iniciar_pedido_conv_carrito'),
    path("iniciar/pedido/convencional",views.vector_prueba4,name='iniciar_pedido_conv_panel'),
    path("registro",views.registroPhoto,name='reconocimientof'),
    path("registro/consulta",views.consultaRegistros,name='registroConsulta'),
]
