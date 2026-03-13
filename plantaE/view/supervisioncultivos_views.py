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
import json
from django.db import transaction

# modelos
from plantaE.models import (
    supervision,
    supervisionproduccion,
    usuariosAppFruta
)

#from django.views.generic import TemplateView

  
def supervisiontomates_create(request):
    user = request.user.username

    if user == 'cosecha.rio@popoyan.com.gt':
        area = 'RIO'
    elif user == 'cosecha.valle@popoyan.com.gt' or user =='cosecha.valle2@popoyan.com.gt' or user =='linday.solares@popoyan.com.gt':
        area = 'VALLE'
    else:
        area = 'ALL'  # gerencial

    return render(request, 'plantaE/supervisiontomates_formPlantilla.html',{
        'area_usuario': area,'user':user
    })

def supervisionchiles_create(request):

    return render(request, 'plantaE/supervisionchiles_formPlantilla.html')

def supervision_create(request):

    return render(request, 'plantaE/supervision_formPlantilla.html')

def supervision_delete(request, pk):

    salidas = get_object_or_404(supervision, pk=pk)
    
    if request.method == 'POST':
        salidas.status = 'Anulado'
        salidas.save() 
        
        return render(request, 'plantaE/supervision_confirm_delete.html', {
            'alert_message': "El registro fue anulado correctamente.",
            'redirect_url': reverse('supervision_list')
        })
    return render(request, 'plantaE/supervision_confirm_delete.html', {'registros': salidas})

def supervision_list(request):
    #today = timezone.now().date()
    #salidas = Recepciones.objects.filter(fecha=today)
    nombre_usuario = request.user.username
    
    datos = usuariosAppFruta.objects.filter(correo=nombre_usuario).values('encargado')
    supervisor = list(datos)[0]['encargado']
    hoy = timezone.now().date()

    # Lunes de la semana actual
    inicio_semana = hoy - datetime.timedelta(days=hoy.weekday())
    # Domingo de la semana actual
    fin_semana = inicio_semana + datetime.timedelta(days=6)
    salidas = supervision.objects.filter(
        supervisor=supervisor,
        fecha__range=(inicio_semana, fin_semana)
    ).exclude(
        status='Anulado'
    ).order_by('-id','estructura','cultivo','zona')

    

    return render(request, 'plantaE/supervision_list.html', {'registros': salidas})

def supervisionproduccion_list(request):

    hoy = timezone.now().date()

    user = request.user.username

    if user == 'cosecha.rio@popoyan.com.gt' or user=='jorge.cruz@popoyan.com.gt':
        area = 'RIO'
    elif user == 'cosecha.valle@popoyan.com.gt' or user =='cosecha.valle2@popoyan.com.gt' or user =='linday.solares@popoyan.com.gt':
        area = 'VALLE'
    else:
        area = 'ALL'  # gerencial

    # Lunes de la semana actual
    inicio_semana = hoy - datetime.timedelta(days=hoy.weekday())
    # Domingo de la semana actual
    fin_semana = inicio_semana + datetime.timedelta(days=6)
    lotes = (
        supervisionproduccion.objects
        .filter(
            status='Abierta',
            fecha__range=(inicio_semana, fin_semana)
        )
        .values(
            'fecha',
            'finca',
            'cultivo',
            'estructura',
            'zona'
        )
        .annotate(
            total_muestras=Count('muestra', distinct=True),
            ultima_muestra=Max('muestra')
        )
        .order_by('-fecha')
    )

    if area != 'ALL':
        lotes = lotes.filter(finca=area)

    return render(request, 'plantaE/supervisionproduccion_list.html', {
        'lotes': lotes,'area_usuario': area,'user':user
    })

def reporte_semanal_view(request):
    user = request.user.username

    if user == 'cosecha.rio@popoyan.com.gt' or user=='jorge.cruz@popoyan.com.gt':
        area = 'RIO'
    elif user == 'cosecha.valle@popoyan.com.gt' or user =='cosecha.valle2@popoyan.com.gt' or user =='linday.solares@popoyan.com.gt':
        area = 'VALLE'
    else:
        area = 'ALL'  # gerencial
    return render(request, 'plantaE/supervisionproduccionreporte.html', {'area_usuario': area,'user':user})

def reporte_semanal_seguimiento(request):
    user = request.user.username

    if user == 'cosecha.rio@popoyan.com.gt' or user=='jorge.cruz@popoyan.com.gt':
        area = 'RIO'
    elif user == 'cosecha.valle@popoyan.com.gt' or user =='cosecha.valle2@popoyan.com.gt' or user =='linday.solares@popoyan.com.gt':
        area = 'VALLE'
    else:
        area = 'ALL'  # gerencial

    return render(request, 'plantaE/supervisionproduccion_seguimiento.html', {'area_usuario': area,'user':user})

def evaluar_deshoje(promedio, ref):
        diff = abs(promedio - ref)
        if diff <= 0.5: return ('E', 'green')
        elif diff <= 1: return ('B', 'yellow')
        elif diff <= 1.5: return ('R', 'orange')
        else: return ('M', 'red')

