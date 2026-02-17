from django.shortcuts import render
from .models import m1Sensoresdata
# Create your views here.
import time
import paho.mqtt.client as mqtt
import uuid
import os
from django.http import JsonResponse
import json
from django.utils.dateparse import parse_datetime
from django.db.models import Q
from django.utils import timezone



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
    plantas = m1Sensoresdata.objects.values_list('planta_id', flat=True).distinct()
    
    return render(request, 'iotappweb/dashboard.html', {
        'plantas': plantas
    })
    
def sensor_api(request):
    planta_id = request.GET.get('planta_id')
    desde = request.GET.get('desde')
    hasta = request.GET.get('hasta')
    limite = request.GET.get('limite', 50)

    data = m1Sensoresdata.objects.all().order_by('-timestamp')

    if planta_id:
        data = data.filter(planta_id=planta_id)

    if desde:
        data = data.filter(timestamp__gte=parse_datetime(desde))

    if hasta:
        data = data.filter(timestamp__lte=parse_datetime(hasta))

    data = data[:int(limite)][::-1]

    def round2(v):
        return round(v, 2) if v else 0

    response = {
        "timestamps": [
            timezone.localtime(d.timestamp).strftime("%H:%M:%S")
            for d in data
        ],
        "temperatura": [round2(d.temperatura) for d in data],
        "humedad_aire": [round2(d.humedad_aire) for d in data],
        "humedad_suelo": [round2(d.humedad_suelo) for d in data],
        "peso": [round2(d.peso) for d in data],
        "latest": {
            "temperatura": round2(data[-1].temperatura) if data else 0,
            "humedad_aire": round2(data[-1].humedad_aire) if data else 0,
            "humedad_suelo": round2(data[-1].humedad_suelo) if data else 0,
            "peso": round2(data[-1].peso) if data else 0,
            "timestamp": timezone.localtime(data[-1].timestamp).strftime("%Y-%m-%d %H:%M:%S") if data else ""
        }
    }

    return JsonResponse(response)


