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
from django.db.models import Q, Avg, Max
from django.utils import timezone
from datetime import timedelta, datetime
from collections import defaultdict


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

def planta_api(request):
    try:
        planta_id = request.GET.get('planta_id')
        desde = request.GET.get('desde')
        hasta = request.GET.get('hasta')
        limite = int(request.GET.get('limite', 50))

        # Traer todos los datos ordenados descendente
        data = m1Sensoresdata.objects.all().order_by('-timestamp')

        if planta_id:
            data = data.filter(planta_id=planta_id)

        if desde:
            dt_desde = parse_datetime(desde)
            if dt_desde:
                data = data.filter(timestamp__gte=dt_desde)

        if hasta:
            dt_hasta = parse_datetime(hasta)
            if dt_hasta:
                data = data.filter(timestamp__lte=dt_hasta)

        # Solo últimos N registros
        data = list(data[:limite][::-1])  # invertimos para ascendente

        def round2(v):
            return round(v, 2) if v is not None else 0

        # Fechas y valores para la gráfica
        timestamps = [timezone.localtime(d.timestamp).strftime("%H:%M:%S") for d in data]
        temperatura = [round2(d.temperatura) for d in data]
        humedad_aire = [round2(d.humedad_aire) for d in data]
        humedad_suelo = [round2(d.humedad_suelo) for d in data]
        peso = [round2(d.peso) for d in data]

        # Últimos datos por planta
        latest_by_planta = {}
        all_plantas = m1Sensoresdata.objects.values_list('planta_id', flat=True).distinct()
        for planta in all_plantas:
            last_entry = m1Sensoresdata.objects.filter(planta_id=planta).order_by('-timestamp').first()
            if last_entry:
                latest_by_planta[planta] = {
                    "temperatura": round2(last_entry.temperatura),
                    "humedad_aire": round2(last_entry.humedad_aire),
                    "humedad_suelo": round2(last_entry.humedad_suelo),
                    "peso": round2(last_entry.peso),
                    "timestamp": timezone.localtime(last_entry.timestamp).strftime("%Y-%m-%d %H:%M:%S")
                }

        # Último dato general
        latest = {}
        if planta_id and planta_id in latest_by_planta:
            latest = latest_by_planta[planta_id]
        elif latest_by_planta:
            latest = list(latest_by_planta.values())[0]

        # Promedio del día en curso
        today = timezone.localtime(timezone.now()).date()
        avg_today_qs = m1Sensoresdata.objects.filter(timestamp__date=today)
        if planta_id:
            avg_today_qs = avg_today_qs.filter(planta_id=planta_id)

        avg_today = {
            "temperatura": round2(avg_today_qs.aggregate(Avg('temperatura'))['temperatura__avg']),
            "humedad_aire": round2(avg_today_qs.aggregate(Avg('humedad_aire'))['humedad_aire__avg']),
            "humedad_suelo": round2(avg_today_qs.aggregate(Avg('humedad_suelo'))['humedad_suelo__avg']),
            "peso": round2(avg_today_qs.aggregate(Avg('peso'))['peso__avg']),
        }

        response = {
            "timestamps": timestamps,
            "temperatura": temperatura,
            "humedad_aire": humedad_aire,
            "humedad_suelo": humedad_suelo,
            "peso": peso,
            "latest": latest,
            "avg_today": avg_today,
            "latest_by_planta": latest_by_planta,
        }

        return JsonResponse(response)

    except Exception as e:
        # Devuelve error en JSON en lugar de HTML
        return JsonResponse({"error": str(e)}, status=500)

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

def consumo_acumulado(request):
    """
    Vista para mostrar consumo acumulado de agua por planta.
    Solo muestra los días de la semana actual.
    """
    hoy = datetime.now()
    inicio_semana = hoy - timedelta(days=hoy.weekday())  # lunes de la semana actual
    fin_semana = inicio_semana + timedelta(days=7)       # domingo

    # Traemos todos los riegos de la semana
    riegos = riegoRegistro.objects.filter(
        timestamp__gte=inicio_semana,
        timestamp__lt=fin_semana
    ).select_related('planta_reg', 'tanque_reg')

    # Creamos la tabla de datos
    tabla = defaultdict(lambda: defaultdict(float))
    plantas_set = set()

    for r in riegos:
        if not r.planta_reg or not r.tanque_reg:
            continue

        planta_id = r.planta_reg.planta_id
        plantas_set.add(planta_id)

        # litros = caudal (L/min) * tiempo_segundos / 60
        litros = r.tiempo_segundos * r.tanque_reg.caudal / 60.0

        fecha = r.timestamp.date()
        tabla[fecha][planta_id] += litros

    fechas = sorted(tabla.keys())
    plantas = sorted(list(plantas_set))

    # Aplanamos la tabla para que sea compatible con Django template
    fechas_plantas = []
    for fecha in fechas:
        fila = {"fecha": fecha}
        for planta in plantas:
            fila[planta] = tabla[fecha].get(planta, 0)
        fechas_plantas.append(fila)

    context = {
        "fechas_plantas": fechas_plantas,
        "plantas": plantas,
    }

    return render(request, "consumo_acumulado_modal.html", context)