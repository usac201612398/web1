import json
from channels.generic.websocket import AsyncWebsocketConsumer

class AranetConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Este método es llamado cuando se realiza una conexión WebSocket."""
        # Se puede usar `self.scope` para manejar conexiones por grupos o usuarios
        self.room_group_name = "aranet_data"

        # Unirse a un grupo para enviar datos a todos los clientes conectados
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Aceptar la conexión WebSocket
        await self.accept()

    async def disconnect(self, close_code):
        """Este método es llamado cuando se cierra la conexión WebSocket."""
        # Salir del grupo
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """Este método es llamado cuando recibimos un mensaje del cliente."""
        # Aquí podemos procesar lo que recibimos o simplemente enviarlo a todos los usuarios
        data = json.loads(text_data)
        
        # Reenviar el mensaje a todos los miembros del grupo (puedes modificar según tu lógica)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'sensor_data',  # El tipo de mensaje que vamos a manejar
                'data': data  # Los datos recibidos
            }
        )

    async def sensor_data(self, event):
        """Este método es llamado cuando el WebSocket recibe un mensaje desde el grupo."""
        data = event['data']

        # Enviar mensaje a WebSocket del cliente
        await self.send(text_data=json.dumps({
            'sensor': data['sensor'],
            'timestamp': data['timestamp'],
            'metric': data['metric'],
            'value': data['value'],
        }))