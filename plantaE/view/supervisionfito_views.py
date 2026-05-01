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

from django.core.files.storage import FileSystemStorage

#from django.views.generic import TemplateView

import cv2
import numpy as np
import base64

def _order_points(pts):
    pts = pts.astype(np.float32)
    s = pts.sum(axis=1)
    d = np.diff(pts, axis=1)
    rect = np.zeros((4, 2), dtype=np.float32)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    rect[1] = pts[np.argmin(d)]
    rect[3] = pts[np.argmax(d)]
    return rect

def _to_base64_png(img_gray_or_bgr):
    ok, buf = cv2.imencode(".png", img_gray_or_bgr)
    if not ok:
        return None
    return base64.b64encode(buf).decode("utf-8")

def _decode_upload_to_bgr(uploaded_file):
    """
    Convierte UploadedFile -> np.ndarray BGR sin guardar a disco.
    Usa chunks() para no reventar memoria con archivos grandes. [1](https://docs.djangoproject.com/en/6.0/ref/files/uploads/)
    """
    # Lee bytes (chunks para robustez)
    data = bytearray()
    for chunk in uploaded_file.chunks():
        data.extend(chunk)

    nparr = np.frombuffer(data, np.uint8)  # numpy.frombuffer [4](https://numpy.org/doc/stable/reference/generated/numpy.frombuffer.html)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)  # cv2.imdecode desde bytes [3](https://www.geeksforgeeks.org/python/python-opencv-imdecode-function/)
    return img

