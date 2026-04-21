# Create your views here.

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from openpyxl import Workbook
from django.shortcuts import get_object_or_404, redirect
from .models import Actpeso,supervision,envioccajas,supervisionproduccion,pedidos,tipoCajas,controlcajas, proyecciones,paramenvlocales,enviosrec,AcumFrutaaux,salidacontenedores, inventarioProdTermAux,productores,contenedores,Boletas, detallerecaux,detallerec,salidasFruta, usuariosAppFruta, datosProduccion, detallesProduccion, detallesEstructuras, Recepciones, Ccalidad,causasRechazo,inventarioProdTerm,productoTerm,cultivoxFinca,AcumFruta
from .forms import boletasForm,controlcajasForm,pedidosForm,itemsForm, itemsenviosForm,salidacontenedoresForm,salidasFrutaForm, contenedoresForm,recepcionesForm, ccalidadForm, inventarioFrutaForm, acumFrutaForm
from django.db.models import  Case, Count, Avg, When,Sum, Q, Max, Min,Value as V,F, ExpressionWrapper, FloatField, IntegerField
from django.db.models.functions import Abs, Trim
from django.utils import timezone
import matplotlib.pyplot as plt
import datetime
from io import BytesIO
import base64
import json
import pandas as pd
import pytz
from openpyxl.utils.dataframe import dataframe_to_rows
from django.template.loader import render_to_string
from django.contrib import messages
from collections import defaultdict
from django.db.models.functions import ExtractWeek, ExtractYear, ExtractIsoYear, ExtractMonth
from django.views.decorators.http import require_GET
from django.urls import reverse
from django.db import transaction
from .view import *
from django.db.models.functions import TruncDate


def obtener_nombre_usuario(request):
    # Obtén el nombre de usuario del usuario autenticado
    now = datetime.datetime.now()
    fecha = now.date()
    dia= fecha.day
    mes= fecha.month
    año= fecha.year
    if mes < 10:
        mes = "0" + str(mes)
    if dia < 10:
        dia = "0" + str(dia)
    fecha_= "{}-{}-{}".format(str(año),str(mes),str(dia))
    nombre_usuario = request.user.username
    
    datos = usuariosAppFruta.objects.filter(correo=nombre_usuario).values('finca', 'encargado')
    adicionales = detallesEstructuras.objects.filter(finca=list(datos)[0]['finca']).values('cultivo').distinct('cultivo')
    return JsonResponse({'username': nombre_usuario,'fecha':fecha_,'adicionales':list(adicionales),'finca':list(datos)[0]['finca'],'encargado':list(datos)[0]['encargado'] })

def obtenerfecha_invFruta(request):
    # Obtén el nombre de usuario del usuario autenticado
    now = datetime.datetime.now()
    fecha = now.date()
    dia= fecha.day
    mes= fecha.month
    año= fecha.year
    if mes < 10:
        mes = "0" + str(mes)
    if dia < 10:
        dia = "0" + str(dia)

    fecha_= "{}-{}-{}".format(str(año),str(mes),str(dia))
    return JsonResponse({'fecha':fecha_})

def load_dataUsuario(request):
    correo_id = request.GET.get('category_id')
    datos = usuariosAppFruta.objects.filter(correo=correo_id).values('finca', 'encargado')
    adicionales = cultivoxFinca.objects.filter(finca=list(datos)[0]['finca']).values('cultivo').distinct('cultivo')
    adicionales_ = datosProduccion.objects.filter(finca=list(datos)[0]['finca']).values('orden').distinct('orden')
    return JsonResponse({'datos': list(datos),'correo':correo_id,'adicionales':list(adicionales),'ordenes':list(adicionales_)})

def load_dataUsuario4(request):
    ordenSelect = request.GET.get('orden')
    cultivo_ = request.GET.get('cultivo')
    finca_ = request.GET.get('finca')
    
    variedad = detallesEstructuras.objects.filter(cultivo=cultivo_,orden=ordenSelect,finca=finca_).values('variedad').distinct('variedad')
    # Filtra las estructuras basadas en la orden seleccionada
    estructura = detallesEstructuras.objects.filter(cultivo=cultivo_,orden=ordenSelect,finca=finca_).values('estructura').distinct('estructura')
    return JsonResponse({'estructura': list(estructura),'variedad': list(variedad)})

