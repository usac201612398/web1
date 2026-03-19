from django.urls import re_path
from .consumers import AranetConsumer

websocket_urlpatterns = [
    re_path(r'ws/sensor_data/$', AranetConsumer.as_asgi()),  # La URL del WebSocket
]