def _detect_card_quad_edges(img_bgr, pad=60, canny1=50, canny2=150):
    """
    ROI por amarillo para acotar + bordes para rectángulo.
    """
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    y = cv2.inRange(hsv, np.array([12,50,50], np.uint8), np.array([45,255,255], np.uint8))

    k = cv2.getStructuringElement(cv2.MORPH_RECT, (9,9))
    y = cv2.morphologyEx(y, cv2.MORPH_CLOSE, k, iterations=2)
    y = cv2.morphologyEx(y, cv2.MORPH_OPEN, k, iterations=1)

    ys, xs = np.where(y > 0)
    if len(xs) == 0:
        return None

    x0, x1 = xs.min(), xs.max()
    y0, y1 = ys.min(), ys.max()

    x0 = max(0, x0 - pad); y0 = max(0, y0 - pad)
    x1 = min(img_bgr.shape[1]-1, x1 + pad)
    y1 = min(img_bgr.shape[0]-1, y1 + pad)

    roi = img_bgr[y0:y1+1, x0:x1+1].copy()

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5,5), 0)
    edges = cv2.Canny(gray, canny1, canny2)

    ke = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    edges2 = cv2.dilate(edges, ke, iterations=1)
    edges2 = cv2.morphologyEx(edges2, cv2.MORPH_CLOSE, ke, iterations=2)

    contours, _ = cv2.findContours(edges2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None

    c = max(contours, key=cv2.contourArea)
    rect = cv2.minAreaRect(c)
    quad = cv2.boxPoints(rect).astype(np.float32)
    quad = _order_points(quad)

    quad[:,0] += x0
    quad[:,1] += y0
    return quad

def analyze_card_bytes(uploaded_file, paper_dim_mm=(30,20), px_per_mm=20, margin_mm=2.0):
    """
    Devuelve dict listo para el template:
    - coverage (%)
    - density (gotas/cm²)
    - mask_base64 (centros/picos)
    - stain_base64 (área húmeda)
    - overlay_base64 (warp + centros)
    """
    img = _decode_upload_to_bgr(uploaded_file)
    if img is None:
        return {"error": "No se pudo decodificar la imagen (bytes no válidos)."}

    quad = _detect_card_quad_edges(img)
    if quad is None:
        return {"error": "No se pudo detectar la tarjeta (amarillo/bordes)."}

    # Warp a 3×2 cm
    L_mm, W_mm = paper_dim_mm
    Wpx = int(round(L_mm * px_per_mm))
    Hpx = int(round(W_mm * px_per_mm))
    dst = np.array([[0,0],[Wpx-1,0],[Wpx-1,Hpx-1],[0,Hpx-1]], dtype=np.float32)
    M = cv2.getPerspectiveTransform(_order_points(quad), dst)
    warp = cv2.warpPerspective(img, M, (Wpx, Hpx), flags=cv2.INTER_LINEAR)

    # 1) Mancha (coverage) con Otsu en gris (invertido)
    gray = cv2.cvtColor(warp, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3,3), 0)
    _, stain = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Quitar padding negro del warp (si hubiera)
    valid = (gray > 10).astype(np.uint8) * 255
    stain = cv2.bitwise_and(stain, valid)

    # Margen interior (2 mm)
    margin_px = int(round(margin_mm * px_per_mm))
    inner = np.zeros_like(stain)
    inner[margin_px:Hpx-margin_px, margin_px:Wpx-margin_px] = 255
    stain = cv2.bitwise_and(stain, inner)

    coverage = round(100.0 * cv2.countNonZero(stain) / (Wpx * Hpx), 2)

    # 2) Centros de gotas (density) con distance transform
    dist = cv2.distanceTransform(stain, cv2.DIST_L2, 5)
    dist_norm = cv2.normalize(dist, None, 0, 1.0, cv2.NORM_MINMAX)

    # Picos: umbral (ajustable 0.35–0.45)
    _, peaks = cv2.threshold(dist_norm, 0.40, 1.0, cv2.THRESH_BINARY)
    peaks = (peaks * 255).astype(np.uint8)
    peaks = cv2.dilate(peaks, np.ones((3,3), np.uint8), iterations=1)

    # Contar componentes conectados (cada pico ~ una gota)
    num_labels, _ = cv2.connectedComponents(peaks)
    droplet_count = max(0, num_labels - 1)

    card_area_cm2 = (L_mm/10.0) * (W_mm/10.0)  # 3×2cm = 6 cm²
    density = round(droplet_count / card_area_cm2, 2)

    # Overlay para QA
    overlay = warp.copy()
    cnts, _ = cv2.findContours(peaks, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in cnts:
        M = cv2.moments(c)
        if M["m00"] > 0:
            cx = int(M["m10"]/M["m00"])
            cy = int(M["m01"]/M["m00"])
            cv2.circle(overlay, (cx, cy), 3, (0,0,255), -1)

    note = "OK"
    if coverage >= 20:
        note = "Cobertura alta: la densidad puede subestimarse por solapes; prioriza cobertura."

    return {
        "coverage": coverage,
        "density": density,
        "droplet_count": droplet_count,
        "note": note,
        "mask_base64": _to_base64_png(peaks),
        "stain_base64": _to_base64_png(stain),
        "overlay_base64": _to_base64_png(overlay),
    }

def upload_card(request):
    
    result = None
    if request.method == "POST" and request.FILES.get("image"):
        result = analyze_card_bytes(request.FILES["image"])

        return render(
            request,
            "plantaE/supervisionfito/detecciontarjetahidro.html",
            {"result": result}
        )

    return render(request, "plantaE/supervisionfito/detecciontarjetahidro.html")

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


        supervisionfito.objects.create(
            fecha=f.get('fecha'),
            muestra=muestra_actual,
            cantidad=cantidad,
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
        
    if 70 <= dato <= 100:
        return 'E', 'green'
    elif 0 <= dato <= 30:
        return 'B', 'yellow'
    else:
        return 'M', 'red'  # 👈 clave

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
    
    now = datetime.datetime.now()
    fecha = now.date()
    año= fecha.year
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

    # Determinar letra y color según actividad
    if actividad.lower() == 'cobertura':
        letra, color = evaluar_cobertura(promedio)
    elif actividad.lower() == 'tizón':
        letra, color = evaluar_tizon(promedio)
    else:
        letra, color = '-', 'secondary'

    return JsonResponse({'muestras': muestras, 'promedio': promedio, 'letra': letra, 'color': color})

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
        prom=Avg('cantidad')

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
        prom=Avg('cantidad')
    )

    data = []
    for row in rows:
        prom = round(row['prom'], 2)

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



