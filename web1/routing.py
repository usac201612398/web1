from django.urls import re_path
from . import consumers

# Enrutamiento de WebSockets
websocket_urlpatterns = [
    re_path(r'ws/sensor_data/$', consumers.SensorDataConsumer.as_asgi()),  # URL para el WebSocket
]
