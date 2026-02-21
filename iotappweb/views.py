from django.shortcuts import render
from .models import m1Sensoresdata, m2Sensoresdata
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


MQTT_HOST = "10.111.112.4"
MQTT_PORT = 1883
MQTT_USER = "sdc-iot"       
MQTT_PASS = "nuevacontraseña"  

def homepage(request):
    return render(request,'iotappweb/homepage.html')

def publicar_mqtt(accion, topic):
    """
    Publica un mensaje MQTT en el topic dado.
    """
    retorno = "Esperando"
    try:
        client = mqtt.Client(client_id=f"django-{uuid.uuid4()}")
        client.username_pw_set(MQTT_USER, MQTT_PASS)
        client.connect(MQTT_HOST, MQTT_PORT, 60)
        client.loop_start()
        time.sleep(1)
        result = client.publish(topic, accion.upper(), qos=0)
        result.wait_for_publish()

        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            retorno = "Publicado con éxito"
        else:
            retorno = f"Error código {result.rc}"

        client.loop_stop()
        client.disconnect()
        
    except Exception as e:
        retorno = f"Error MQTT: {str(e)}"

    return retorno

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import datetime

# Simulación de datos del tanque (normalmente lo traerías de tu DB o MQTT)
TANQUE_DATOS = {
    "latest": {
        "nivel": 50.0,
        "porcentaje_llenado": 50,
        "temperatura": 25.0,
        "caudal": 10.0,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    },
    "timestamps": [],
    "temperatura": [],
    "caudal": [],
    "porcentaje_llenado": []
}

def tanquedashboard(request):
    """
    Renderiza el dashboard del tanque.
    """
    return render(request, "iotappweb/tanquedashboard.html")


def tanque_api(request):
    """
    Retorna datos del tanque en formato JSON para la gráfica.
    """
    # Parámetros opcionales
    limite = int(request.GET.get("limite", 50))
    tanque_id = request.GET.get("tanque_id")
    desde = request.GET.get("desde")
    hasta = request.GET.get("hasta")

    # Aquí podrías filtrar tus datos reales según tanque_id y rango de fechas
    # Por ahora devolvemos los datos simulados
    response = TANQUE_DATOS.copy()
    return JsonResponse(response)


@csrf_exempt
def enviarinstruccion(request):
    """
    Recibe instrucciones para riego o tanque.
    Puede ser desde botones normales o desde modal de riego manual.
    """
    if request.method == "POST":
        try:
            if request.content_type == "application/json":
                # Riego manual con tiempo y válvula
                data = json.loads(request.body)
                accion = data.get("accion")
                dispositivo = data.get("dispositivo")
                valvula = data.get("valvula")
                tiempo = data.get("tiempo")
            else:
                # Botones normales (on/off/auto)
                accion = request.POST.get("accion")
                dispositivo = request.POST.get("dispositivo")
                valvula = None
                tiempo = None

            # Aquí va la lógica de MQTT o de control real
            # Por ejemplo:
            print(f"[INFO] Instrucción recibida -> Dispositivo: {dispositivo}, Acción: {accion}, Válvula: {valvula}, Tiempo: {tiempo}")

            # Simular respuesta
            return JsonResponse({"status": "ok", "accion": accion, "dispositivo": dispositivo})

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error", "message": "Método no permitido"}, status=405)

def plantadashboard(request):
    plantas = m1Sensoresdata.objects.values_list('planta_id', flat=True).distinct()
    
    return render(request, 'iotappweb/plantadashboard.html', {
        'plantas': plantas
    })
    
def planta_api(request):
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

def tanquedashboard(request):
    return render(request, "iotappweb/tanquedashboard.html")

def tanque_api(request):
    tanque_id = request.GET.get('tanque_id')
    desde = request.GET.get('desde')
    hasta = request.GET.get('hasta')
    limite = int(request.GET.get('limite', 50))

    data = m2Sensoresdata.objects.all().order_by('-timestamp')

    if tanque_id:
        data = data.filter(tanque_id=tanque_id)
    if desde:
        data = data.filter(timestamp__gte=parse_datetime(desde))
    if hasta:
        data = data.filter(timestamp__lte=parse_datetime(hasta))

    data = list(data[:limite])[::-1]

    def round2(v):
        return round(v, 2) if v is not None else 0

    response = {
        "timestamps": [
            timezone.localtime(d.timestamp).strftime("%H:%M:%S")
            for d in data
        ],
        "temperatura": [round2(d.temperatura) for d in data],
        "caudal": [round2(d.caudal) for d in data],
        "nivel": [round2(d.nivel) for d in data],
        "porcentaje_llenado": [round2(d.porcentaje_llenado) for d in data],
        "latest": {
            "temperatura": round2(data[-1].temperatura) if data else 0,
            "caudal": round2(data[-1].caudal) if data else 0,
            "nivel": round2(data[-1].nivel) if data else 0,
            
            "porcentaje_llenado": round2(data[-1].porcentaje_llenado) if data else 0,
            "timestamp": timezone.localtime(data[-1].timestamp).strftime("%Y-%m-%d %H:%M:%S") if data else ""
        }
    }
    return JsonResponse(response)


