# app1/management/commands/mqtt_listener.py
import time
import json
import paho.mqtt.client as mqtt
from django.core.management.base import BaseCommand
from app1.models import SensorData
import django
import os
MQTT_HOST = "10.111.112.4"
MQTT_PORT = 1883
MQTT_USER = "sdc-iot"
MQTT_PASS = "nuevacontraseña"
TOPIC = "esp32/temperature"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web1.settings")
django.setup()
class Command(BaseCommand):
    help = "Listener MQTT que guarda datos en la base de datos"

    def handle(self, *args, **options):
        def on_connect(client, userdata, flags, rc):
            print("Conectado a MQTT con código:", rc)
            client.subscribe(TOPIC)

        def on_message(client, userdata, msg):
            try:
                payload = msg.payload.decode()
                data = json.loads(payload)
                device_id = data.get("id")
                temp = float(data.get("temp"))
                hum = float(data.get("hum"))

                # Guardar en base de datos
                SensorData.objects.create(
                    device_id=device_id,
                    temperature=temp,
                    humidity=hum
                )
                print(f"Guardado: {device_id} T={temp} H={hum}")
            except Exception as e:
                print("Error procesando mensaje:", e)

        client = mqtt.Client()
        client.username_pw_set(MQTT_USER, MQTT_PASS)
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect(MQTT_HOST, MQTT_PORT, 60)
        client.loop_forever()
