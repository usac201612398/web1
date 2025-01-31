# tu_aplicacion/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class SensorDataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Aquí puedes agregar la lógica de autenticación si es necesario
        self.room_name = 'sensor_data'
        self.room_group_name = 'sensor_data_group'

        # Unirse a un grupo de WebSocket
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Dejar el grupo de WebSocket
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Recibir un mensaje desde WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        sensor_value = text_data_json['value']

        # Enviar el mensaje a todos los clientes conectados
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'sensor_data',
                'value': sensor_value
            }
        )

    # Recibir mensaje desde el grupo
    async def sensor_data(self, event):
        sensor_value = event['value']

        # Enviar el mensaje WebSocket al cliente
        await self.send(text_data=json.dumps({
            'value': sensor_value
        }))