def load_dataUsuario2(request):
    ordenSelect = request.GET.get('category_id')
    cultivo_ = request.GET.get('cultivo')
    finca_ = request.GET.get('finca')

    # Filtra las órdenes de detallesEstructuras por finca y cultivo
    orden = detallesEstructuras.objects.filter(finca=finca_, cultivo=cultivo_).values('orden').distinct('orden')

    # Filtra los cultivos basados en la orden seleccionada y estado "Abierta"
    cultivo = datosProduccion.objects.filter(orden=ordenSelect, status="Abierta").values('cultivo')

    # Verifica si hay al menos un cultivo en los resultados
    if cultivo:
        # Si hay un cultivo, toma el primero y filtra las variedades asociadas
        variedad = detallesProduccion.objects.filter(cultivo=list(cultivo)[0]['cultivo']).values('variedad')
    else:
        # Si no hay cultivos, asigna una lista vacía a variedad
        variedad = []

    # Filtra las estructuras basadas en la orden seleccionada
    estructura = detallesEstructuras.objects.filter(orden=ordenSelect).values('estructura')

    # Devuelve los resultados como JSON
    return JsonResponse({
        'datos': list(cultivo),
        'variedad': list(variedad),
        'estructura': list(estructura),
        'orden': ordenSelect,
        'ordenes': list(orden)
    })

def load_dataUsuario3(request):
    cultivo_ = request.GET.get('category_id')
    finca_ = request.GET.get('finca')
    cultivo = detallesEstructuras.objects.filter(finca=finca_).values('cultivo').distinct('cultivo')
    variedad= cultivoxFinca.objects.filter(finca=finca_,cultivo=cultivo_).values('variedad').distinct('variedad')
    semana = AcumFruta.objects.values('fecha').distinct().order_by('-fecha')

    # Convierte el queryset a una lista de diccionarios
    df = pd.DataFrame(list(semana))

    # Convierte la columna 'fecha' a tipo datetime
    df['fecha'] = pd.to_datetime(df['fecha'])
    # Extrae el número de semana y el año
    df['semana'] = df['fecha'].dt.isocalendar().week
    df['año'] = df['fecha'].dt.isocalendar().year

    # Crea una nueva columna con la combinación "Semana-Año"
    df['periodo'] = 'Semana ' + df['semana'].astype(str) + ' del ' + df['año'].astype(str)
    df = df.drop_duplicates(subset=['periodo'])
    # Conviértelo de nuevo a una lista de diccionarios
    semana_año_list = df[['fecha', 'periodo']].to_dict(orient='records')

    #variedad = cultivoxFinca.objects.filter(cultivo=list(cultivo)[0]['cultivo']).values('variedad')
    return JsonResponse({'datos': list(variedad),'cultivo': list(cultivo),'semana':semana_año_list})

def load_dataUsuario5(request):

    nombre_usuario = request.user.username
    proveedor = Boletas.objects.values('finca').distinct('finca')
    
    return JsonResponse({'username':nombre_usuario,'proveedor': list(proveedor)})

def load_dataUsuario6(request):

    opcion1 = request.GET.get('proveedor')
    cultivo = Boletas.objects.filter(finca=opcion1).values('cultivo').distinct('cultivo')
    
    return JsonResponse({'cultivo': list(cultivo)})

def load_dataUsuario7(request):

    opcion1 = request.GET.get('fechareporte')  # fecha
    opcion2 = request.GET.get('cultivo')       # cultivo

    # Paso 1: Obtener los itemcodigo que tengan ese cultivo
    
    items_filtrados = productoTerm.objects.filter(cultivo=opcion2).values_list('itemsapcode', flat=True)

    fecha_obj = datetime.datetime.strptime(opcion1, '%Y-%m-%d').date()
    envios = enviosrec.objects.filter(fecha=fecha_obj).exclude(status="Anulado"
            ).exclude(
                productor__isnull=True
            ).exclude(
                productor__exact=''
            ).values_list('envio', flat=True).distinct()    
            
    return JsonResponse({'envio':list(envios)})

def load_dataUsuario8(request):

    opcion1 = request.GET.get('fechareporte')  # fecha
    opcion2 = request.GET.get('cultivo')       # cultivo

    # Paso 1: Obtener los itemcodigo que tengan ese cultivo

    fecha_obj = datetime.datetime.strptime(opcion1, '%Y-%m-%d').date()
    conten = salidacontenedores.objects.filter(fechasalcontenedor=fecha_obj).exclude(status="Anulado"
            ).values_list('contenedor', flat=True).distinct()    
            
    return JsonResponse({'contenedores':list(conten)})

