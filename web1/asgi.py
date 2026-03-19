import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from iotappweb.routing import websocket_urlpatterns  # Asegúrate de importar las URLs del WebSocket
import django

# Establecer la configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web1.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Maneja solicitudes HTTP tradicionales
    "websocket": AuthMiddlewareStack(  # Asegúrate de usar AuthMiddlewareStack para autenticar WebSockets si es necesario
        URLRouter(websocket_urlpatterns)  # Aquí conectamos las rutas WebSocket
    ),
})
