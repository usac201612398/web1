# app1/management/commands/mqtt_listener.py

import os
import json
import ssl
import paho.mqtt.client as mqtt
from django.core.management.base import BaseCommand
from iotappweb.models import m1Sensoresdata, m2Sensoresdata, riegoRegistro
from django.conf import settings

#MQTT_HOST = "a4810e38lk0oy-ats.iot.us-east-1.amazonaws.com"
#MQTT_PORT = 8883
MQTT_PORT = 1883
MQTT_HOST = "10.111.112.4"
MQTT_USER = "sdc-iot"
MQTT_PASS = "nuevacontraseña"
TOPIC_PLANTA = "casa/planta01/data"
TOPIC_TANQUE = "casa/tanque01/data"

class Command(BaseCommand):
    help = "Listener MQTT que guarda datos en la base de datos"

    def handle(self, *args, **options):

        #BASE_DIR = settings.BASE_DIR

        #ca = os.path.join(BASE_DIR, "certs/AmazonRootCA1.pem")
        #cert = os.path.join(BASE_DIR, "certs/cert.pem.crt")
        #key = os.path.join(BASE_DIR, "certs/private.pem.key")

        def on_connect(client, userdata, flags, rc):
            client.subscribe(TOPIC_PLANTA)
            client.subscribe(TOPIC_TANQUE)

        def on_message(client, userdata, msg):

            try:
                payload = msg.payload.decode()
                print("Mensaje recibido en", msg.topic, ":", payload)
                data = json.loads(payload)

                if msg.topic == TOPIC_PLANTA:
                    # Guardar datos de planta
                    m1Sensoresdata.objects.create(
                        planta_id=data.get("planta_id"),
                        temperatura=float(data.get("temp_amb", 0)),
                        humedad_aire=float(data.get("hum_amb", 0)),
                        humedad_suelo=float(data.get("hum_suelo", 0)),
                        peso=float(data.get("peso", 0)),
                    )
                elif msg.topic == TOPIC_TANQUE:
                    # Guardar datos de tanque
                    m2Sensoresdata.objects.create(
                        tanque_id=data.get("tanque_id"),
                        temperatura=float(data.get("temp_agua", 0)),
                        caudal=float(data.get("caudal", 0)),
                        porcentaje_llenado=float(data.get("porcentaje_llenado", 0)),
                        nivel=float(data.get("nivel", 0)),
                    )
                elif msg.topic == TOPIC_RIEGO:
                # Guardar trazabilidad completa
                    riegoRegistro.objects.create(
                        zona=int(data.get("zona", 0)),
                        accion=data.get("accion", "UNKNOWN"),
                        tiempo_segundos=int(data.get("tiempo_ms", 0)) // 1000,  # convertir ms a segundos
                        temp_amb=float(data.get("temp_amb", 0)),
                        hum_amb=float(data.get("hum_amb", 0)),
                        hum_suelo=float(data.get("hum_suelo", 0)),
                        peso=float(data.get("peso", 0)),
                        modo=data.get("modo", "AUTO" if not data.get("manual") else "MANUAL")
                    )
                    print(f"Riego registrado: {data}")
                else:
                    print("Tópico desconocido:", msg.topic)

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
