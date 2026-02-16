from django.shortcuts import render
from .models import m1Sensoresdata
# Create your views here.
import time
import paho.mqtt.client as mqtt
import uuid
import os
from django.http import JsonResponse


def homepage(request):
    return render(request,'iotappweb/homepage.html')

def publicar_mqtt(accion,topic):
    APP_DIR = os.path.dirname(__file__)

    MQTT_HOST = "a4810e38lk0oy-ats.iot.us-east-1.amazonaws.com"
    MQTT_PORT = 8883
    TOPIC = topic
    #MQTT_USER = "sdc-iot"       # <-- Aquí tu usuario
    #MQTT_PASS = "nuevacontraseña"    # <-- Aquí tu contraseña

    ca = os.path.join(APP_DIR, "AmazonRootCA1.pem")
    cert = os.path.join(APP_DIR, "cert.pem.crt")
    key = os.path.join(APP_DIR, "private.pem.key")

    retorno = "Esperando"
    try:

        client = mqtt.Client(client_id=f"django-{uuid.uuid4()}")
        #client.username_pw_set(MQTT_USER, MQTT_PASS)
        client.tls_set(
            ca_certs=ca,
            certfile=cert,
            keyfile=key
        )

        client.connect(MQTT_HOST, MQTT_PORT, 60)

        client.loop_start()
        
        time.sleep(1)
        
        result = client.publish(TOPIC, accion.upper(), qos=0)
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            retorno = "Publicado con éxito"
        else:
            retorno = f"Error código {result.rc}"
        result.wait_for_publish()

        time.sleep(0.5)
        client.loop_stop()
        client.disconnect()

    except Exception as e:
        retorno = f"Error MQTT: {str(e)}"

    return {
        "retorno":retorno
    }

def enviarinstruccion(request):
    if request.method == "POST":
        accion = request.POST.get("accion")
        print("Acción recibida:", accion)
        info = publicar_mqtt(accion,"casa/tanque01/llenado/manual")
        return JsonResponse({"status": "ok", "accion_recibida": accion,
                            "retorno": info["retorno"]})

    return render(request, "iotappweb/accionmqtt.html")

def dashboard(request):
    latest = m1Sensoresdata.objects.order_by('-timestamp').first()
    return render(request, 'iotappweb/dashboard.html', {'latest': latest})