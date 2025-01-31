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

        # Aceptar la conexión WebSocket
        await self.accept()

    async def disconnect(self, close_code):
        # Dejar el grupo de WebSocket cuando el cliente se desconecte
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Recibir un mensaje desde WebSocket (mensaje del cliente)
    async def receive(self, text_data):
        try:
            # Cargar los datos recibidos en formato JSON
            text_data_json = json.loads(text_data)
            
            # Obtener el valor del sensor
            sensor_value = text_data_json.get('value', None)  # Usamos `get` para evitar errores si no existe la clave
            
            if sensor_value is not None:
                # Enviar el mensaje a todos los clientes conectados al grupo
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'sensor_data',  # El tipo de mensaje
                        'value': sensor_value   # Los datos del sensor
                    }
                )
            else:
                print("Error: El campo 'value' no fue encontrado en los datos recibidos.")
        except json.JSONDecodeError:
            # Si no se puede decodificar el JSON, imprimir error
            print("Error: No se pudo decodificar el mensaje JSON.")
        except Exception as e:
            # Si ocurre otro error, mostrar el mensaje de error
            print(f"Error inesperado: {e}")

    # Recibir mensaje desde el grupo (y enviarlo al WebSocket del cliente)
    async def sensor_data(self, event):
        # Obtener el valor del sensor del mensaje del grupo
        sensor_value = event['value']

        # Enviar el valor del sensor al cliente WebSocket
        await self.send(text_data=json.dumps({
            'value': sensor_value  # Enviar los datos del sensor al cliente
        }))
