from django.shortcuts import render
from .models import m1Sensoresdata, m2Sensoresdata, riegoRegistro
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
from datetime import timedelta


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

def enviarinstruccion(request):
    """
    Vista unificada para:
    - Riego on/off/auto
    - Riego con tiempo y válvula (modal)
    - Tanque manual
    """
    if request.method == "POST":
        # Intentamos recibir JSON (para riego manual con tiempo/valvula)
        if request.content_type == "application/json":
            data = json.loads(request.body)
            accion = data.get("accion")
            dispositivo = data.get("dispositivo")
            zona = data.get("valvula")  # opcional
            tiempo = data.get("tiempo")    # opcional
        else:
            # Botones normales (on/off/auto)
            accion = request.POST.get("accion")
            dispositivo = request.POST.get("dispositivo")
            zona = None
            tiempo = None

        # Preparamos payload para MQTT
        payload = {"accion": accion}
        if zona:
            payload["zona"] = zona
        if tiempo:
            payload["tiempo"] = tiempo

        payload_json = json.dumps(payload)

        # Selección de topic
        if dispositivo == "riego":
            topic = "casa/tanque01/riego/manual"
        elif dispositivo == "tanque":
            topic = "casa/tanque01/llenado/manual"
        else:
            return JsonResponse({"status": "error", "msg": "Dispositivo desconocido"})

        retorno = publicar_mqtt(payload_json, topic)

        return JsonResponse({
            "status": "ok",
            "accion": payload,
            "dispositivo": dispositivo,
            "retorno": retorno
        })

    return JsonResponse({"status": "error", "msg": "Método no permitido"})

def plantadashboard(request):
    plantas = m1Sensoresdata.objects.values_list('planta_id', flat=True).distinct()
    
    return render(request, 'iotappweb/plantadashboard.html', {
        'plantas': plantas
    })

from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Avg
from dateutil.parser import parse as parse_datetime
from datetime import datetime

def planta_api(request):
    planta_id = request.GET.get('planta_id')
    desde = request.GET.get('desde')
    hasta = request.GET.get('hasta')
    limite = int(request.GET.get('limite', 50))

    # Query base
    data = m1Sensoresdata.objects.all().order_by('-timestamp')

    if planta_id:
        data = data.filter(planta_id=planta_id)

    if desde:
        data = data.filter(timestamp__gte=parse_datetime(desde))
    if hasta:
        data = data.filter(timestamp__lte=parse_datetime(hasta))

    # Últimos N registros
    data = list(data[:limite])[::-1]

    # Último registro por planta
    latest_by_planta = {}
    plantas = m1Sensoresdata.objects.values_list('planta_id', flat=True).distinct()
    for p in plantas:
        q = m1Sensoresdata.objects.filter(planta_id=p).order_by('-timestamp').first()
        if q:
            latest_by_planta[p] = {
                "temperatura": round(q.temperatura, 2),
                "humedad_aire": round(q.humedad_aire, 2),
                "humedad_suelo": round(q.humedad_suelo, 2),
                "peso": round(q.peso, 2),
                "timestamp": timezone.localtime(q.timestamp).strftime("%Y-%m-%d %H:%M:%S")
            }

    # Promedio del día (desde 00:00 hasta ahora)
    today_start = timezone.localtime(timezone.now()).replace(hour=0, minute=0, second=0, microsecond=0)
    avg_today = m1Sensoresdata.objects.filter(timestamp__gte=today_start)
    if planta_id:
        avg_today = avg_today.filter(planta_id=planta_id)

    avg_data = avg_today.aggregate(
        temperatura=Avg('temperatura'),
        humedad_aire=Avg('humedad_aire'),
        humedad_suelo=Avg('humedad_suelo'),
        peso=Avg('peso')
    )

    # Formatear
    def round2(v):
        return round(v, 2) if v else 0

    avg_data = {k: round2(v) for k, v in avg_data.items()}

    response = {
        "timestamps": [timezone.localtime(d.timestamp).strftime("%H:%M:%S") for d in data],
        "temperatura": [round2(d.temperatura) for d in data],
        "humedad_aire": [round2(d.humedad_aire) for d in data],
        "humedad_suelo": [round2(d.humedad_suelo) for d in data],
        "peso": [round2(d.peso) for d in data],
        "latest_by_planta": latest_by_planta,
        "avg_today": avg_data
    }

    return JsonResponse(response)

def tanquedashboard(request):
    return render(request, "iotappweb/tanquedashboard.html")

def historial_riegos(request):
    
    hace_7_dias = timezone.now() - timedelta(days=7)

    riegos = riegoRegistro.objects.filter(
        fecha__gte=hace_7_dias
    ).select_related('planta_reg', 'tanque_reg').order_by('-registro')

    return render(request, "iotappweb/historialderiegos.html", {
        "riegos": riegos
    })

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