def load_dataUsuario9(request):
    contenedor = request.GET.get('contenedor')
    fecha = request.GET.get('fecha')

    cultivos = (salidacontenedores.objects
        .filter(contenedor=contenedor, fechasalcontenedor=fecha)
        .values_list('cultivo', flat=True)
        .distinct()
    )

    return JsonResponse({
        "cultivos": list(cultivos)
    })

def obtener_registros_y_graficar(filtros):
    registros = AcumFruta.objects.exclude('Anulado').filter(**filtros)
    
    df = pd.DataFrame(list(registros.values()), columns=['fecha', 'orden', 'libras'])
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')

    # Agregar columnas para el número de semana y el año
    df['semana'] = df['fecha'].dt.isocalendar().week
    df['año'] = df['fecha'].dt.isocalendar().year
    df['kilos'] = df['libras'] * 0.453592

    # Agrupar por semana y año, sumando los kilos
    df_agrupado = df.groupby(['semana', 'año'], as_index=False).agg(
        total_kilos=('kilos', 'sum'),
        semana=('semana', 'first'),
        orden=('orden', 'first'),
        año=('año', 'first')
    )

    # Crear una nueva columna que combine semana y año en un formato "año-semana"
    df_agrupado['semana_año'] = df_agrupado['año'].astype(str) + '-W' + df_agrupado['semana'].astype(str)

    areas = datosProduccion.objects.all()

    df_areas = pd.DataFrame(list(areas.values()), columns=['orden', 'area'])  # 'orden' y 'area'

    # Realizamos un merge para agregar las áreas correspondientes a cada 'orden'
    df_final = df_agrupado.merge(df_areas, on='orden', how='inner')
    df_final['kxm2'] = df_final['total_kilos'] /df_final['area']
    registros_finales = df_final.to_dict(orient='records')
    # Extraer los valores para los ejes
    x_vals = df_final['semana_año']
    y_vals = df_final['kxm2']

    # Crear el gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(x_vals, y_vals, marker='o', linestyle='-', color='b')

    # Etiquetas y título
    plt.xlabel('Semana y Año')
    plt.ylabel('Kilos')
    plt.title('Gráfico de Kilos por Semana y Año')
    plt.xticks(rotation=45)

    # Guardar la figura en un objeto BytesIO para enviarla a la respuesta HTTP
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Codificar la imagen en base64
    imagen_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')

    return imagen_base64, registros_finales

def get_date_from_week(anio, semana):
    first_day = datetime.datetime(anio, 1, 4)  # El 4 de enero siempre está en la semana 1
    start_of_week = first_day - datetime.timedelta(days=first_day.weekday())
    return (start_of_week + datetime.timedelta(weeks=semana - 1)).date()

def get_ordenes_por_finca(request):
    finca = request.POST.get('finca')
    if finca:
        ordenes_abiertas = datosProduccion.objects.filter(status='Abierta').values_list('orden', flat=True)
        ordenes = AcumFruta.objects.filter(finca=finca,orden__in=ordenes_abiertas)\
            .exclude(orden__isnull=True)\
            .exclude(orden='')\
            .values_list('orden', flat=True)\
            .distinct()
        return JsonResponse({'ordenes': list(ordenes)})
    return JsonResponse({'ordenes': []})

def get_ordenes_por_finca2(request):
    finca = request.POST.get('finca')
    nombre_usuario = request.user.username
    ordenes_abiertas = datosProduccion.objects.filter(status='Abierta').values_list('orden', flat=True)
    if finca:
        ordenes = AcumFruta.objects.filter(finca=finca,correo=nombre_usuario,orden__in=ordenes_abiertas)\
            .exclude(orden__isnull=True)\
            .exclude(orden='')\
            .values_list('orden', flat=True)\
            .distinct()
        return JsonResponse({'ordenes': list(ordenes)})
    return JsonResponse({'ordenes': []})

