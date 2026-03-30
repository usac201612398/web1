from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
#from django.views import View
#from django.views.generic import TemplateView, ListView
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Avg, Max, Count
from django.db.models.functions import ExtractWeek, ExtractYear
from collections import defaultdict
import datetime
from django.db.models import Case, When, Value, IntegerField
import json
from django.db import transaction
from .auxiliares import *
# modelos
from plantaE.models import (
    supervisionfito,
    usuariosAppFruta
)

#from django.views.generic import TemplateView

  
def supervisionfitotomatescob_create(request):
    user = request.user.username

    if user == 'cosecha.rio@popoyan.com.gt':
        area = 'RIO'
    elif user == 'cosecha.valle@popoyan.com.gt' or user =='cosecha.valle2@popoyan.com.gt' or user =='linday.solares@popoyan.com.gt':
        area = 'VALLE'
    else:
        area = 'ALL'  # gerencial

    return render(request, 'plantaE/supervisionfito/supervisionfitotomatescob_formPlantilla.html',{
        'area_usuario': area,'user':user
    })

def supervisionfitotomatestizon_create(request):
    user = request.user.username

    if user == 'cosecha.rio@popoyan.com.gt':
        area = 'RIO'
    elif user == 'cosecha.valle@popoyan.com.gt' or user =='cosecha.valle2@popoyan.com.gt' or user =='linday.solares@popoyan.com.gt':
        area = 'VALLE'
    else:
        area = 'ALL'  # gerencial

    return render(request, 'plantaE/supervisionfito/supervisionfitotomatestizon_formPlantilla.html',{
        'area_usuario': area,'user':user
    })

def supervisionfito_list(request):

    hoy = timezone.now().date()
    user = request.user.username

    # ===== AREA POR USUARIO =====
    if user in ['cosecha.rio@popoyan.com.gt', 'jorge.cruz@popoyan.com.gt']:
        area = 'RIO'
    elif user in [
        'cosecha.valle@popoyan.com.gt',
        'cosecha.valle2@popoyan.com.gt',
        'linday.solares@popoyan.com.gt'
    ]:
        area = 'VALLE'
    else:
        area = 'ALL'  # gerencial

    # ===== RANGO SEMANAL =====
    inicio_semana = hoy - datetime.timedelta(days=hoy.weekday())
    fin_semana = inicio_semana + datetime.timedelta(days=6)

    # ===== QUERY BASE =====
    lotes = supervisionfito.objects.filter(
        status='Abierta',
        fecha__range=(inicio_semana, fin_semana)
    )

    # ===== FILTRO POR AREA =====
    if area != 'ALL':
        lotes = lotes.filter(finca=area)

    # ===== AGRUPACIÓN + CÁLCULOS =====
    lotes = (
        lotes
        .values(
            'fecha',
            'finca',
            'cultivo',
            'estructura',
            'zona',
            'actividad'
        )
        .annotate(
            total_muestras=Count('muestra', distinct=True),
            ultima_muestra=Max('muestra'),

            # 🔥 LÍMITE DINÁMICO
            limite=Case(
                When(actividad='Tizón', then=Value(5)),
                When(actividad='Cobertura', then=Value(2)),
                default=Value(0),
                output_field=IntegerField()
            )
        )
        .order_by('-fecha')
    )

    return render(request, 'plantaE/supervisionfito/supervisionfito_list.html', {
        'lotes': lotes,
        'area_usuario': area,
        'user': user
    })

def supervisionfito_delete(request, pk):

    salidas = get_object_or_404(supervisionfito, pk=pk)
    
    if request.method == 'POST':
        registros = supervisionfito.objects.filter(
            fecha=salidas.fecha,
            zona=salidas.zona,
            estructura=salidas.estructura,
            supervisor=salidas.supervisor,
            cultivo=salidas.cultivo,
            muestra=salidas.muestra
        )

        # Marcamos como 'Anulado'
        count = registros.update(status='Anulado')
        
        
        return render(request, 'plantaE/supervisionfito/supervisionfito_confirm_delete.html', {
            'alert_message': f'Se anularon {count} registros correctamente',
            'redirect_url': reverse('supervisionfito_list')
        })
    
    return render(request, 'plantaE/supervisionfito/supervisionfito_confirm_delete.html', {'registros': salidas})