def evaluar_ganchos(prom):
    if 14.5 <= prom <= 15.5: return ('E', 'green')
    elif 15.5 <= prom < 16: return ('B', 'yellow')
    elif 14.0 <= prom < 14.5: return ('B', 'yellow')
    elif 13.5 <= prom < 14: return ('R', 'orange')
    elif 16 <= prom < 16.5: return ('R', 'orange')
    else: return ('M', 'red')

def evaluar_descoronado(prom):
    if 0 <= prom < 1.5: return ('E', 'green')
    elif 1.5 <= prom < 2.5: return ('B', 'yellow')
    elif 2.5 <= prom < 3.5: return ('R', 'orange')
    else: return ('M', 'red')

def reporte_general(request):
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
    qs = supervisionproduccion.objects.exclude(status='Anulado')
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

    # 👇 Construir lista de dicts para pivot
    data = []
    for row in rows:
        if row['actividad'] == 'Deshoje':
            letra, color = evaluar_deshoje(row['prom'], row['ref'])
        elif row['actividad'] == 'Ganchos':
            letra, color = evaluar_ganchos(row['prom'])
        else:
            letra, color = evaluar_descoronado(row['prom'])

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

def reporte_semanal_supervision(request):

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
    qs = supervisionproduccion.objects.exclude(status='Anulado')

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

        if row['actividad'] == 'Deshoje':
            letra, color = evaluar_deshoje(prom, ref)
        elif row['actividad'] == 'Ganchos':
            letra, color = evaluar_ganchos(prom)
        else:
            letra, color = evaluar_descoronado(prom)

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

def reporte_seguimiento_api(request):
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

    queryset = supervisionproduccion.objects.filter(
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

    muestras = list(queryset.order_by('fecha','muestra').values('muestra','cantidad','ref'))

    cantidades_validas = [m['cantidad'] for m in muestras if m['cantidad'] is not None]
    promedio = sum(cantidades_validas) / len(cantidades_validas) if cantidades_validas else 0

    letra, color = ('','')
    if actividad == 'Deshoje':
        ref_avg = queryset.aggregate(ref_avg=Avg('ref'))['ref_avg'] or 0
        diff = abs(promedio - ref_avg)
        if diff <= 0.5: letra, color = 'E','green'
        elif diff <= 1: letra, color = 'B','yellow'
        elif diff <= 1.5: letra, color = 'R','orange'
        else: letra, color = 'M','red'

    return JsonResponse({'muestras': muestras, 'promedio': promedio, 'letra': letra, 'color': color})
@transaction.atomic
def supervision_grabar(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        filas = data.get('array', [])

        for f in filas:
            supervision.objects.create(
                fecha=f['fecha'],
                regla=f['regla'],
                cumplimiento=f['cumplimiento'],
                area=f['area'],
                estructura=f['estructura'],
                cultivo=f['cultivo'],
                supervisor=f['supervisor'],
                observaciones=f['observaciones'],
                status=f['status']
            )

        return JsonResponse({
            'msm': f'Se guardaron {len(filas)} registros correctamente'
        })

def supervisionproduccion_delete(request, pk):

    salidas = get_object_or_404(supervisionproduccion, pk=pk)
    
    if request.method == 'POST':
        registros = supervisionproduccion.objects.filter(
            fecha=salidas.fecha,
            zona=salidas.zona,
            estructura=salidas.estructura,
            supervisor=salidas.supervisor,
            cultivo=salidas.cultivo,
            muestra=salidas.muestra
        )

        # Marcamos como 'Anulado'
        count = registros.update(status='Anulado')
        
        
        return render(request, 'plantaE/supervisionproduccion_confirm_delete.html', {
            'alert_message': f'Se anularon {count} registros correctamente',
            'redirect_url': reverse('supervisionproduccion_list')
        })
    
    return render(request, 'plantaE/supervisionproduccion_confirm_delete.html', {'registros': salidas})

def supervisionproduccion_detalle(request, fecha, cultivo, estructura, zona,finca):

    registros = supervisionproduccion.objects.filter(
        fecha=fecha,
        cultivo=cultivo,
        estructura=estructura,
        zona=zona,
        finca=finca
    ).exclude(status='Anulado').order_by('muestra', 'actividad')

    muestras = defaultdict(list)
    for r in registros:
        muestras[r.muestra].append(r)

    return render(request, 'plantaE/supervisionproduccion_detalle.html', {
        'fecha': fecha,
        'cultivo': cultivo,
        'estructura': estructura,
        'zona': zona,
        'finca': finca,
        'muestras': dict(muestras)
    })
@transaction.atomic
def supervisionproduccion_grabar(request):
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
        'status': 'Abierta'
    }

    # 🔢 ¿Cuántas muestras ya existen?
    muestras_actuales = supervisionproduccion.objects.filter(
        **filtros_lote
    ).values('muestra').distinct().count()

    if muestras_actuales >= 5:
        return JsonResponse({
            'error': 'Este lote ya cuenta con las 10 muestras completas'
        }, status=400)

    muestra_actual = muestras_actuales + 1

    # 📝 Guardar registros
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

        supervisionproduccion.objects.create(
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
        'completo': muestra_actual == 5
    })
