# app1/management/commands/mqtt_listener.py

import os
import json
import ssl
import paho.mqtt.client as mqtt
from django.core.management.base import BaseCommand
from app1.models import SensorData

MQTT_HOST = "a4810e38lk0oy-ats.iot.us-east-1.amazonaws.com"
MQTT_PORT = 8883
TOPIC = "casa/planta01/data"

class Command(BaseCommand):
    help = "Listener MQTT que guarda datos en la base de datos"

    def handle(self, *args, **options):

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

        ca = os.path.join(BASE_DIR, "AmazonRootCA1.pem")
        cert = os.path.join(BASE_DIR, "cert.pem.crt")
        key = os.path.join(BASE_DIR, "private.pem.key")

        def on_connect(client, userdata, flags, rc):
            print("Conectado a AWS IoT con código:", rc)
            client.subscribe(TOPIC)

        def on_message(client, userdata, msg):
            try:
                payload = msg.payload.decode()
                print("Mensaje recibido:", payload)

                data = json.loads(payload)

                planta_id = data.get("planta_id")
                temperatura = float(data.get("hum_amb"))
                hum_aire = float(data.get("hum_amb"))
                hum_suelo = float(data.get("hum_suelo"))
                peso = float(data.get("peso"))

                m1Sensoresdata.objects.create(
                    planta_id=planta_id,
                    temperatura=temperatura,
                    humedad_aire=hum_aire,
                    humedad_suelo=hum_suelo,
                    peso=peso,
                )


            except Exception as e:
                print("Error procesando mensaje:", e)

        client = mqtt.Client()

        client.tls_set(
            ca_certs=ca,
            certfile=cert,
            keyfile=key,
            tls_version=ssl.PROTOCOL_TLSv1_2
        )

        client.on_connect = on_connect
        client.on_message = on_message

        client.connect(MQTT_HOST, MQTT_PORT, 60)
        client.loop_forever()
