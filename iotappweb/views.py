from django.shortcuts import render
from .models import m1Sensoresdata, SensorDetalles,m2Sensoresdata, riegoRegistro, riegoResumen, SensorData, SensorAlert
# Create your views here.
import time
import paho.mqtt.client as mqtt
import uuid
import os
import numpy as np
from django.http import JsonResponse
import json
from django.utils.dateparse import parse_datetime
from django.db.models import Q, Avg, Max
from django.utils import timezone
from datetime import timedelta, datetime
from collections import defaultdict
from django.views.decorators.csrf import csrf_exempt
from functools import wraps
from twilio.rest import Client
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from .forms import sensordetallesForm

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
            topic = "casa/tanque/1/riego/manual"
        elif dispositivo == "tanque":
            topic = "casa/tanque/1/llenado/manual"
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
    Consumo acumulado por día para la semana actual, separado por válvula.
    """
    hoy = datetime.now()
    inicio_semana = hoy - timedelta(days=hoy.weekday())  # lunes
    fin_semana = inicio_semana + timedelta(days=7)       # domingo

    resumenes = riegoResumen.objects.filter(
        fecha__gte=inicio_semana,
        fecha__lt=fin_semana
    )

    # Para almacenar el consumo acumulado separado por válvula y fecha
    tabla = defaultdict(lambda: defaultdict(float))

    for resumen in resumenes:
        litros = resumen.litros_usados
        fecha = resumen.fecha.date()
        # Determinamos la válvula del riego (basado en el "zona" del riego)
        zona = resumen.riego.zona  # Aquí obtenemos la zona de riego
        valvula = 1 if zona == 1 else 2  # Asumimos que zona 1 es válvula 1 y zona 2 es válvula 2
        
        # Sumamos los litros consumidos por válvula y fecha
        tabla[fecha][valvula] += litros

    # Preparamos los datos para mostrarlos en el template
    fechas_litros = []
    for fecha in sorted(tabla.keys()):
        fila = {"fecha": fecha}
        fila["valvula_1"] = tabla[fecha].get(1, 0)
        fila["valvula_2"] = tabla[fecha].get(2, 0)
        fechas_litros.append(fila)

    # Pasamos los datos al contexto para ser usados en el template
    context = {
        "fechas_litros": fechas_litros,
    }

    return render(request, "consumo_acumulado_modal.html", context)

def histograma_api(request):
    
    planta = request.GET.get("planta_id")
    variable = request.GET.get("variable")
    desde = request.GET.get("desde")
    hasta = request.GET.get("hasta")

    if variable not in ["temperatura", "humedad_aire", "humedad_suelo", "peso"]:
        return JsonResponse({"error": "Variable inválida"}, status=400)

    queryset = m1Sensoresdata.objects.all()
    
    if planta:
        queryset = queryset.filter(planta_id=planta)
    if desde:
        queryset = queryset.filter(timestamp__gte=desde)
    if hasta:
        queryset = queryset.filter(timestamp__lte=hasta)

    valores = np.array(list(queryset.values_list(variable, flat=True)), dtype=float)

    if valores.size == 0:
        return JsonResponse({
            "bins": [],
            "counts": [],
            "media": 0,
            "mediana": 0,
            "std": 0,
            "min": 0,
            "max": 0,
            "total_mediciones": 0
        })

    counts, bins = np.histogram(valores, bins=10)
    media = float(np.mean(valores))
    mediana = float(np.median(valores))
    std = float(np.std(valores))
    min_val = float(np.min(valores))
    max_val = float(np.max(valores))
    total_mediciones = valores.size

    return JsonResponse({
        "bins": [round(b,2) for b in bins[:-1]],
        "counts": counts.tolist(),
        "media": round(media,2),
        "mediana": round(mediana,2),
        "std": round(std,2),
        "min": round(min_val,2),
        "max": round(max_val,2),
        "total_mediciones": total_mediciones
    })

def login_exempt(view_func):
    setattr(view_func, 'login_exempt', True)
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        return view_func(*args, **kwargs)
    return wrapped_view


def enviar_whatsapp(mensaje, numero):
    client = Client("AC5964f3c0c7a0055b23f9c5f750e0e118", "86ae449283a37034b118cfc12dc89af0")

    client.messages.create(
        body=mensaje,
        from_='whatsapp:+14155238886',
        to=f'whatsapp:{numero}'
    )
#ARANET_SECRET = "wgm499gftypgcmx7wkrcspwsf5ykt4rg"
ARANET_SECRET = "rphvcx8qe3dk5dwjfcw84na5vqz34jen"

@login_exempt
@csrf_exempt
def aranet_webhook(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method Not Allowed"}, status=405)

    token = request.headers.get("X-Aranet-Key")
    if token != ARANET_SECRET:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    try:
        data = json.loads(request.body)
        objects = []

        for record in data:
            sensor = record.get("bn")
            metric = record.get("n")
            value = record.get("v")
            unit = record.get("u")
            bt = record.get("bt")
            timestamp = (
                datetime.fromtimestamp(bt, tz=timezone.utc)
                if bt else timezone.now()
            )

            # Ignorar registros inválidos
            if not sensor or not metric or value is None:
                continue

            sensor_code = sensor.rstrip(":")

            sensor_obj = SensorDetalles.objects.filter(sensor=sensor_code).first()
            if not sensor_obj:
                continue
            objects.append(
                SensorData(
                    sensor=sensor_obj,
                    metric=metric,
                    value=value,
                    unit=unit,
                    timestamp=timestamp
                )
            )

        if objects:
            SensorData.objects.bulk_create(objects, batch_size=100)
            ahora = timezone.now()
            hace_10_min = ahora - timedelta(minutes=10)
            datos_recientes = [
                obj for obj in objects
                if obj.timestamp >= hace_10_min
            ]
            if len(datos_recientes) < len(objects) * 0.3:
                print("📦 Bulk histórico detectado → no se envían alertas")
                return JsonResponse({"status": "bulk_saved_no_alerts"})

            sensores = set(obj.sensor for obj in datos_recientes)
            for sensor in sensores:
                resultado = evaluar_sensor(sensor)
                if resultado:
                    enviar_alerta(resultado)

        return JsonResponse({"status": "ok", "saved": len(objects)})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
        
def aranet_resumen_json(request):
    # Obtener todos los sensores distintos
    sensores = SensorData.objects.values_list('sensor', flat=True).distinct()

    resultado = []

    for sensor in sensores:
        readings = SensorData.objects.filter(
            sensor=sensor,
            metric="weight"
        ).order_by('-timestamp')[:50]

        if not readings:
            continue

        peso_actual = readings[0].value
        peso_base = readings[0].sensor.set_point  # aquí tu valor base

        if peso_base == 0:
            continue

        porcentaje_restante = (peso_actual / peso_base) * 100
        porcentaje_perdida = 100 - porcentaje_restante

        # agregar finca, priva y estructura
        resultado.append({
            "sensor": str(readings[0].sensor.sensor),
            "finca": readings[0].sensor.finca,
            "priva": readings[0].sensor.priva,
            "estructura": readings[0].sensor.estructura,
            "peso_actual": round(peso_actual, 3),
            "peso_base": round(peso_base, 3),
            "porcentaje_restante": round(porcentaje_restante, 2),
            "porcentaje_perdida": round(porcentaje_perdida, 2),
        })
    resultado_ordenado = sorted(
        resultado,
        key=lambda x: (x['estructura'], x['priva'])
    )
    return JsonResponse(resultado_ordenado, safe=False)

def aranet_resumen_page(request):
    return render(request, "iotappweb/aranet_resumen.html")

def evaluar_sensor(sensor_obj):
    readings = SensorData.objects.filter(
        sensor=sensor_obj,
        metric="weight"
    ).order_by('-timestamp')[:5]

    if len(readings) < 2:
        return None

    peso_base = sensor_obj.set_point

    # calcular porcentajes
    porcentajes = []
    for r in readings:
        porcentaje_restante = (r.value / peso_base) * 100
        porcentaje_perdida = 100 - porcentaje_restante
        porcentajes.append(porcentaje_perdida)

    actual = porcentajes[0]
    anterior = porcentajes[1]

    cambio = actual - anterior

    # 1. ignorar ruido (<2%)
    if abs(cambio) < 2:
        return None

    # 2. ignorar saltos bruscos (>5%)
    if abs(cambio) > 5:
        print("⚠️ Salto brusco:", cambio)
        return None

    # 3. validar tendencia progresiva
    tendencia_subida = all(
        porcentajes[i] >= porcentajes[i+1]
        for i in range(len(porcentajes)-1)
    )

    tendencia_bajada = all(
        porcentajes[i] <= porcentajes[i+1]
        for i in range(len(porcentajes)-1)
    )

    if not (tendencia_subida or tendencia_bajada):
        print("⚠️ Tendencia inconsistente")
        return None

    # 🚨 4. reglas de alerta
    if actual >= sensor_obj.umbral_min:
        tipo = "riego"
    elif actual <= sensor_obj.umbral_max:
        tipo = "exceso"
    else:
        return None

    # resultado final
    return {
        "sensor": sensor_obj,
        "peso_actual": readings[0].value,
        "peso_base": peso_base,
        "porcentaje_perdida": actual,
        "cambio": cambio,
        "tipo": tipo
    }

def enviar_alerta(data):
    if data["tipo"] == "riego":
        mensaje = (
            f"🚨 NECESITA RIEGO\n"
            f"Sensor: {data['sensor']}\n"
            f"Finca: {finca}\n"
            f"Estructura: {estructura}\n"
            f"Priva: {priva}\n"
            f"Pérdida: {data['porcentaje_perdida']:.2f}%"
        )
    elif data["tipo"] == "exceso":
        mensaje = (
            f"💧 EXCESO DE RIEGO\n"
            f"Sensor: {data['sensor']}\n"
            f"Finca: {finca}\n"
            f"Estructura: {estructura}\n"
            f"Priva: {priva}\n"
            f"Exceso: {data['porcentaje_perdida']:.2f}%"
        )
    else:
        return

    # Guardar alerta en base de datos
    SensorAlert.objects.create(
        sensor=data['sensor'],
        tipo=data['tipo'],
        porcentaje_perdida=data['porcentaje_perdida'],
        mensaje=mensaje
    )

    # Enviar WhatsApp
    for numero in ["+50230664716","+50240304201","+50253050677"]:
        try:
            enviar_whatsapp(mensaje, numero)
        except Exception as e:
            print("❌ ERROR WhatsApp:", str(e)) 
# Retorna los últimos 20 registros en JSON
def aranet_data_json(request):
    readings = SensorData.objects.select_related('sensor').order_by('-timestamp')[:20]

    data = [{
        "finca": r.sensor.finca,
        "priva": r.sensor.priva,
        "estructura": r.sensor.estructura,
        "sensor": str(r.sensor),  # o r.sensor.nombre si tienes
        "timestamp": timezone.localtime(r.timestamp).strftime("%Y-%m-%d %H:%M:%S"),
        "metric": r.metric,
        "value": r.value,
        "unit": r.unit
    } for r in readings]
    resultado_ordenado = sorted(
        data,
        key=lambda x: (x['estructura'], x['priva'])
    )
    return JsonResponse(resultado_ordenado, safe=False)

# Página web para mostrar los datos en tiempo real
def aranet_live_page(request):
    # Se pueden mostrar los últimos 20 registros iniciales
    readings = SensorData.objects.order_by('-timestamp')[:14]
    return render(request, "iotappweb/aranet_live.html", {"readings": readings})

def detallesensores_list(request):
    #today = timezone.localtime(timezone.now()).date()
    salidas = SensorDetalles.objects.exclude(status__in=["Averiado","Anulado", "Cerrado"])
    return render(request, 'iotappweb/formsensores/detallesensores_list.html', {'registros': salidas})

def aranet_resumen_grafica_page(request):
    
    return render(request, "iotappweb/graficos_aranet.html")


def aranet_curvas_json(request):
    """
    Retorna los últimos 50 registros de peso por sensor.
    Formato limpio para JS.
    """
    sensores = SensorData.objects.filter(metric="weight").values_list('sensor', flat=True).distinct()
    resultado = []

    for sensor_id in sensores:
        readings_qs = SensorData.objects.filter(sensor_id=sensor_id, metric="weight").order_by('-timestamp')[:50]

        if not readings_qs.exists():
            continue

        sensor_obj = readings_qs.first().sensor

        # Creamos la lista de lecturas ordenadas de más antiguo a reciente
        readings = [
            {"timestamp": timezone.localtime(r.timestamp).strftime("%Y-%m-%d %H:%M:%S"), "value": r.value}
            for r in reversed(readings_qs)
            
        ]

        resultado.append({
            "sensor": str(sensor_obj.sensor),
            "finca": sensor_obj.finca,
            "priva": sensor_obj.priva,
            "estructura": sensor_obj.estructura,
            "readings": readings
        })

    return JsonResponse(resultado, safe=False)

def detallesensores_create(request):
    if request.method == 'POST':
        form = sensordetallesForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                # Manejar excepciones específicas (por ejemplo, UniqueConstraintError)
                return JsonResponse({'error': str(e)}, status=400)
            return redirect('detallesensores_list')
        else:
            # Imprimir errores para depuración
            return JsonResponse({'errores': form.errors}, status=400)
    else:
        # Inicializa el formulario vacío para GET
        form = sensordetallesForm()

    return render(request, 'iotappweb/formsensores/detallesensores_form.html', {'form': form, 'modo':'crear'})
    
def detallesensores_update(request, pk):
    salidas = get_object_or_404(SensorDetalles, pk=pk)
    if request.method == 'POST':
        form = sensordetallesForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('detallesensores_list')
    else:
        form = sensordetallesForm(instance=salidas)
    return render(request, 'iotappweb/formsensores/detallesensores_form.html', {'form': form,'modo':'actualizar'})

def detallesensores_delete(request, pk):

    salidas = get_object_or_404(SensorDetalles, pk=pk)

    if request.method == 'POST':
        salidas.status = 'Averiado'
        salidas.save()
        messages.success(request, "Sensor anulado correctamente.")
        return redirect('detallesensores_list')
    
    return render(request, 'iotappweb/formsensores/detallesensores_confirm_delete.html', {'registros': salidas})
