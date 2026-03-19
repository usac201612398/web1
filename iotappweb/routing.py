# iotappweb/routing.py
from django.urls import re_path
from .consumers import AranetConsumer

websocket_urlpatterns = [
    re_path(r'ws/aranet/$', AranetConsumer.as_asgi()),
]