def get_estructuras_por_orden(request):
    orden = request.POST.get('orden')
    
    if orden:
        estructuras = AcumFruta.objects.filter(orden=orden)\
            .exclude(estructura__isnull=True)\
            .exclude(estructura='')\
            .values_list('estructura', flat=True)\
            .distinct()
        cultivos = AcumFruta.objects.filter(orden=orden)\
            .exclude(cultivo__isnull=True)\
            .exclude(cultivo='')\
            .values_list('cultivo', flat=True)\
            .distinct()
        return JsonResponse({'estructuras': list(estructuras), 'cultivos':list(cultivos)})
    return JsonResponse({'estructuras': []})

def get_estructuras_por_orden2(request):
    orden = request.POST.get('orden')
    nombre_usuario = request.user.username
    if orden:
        estructuras = AcumFruta.objects.filter(orden=orden,correo=nombre_usuario)\
            .exclude(estructura__isnull=True)\
            .exclude(estructura='')\
            .values_list('estructura', flat=True)\
            .distinct()
        cultivos = AcumFruta.objects.filter(orden=orden, correo = nombre_usuario)\
            .exclude(cultivo__isnull=True)\
            .exclude(cultivo='')\
            .values_list('cultivo', flat=True)\
            .distinct()
        return JsonResponse({'estructuras': list(estructuras), 'cultivos':list(cultivos)})
    return JsonResponse({'estructuras': []})

def get_variedades_por_estructura(request):
    estructura = request.POST.get('estructura')
    orden = request.POST.get('orden')
    if estructura:
        variedades = AcumFruta.objects.filter(estructura=estructura).filter(orden=orden)\
            .exclude(variedad__isnull=True)\
            .exclude(variedad='')\
            .values_list('variedad', flat=True)\
            .distinct()
        return JsonResponse({'variedad': list(variedades)})
    return JsonResponse({'variedad': []})

def get_variedades_por_estructura2(request):
    estructura = request.POST.get('estructura')
    nombre_usuario = request.user.username
    orden = request.POST.get('orden')
    if estructura:
        variedades = AcumFruta.objects.filter(estructura=estructura,correo=nombre_usuario).filter(orden=orden)\
            .exclude(variedad__isnull=True)\
            .exclude(variedad='')\
            .values_list('variedad', flat=True)\
            .distinct()
        return JsonResponse({'variedad': list(variedades)})
    return JsonResponse({'variedad': []})

def formar_clave(finca, cultivo):
    return (finca.strip().upper(), cultivo.strip().upper())

def formar_clave2(finca, cultivo,orden,estructura,variedad):
    return (finca.strip().upper(), cultivo.strip().upper(),orden.strip().upper(),estructura.strip().upper(),variedad.strip().upper())

def formar_clave3(recepcion,proveedor, cultivo, fecha):
    return (recepcion.strip().upper(),proveedor.strip().upper(), cultivo.strip().upper(),fecha.strip().upper())

def formar_clave4(finca, cultivo,orden):
    return (finca.strip().upper(), cultivo.strip().upper(),orden.strip().upper())

def obtener_proveedor_desde_finca_llave(finca, llave):
    if finca.strip().lower() == "productor":
        return llave.strip()
    return finca.strip()

def obtener_proveedor_detalle(finca, llave):
    if (finca or "").strip().lower() == "productor":
        return (llave or "").strip()
    return (finca or "").strip()

def graficas(request):
    data = json.loads(request.body)
    mensaje = data['array']

    
    # Construcción de filtros de consulta
    filtros = {}
    if mensaje[0][0]:  # finca
        filtros['finca'] = mensaje[0][0]
    if mensaje[0][1]:  # cultivo
        filtros['cultivo'] = mensaje[0][1]
    if mensaje[0][2]:  # orden
        filtros['orden'] = mensaje[0][2]
    if mensaje[0][3]:  # estructura
        filtros['estructura'] = mensaje[0][3]
    if mensaje[0][4]:  # variedad
        filtros['variedad'] = mensaje[0][4]

    # Validar que al menos haya un filtro seleccionado
    if not filtros:
        return JsonResponse({'mensaje': "Debe seleccionar por lo menos un parámetro para consultar."})

    # Llamar a la función para obtener registros y graficar
    imagen_base64, dataframe = obtener_registros_y_graficar(filtros)

        # Responder con el gráfico generado
        
    
    return JsonResponse( {
            'imagen': imagen_base64,
            'finca': mensaje[0][0],
            'cultivo': mensaje[0][1],
            'orden': mensaje[0][2],
            'estructura': mensaje[0][3],
            'variedad': mensaje[0][4],
            'dataframe': dataframe
        })