@transaction.atomic
def supervisionfito_grabar(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    data = json.loads(request.body)
    filas = data.get('array', [])
    
    if not filas:
        return JsonResponse({'error': 'No se recibieron datos'}, status=400)

    # 🔑 Tomamos el primer registro para identificar el lote
    base = filas[0]

    filtros_lote = {
        'fecha': base.get('fecha'),
        'zona': base.get('zona'),
        'estructura': base.get('estructura'),
        'cultivo': base.get('cultivo'),
        'finca': base.get('area'),
        'actividad': base.get('actividad'),
        'status': 'Abierta'
    }

    # ¿Cuántas muestras ya existen?
    muestras_actuales = supervisionfito.objects.filter(
        **filtros_lote
    ).values('muestra').distinct().count()

    muestras_actuales = supervisionfito.objects.filter(
        **filtros_lote
    ).values('muestra').distinct().count()

    if base.get('actividad') == 'Tizón':
        muestralimite = 5
    else:
        muestralimite = 2

    if base.get('actividad') == 'Tizón' and muestras_actuales >= 5 :
        return JsonResponse({
            'error': 'Este lote ya cuenta con las 5 muestras completas'
        }, status=400)
    elif base.get('actividad') == 'Cobertura' and muestras_actuales >= 2 :
        return JsonResponse({
            'error': 'Este lote ya cuenta con la muestra completa'
        }, status=400)

    muestra_actual = muestras_actuales + 1

    # Guardar registros
    for f in filas:

        # Cantidad (ya viene como promedio o valor único)
        try:
            cantidad = float(f.get('cantidad'))
        except (ValueError, TypeError):
            cantidad = None

        # Ref solo aplica a Deshoje
        try:
            ref = int(f.get('ref')) if f.get('ref') else None
        except (ValueError, TypeError):
            ref = None

        supervisionfito.objects.create(
            fecha=f.get('fecha'),
            muestra=muestra_actual,
            cantidad=cantidad,
            ref=ref,
            zona=f.get('zona'),
            finca=f.get('area'),
            actividad=f.get('actividad'),
            estructura=f.get('estructura'),
            cultivo=f.get('cultivo'),
            supervisor=f.get('supervisor'),
            observaciones=f.get('observaciones'),
            status='Abierta'
        )

    return JsonResponse({
        'msm': f'Se registró correctamente la muestra {muestra_actual}',
        'muestra': muestra_actual,
        'completo': muestra_actual == muestralimite
    })

def evaluar_cobertura(dato):

    try:
        dato = float(dato)
    except (TypeError, ValueError):
        return '-', 'secondary'

    if dato == 200:
        return 'M', 'red'
    elif 70 <= dato <= 100:
        return 'E', 'green'
    elif 0 <= dato <= 30:
        return 'B', 'yellow'
    else:
        return '-', 'secondary'  # 👈 clave

def evaluar_tizon(dato):

    try:
        dato = float(dato)
    except (TypeError, ValueError):
        return '-', 'secondary'

    if dato == 0:
        return 'E', 'green'
    elif 0 < dato <= 2:
        return 'B', 'yellow'
    elif dato > 2:
        return 'M', 'red'
    else:
        return '-', 'secondary'  # 

def reporte_seguimiento_api_fito(request):
    finca = request.GET.get('finca')
    estructura = request.GET.get('estructura')
    zona = request.GET.get('zona')
    actividad = request.GET.get('actividad')
    cultivo = request.GET.get('cultivo')
    semana = request.GET.get('semana')
    año = request.GET.get('anio')  # <-- Nuevo parámetro

    # Convertir semana y año a enteros
    try:
        semana = int(semana)
    except (TypeError, ValueError):
        semana = None

    try:
        año = int(año)
    except (TypeError, ValueError):
        año = None

    queryset = supervisionfito.objects.filter(
        finca=finca,
        estructura=estructura,
        zona=zona,
        actividad=actividad,
        cultivo=cultivo
    ).annotate(
        semana=ExtractWeek('fecha'),
        anio=ExtractYear('fecha')  # <-- Extraemos el año
    ).exclude(status='Anulado')

    # Filtrar por semana y año si se proporcionan
    if semana:
        queryset = queryset.filter(semana=semana)
    if año:
        queryset = queryset.filter(anio=año)

    muestras = list(queryset.order_by('fecha','muestra').values('muestra','cantidad'))

    cantidades_validas = [m['cantidad'] for m in muestras if m['cantidad'] is not None]
    promedio = sum(cantidades_validas) / len(cantidades_validas) if cantidades_validas else 0

    return JsonResponse({'muestras': muestras, 'promedio': promedio})

def reporte_general_fito(request):
    # Funciones de semáforo
    # 👇 Filtros
    estructura = request.GET.get('estructura')
    zona = request.GET.get('zona')
    actividad = request.GET.get('actividad')
    finca = request.GET.get('finca')
    cultivo = request.GET.get('cultivo')
    # ===============================
    # DETERMINAR ÁREA SEGÚN USUARIO
    # ===============================
    user = request.user.username.lower() 
    if user == 'cosecha.rio@popoyan.com.gt' or user=='jorge.cruz@popoyan.com.gt':
        area = 'RIO'
    elif user == 'cosecha.valle@popoyan.com.gt' or user =='cosecha.valle2@popoyan.com.gt' or user =='linday.solares@popoyan.com.gt':
        area = 'VALLE'
    else:
        area = 'ALL'

    # ===============================
    # QUERY BASE n jnd  Queryset base
    qs = supervisionfito.objects.exclude(status='Anulado')
    # Filtrar por área si no es ALL
    if area != 'ALL':
        qs = qs.filter(finca=area)  # Aquí se filtra por finca
    if estructura: qs = qs.filter(estructura=estructura)
    if zona: qs = qs.filter(zona=zona)
    if actividad: qs = qs.filter(actividad=actividad)
    if finca: qs = qs.filter(finca=finca)
    if cultivo: qs = qs.filter(cultivo=cultivo)

    # 👇 Agregar semana y año
    qs = qs.annotate(
        semana=ExtractWeek('fecha'),
        anio=ExtractYear('fecha')
    )

    rows = qs.values(
        'anio',
        'semana',
        'estructura',
        'zona',
        'actividad',
        'finca',
        'cultivo'
    ).annotate(
        prom=Avg('cantidad'),
        ref=Avg('ref')
    ).order_by('anio', 'semana','estructura')

    # Construir lista de dicts para pivot

    data = []

    for row in rows:
        if row['actividad'] == 'Cobertura':
            letra, color = evaluar_cobertura(row['prom'])
        else:
            letra, color = evaluar_tizon(row['prom'])

        data.append({
            'estructura': row['estructura'],
            'zona': row['zona'],
            'actividad': row['actividad'],
            'finca': row['finca'],
            'cultivo': row['cultivo'],

            # 🔑 clave para el pivot
            'semana': f"{row['semana']}-{str(row['anio'])[-2:]}",
            'semana_num': row['semana'],
            'anio': row['anio'],

            'letra': letra,
            'color': color
        })

    return JsonResponse(data, safe=False)

def reporte_semanal_supervision_fito(request):

    # ===============================
    # PARÁMETROS FILTROS
    # ===============================
    estructura = request.GET.get('estructura')
    zona = request.GET.get('zona')
    actividad_filtro = request.GET.get('actividad')
    cultivo = request.GET.get('cultivo')
    
    finca = request.GET.get('finca')

    # ===============================
    # DETERMINAR ÁREA SEGÚN USUARIO
    # ===============================
    user = request.user.username.lower() 
    if user == 'cosecha.rio@popoyan.com.gt' or user=='jorge.cruz@popoyan.com.gt':
        area = 'RIO'
    elif user == 'cosecha.valle@popoyan.com.gt' or user =='cosecha.valle2@popoyan.com.gt' or user =='linday.solares@popoyan.com.gt':
        area = 'VALLE'
    else:
        if finca:
            area=finca
        else:
            area = 'ALL'

    # ===============================
    # QUERY BASE
    # ===============================
    qs = supervisionfito.objects.exclude(status='Anulado')

    # Filtrar por área si no es ALL
    if area != 'ALL':
        qs = qs.filter(finca=area)  # Aquí se filtra por finca

    # ===============================
    # FILTROS OPCIONALES
    # ===============================
    if estructura:
        qs = qs.filter(estructura=estructura)
    if zona:
        qs = qs.filter(zona=zona)
    if cultivo:
        qs = qs.filter(cultivo=cultivo)
    if actividad_filtro:
        qs = qs.filter(actividad=actividad_filtro)

    # ===============================
    # SEMANA / AÑO
    # ===============================
    qs = qs.annotate(
        semana=ExtractWeek('fecha'),
        anio=ExtractYear('fecha')
    ).order_by('estructura', 'zona', 'actividad')
    # Obtener año máximo
    max_anio = qs.aggregate(max_anio=Max('anio'))['max_anio']
    # Luego semana máxima dentro de ese año
    max_semana = qs.filter(anio=max_anio).aggregate(max_semana=Max('semana'))['max_semana']
    qs = qs.filter(anio=max_anio, semana=max_semana)

    # ===============================
    # AGREGAR PROMEDIOS Y FORMATEAR JSON
    # ===============================
    rows = qs.values(
        'actividad', 'finca', 'zona', 'cultivo', 'estructura', 'semana', 'anio'
    ).annotate(
        prom=Avg('cantidad'),
        ref=Avg('ref')
    )

    data = []
    for row in rows:
        prom = round(row['prom'], 2)
        ref = row['ref']

        if row['actividad'] == 'Cobertura':
            letra, color = evaluar_cobertura(prom)
        else:
            letra, color = evaluar_tizon(prom)

        data.append({
            'actividad': row['actividad'],
            'finca': row['finca'],  # Esto ahora corresponde a RIO o VALLE
            'zona': row['zona'],
            'cultivo': row['cultivo'],
            'estructura': row['estructura'],
            'semana': f"Semana {row['semana']}-{row['anio']}",
            'semana_num': row['semana'],
            'anio': row['anio'],
            'letra': letra,
            'color': color,
            'promedio': prom
        })

    return JsonResponse(data, safe=False)

def supervisionfito_detalle(request, fecha, cultivo, estructura, actividad, zona,finca):

    registros = supervisionfito.objects.filter(
        fecha=fecha,
        cultivo=cultivo,
        estructura=estructura,
        zona=zona,
        finca=finca,
        actividad=actividad
    ).exclude(status='Anulado').order_by('muestra', 'actividad')

    muestras = defaultdict(list)
    for r in registros:
        muestras[r.muestra].append(r)

    return render(request, 'plantaE/supervisionfito/supervisionfito_detalle.html', {
        'fecha': fecha,
        'cultivo': cultivo,
        'estructura': estructura,
        'zona': zona,
        'finca': finca,
        'muestras': dict(muestras)
    })


def reporte_semanal_view_fito(request):
    user = request.user.username

    if user == 'cosecha.rio@popoyan.com.gt' or user=='jorge.cruz@popoyan.com.gt':
        area = 'RIO'
    elif user == 'cosecha.valle@popoyan.com.gt' or user =='cosecha.valle2@popoyan.com.gt' or user =='linday.solares@popoyan.com.gt':
        area = 'VALLE'
    else:
        area = 'ALL'  # gerencial
    return render(request, 'plantaE/supervisionfito/supervisionfitoreporte.html', {'area_usuario': area,'user':user})

def reporte_semanal_seguimiento_fito(request):
    user = request.user.username

    if user == 'cosecha.rio@popoyan.com.gt' or user=='jorge.cruz@popoyan.com.gt':
        area = 'RIO'
    elif user == 'cosecha.valle@popoyan.com.gt' or user =='cosecha.valle2@popoyan.com.gt' or user =='linday.solares@popoyan.com.gt':
        area = 'VALLE'
    else:
        area = 'ALL'  # gerencial

    return render(request, 'plantaE/supervisionfito/supervisionfito_seguimiento.html', {'area_usuario': area,'user':user})



