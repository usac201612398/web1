# app1/management/commands/mqtt_listener.py

import os
import json
import ssl
import paho.mqtt.client as mqtt
from django.core.management.base import BaseCommand
from iotappweb.models import m1Sensoresdata
from django.conf import settings

#MQTT_HOST = "a4810e38lk0oy-ats.iot.us-east-1.amazonaws.com"
#MQTT_PORT = 8883
MQTT_PORT = 1883
MQTT_HOST = "10.111.112.4"
MQTT_USER = "sdc-iot"
MQTT_PASS = "nuevacontraseña"
TOPIC = "casa/planta01/data"

class Command(BaseCommand):
    help = "Listener MQTT que guarda datos en la base de datos"

    def handle(self, *args, **options):

        #BASE_DIR = settings.BASE_DIR

        #ca = os.path.join(BASE_DIR, "certs/AmazonRootCA1.pem")
        #cert = os.path.join(BASE_DIR, "certs/cert.pem.crt")
        #key = os.path.join(BASE_DIR, "certs/private.pem.key")

        def on_connect(client, userdata, flags, rc):
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
        '''
        client.tls_set(
            ca_certs=ca,
            certfile=cert,
            keyfile=key,
            tls_version=ssl.PROTOCOL_TLSv1_2
        )
        ''' 
        client.username_pw_set(MQTT_USER, MQTT_PASS)
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect(MQTT_HOST, MQTT_PORT, 60)
        client.loop_forever()
