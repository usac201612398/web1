# iotappweb/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class AranetConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("aranet_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("aranet_group", self.channel_name)

    async def aranet_message(self, event):
        await self.send(text_data=json.dumps(event["message"]))