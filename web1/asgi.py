import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import re_path
from plantaE import consumers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web1.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter([
            re_path(r'ws/sensor_data/$', consumers.SensorDataConsumer.as_asgi()),
        ])
    ),
})
