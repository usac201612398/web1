"""
ASGI config for web1 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import re_path
from plantaE import consumers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web1.settings')

application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            re_path(r'ws/sensor_data/$', consumers.SensorDataConsumer.as_asgi()),  # URL WebSocket
        ])
    ),
})
