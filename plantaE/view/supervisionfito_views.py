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
import os
from django.conf import settings
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# -------------------------
# Utilidades geométricas
# -------------------------
def _order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    diff = np.diff(pts, axis=1)
    rect[0] = pts[np.argmin(s)]      # top-left
    rect[2] = pts[np.argmax(s)]      # bottom-right
    rect[1] = pts[np.argmin(diff)]   # top-right
    rect[3] = pts[np.argmax(diff)]   # bottom-left
    return rect

def _find_card_quad(img_bgr):
    """
    Detecta la tarjeta por su color amarillo en HSV y devuelve el cuadrilátero (4 puntos).
    """
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

    # Amarillo típico de WSP (ajustable si hace falta)
    lower_yellow = np.array([12, 50, 50], dtype=np.uint8)
    upper_yellow = np.array([45, 255, 255], dtype=np.uint8)

    card_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Cierre para rellenar huecos, apertura para limpiar ruido
    k = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    card_mask = cv2.morphologyEx(card_mask, cv2.MORPH_CLOSE, k, iterations=2)
    card_mask = cv2.morphologyEx(card_mask, cv2.MORPH_OPEN, k, iterations=1)

    contours, _ = cv2.findContours(card_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None, card_mask

    c = max(contours, key=cv2.contourArea)
    if cv2.contourArea(c) < 3000:
        return None, card_mask

    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)

    if len(approx) == 4:
        quad = _order_points(approx.reshape(4, 2).astype("float32"))
        return quad, card_mask

    # Fallback: minAreaRect
    rect = cv2.minAreaRect(c)
    box = cv2.boxPoints(rect)
    quad = _order_points(box.astype("float32"))
    return quad, card_mask

def _warp_to_standard(img_bgr, quad, paper_dim_mm=(30, 20), px_per_mm=20):
    """
    Rectifica perspectiva a tamaño estándar en píxeles.
    paper_dim_mm = (largo_mm, ancho_mm)  -> aquí 30x20mm (3x2cm)
    """
    L_mm, W_mm = paper_dim_mm
    # Convertimos a tamaño de imagen objetivo
    Wpx = int(round(L_mm * px_per_mm))  # eje X = largo
    Hpx = int(round(W_mm * px_per_mm))  # eje Y = ancho

    dst = np.array([[0, 0], [Wpx - 1, 0], [Wpx - 1, Hpx - 1], [0, Hpx - 1]], dtype="float32")
    M = cv2.getPerspectiveTransform(quad, dst)
    warp = cv2.warpPerspective(img_bgr, M, (Wpx, Hpx), flags=cv2.INTER_LINEAR)
    return warp, (Wpx, Hpx)

# -------------------------
# Segmentación de gotas
# -------------------------
def _segment_droplets(warp_bgr):
    """
    Segmenta manchas oscuras sobre fondo amarillo.
    Pipeline robusto: normalización + Otsu. [1](https://link.springer.com/article/10.1007/s11042-025-20697-2)
    """
    lab = cv2.cvtColor(warp_bgr, cv2.COLOR_BGR2LAB)
    L, A, B = cv2.split(lab)

    # CLAHE para compensar sombras/iluminación
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    L2 = clahe.apply(L)
    L2 = cv2.medianBlur(L2, 3)

    # Otsu invertido: manchas oscuras -> blanco
    _, mask = cv2.threshold(L2, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Apertura suave para quitar puntitos sin fusionar demasiado
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, k, iterations=1)
    return mask

def _watershed_split(binary_mask):
    """
    Intenta separar manchas pegadas (solapes).
    Ojo: cuando hay alta cobertura, el conteo es incierto por solapes. [3](https://sprayers101.com/assessing_wsp_pt3/)[4](https://upcommons.upc.edu/bitstreams/d2e74f77-44a8-4885-9e55-eb3e9d804624/download)
    """
    mask = (binary_mask > 0).astype(np.uint8) * 255
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

    sure_bg = cv2.dilate(mask, kernel, iterations=2)

    dist = cv2.distanceTransform(mask, cv2.DIST_L2, 5)
    _, sure_fg = cv2.threshold(dist, 0.35 * dist.max(), 255, 0)
    sure_fg = sure_fg.astype(np.uint8)

    unknown = cv2.subtract(sure_bg, sure_fg)

    _, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1
    markers[unknown == 255] = 0

    img3 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    markers = cv2.watershed(img3, markers)

    out = np.zeros_like(mask)
    out[markers > 1] = 255
    return out

# -------------------------
# Métricas por grid (robustez)
# -------------------------
def _trimmed_mean(x, trim=0.10):
    x = np.sort(x)
    k = int(len(x) * trim)
    if len(x) < 2 * k + 1:
        return float(np.mean(x))
    return float(np.mean(x[k:-k]))


def _cv_pct(x):
    m = float(np.mean(x))
    s = float(np.std(x))
    return (s / m) * 100.0 if m > 0 else None


def _grid_metrics(droplet_mask, contours, px_per_mm, tile_cm=0.5, margin_mm=2.0):
    """
    Divide el interior en celdas (tile_cm x tile_cm) y calcula:
    - coverage por celda
    - densidad por celda (gotas/cm²) asignando gota por centroide
    """
    H, W = droplet_mask.shape[:2]
    tile_mm = tile_cm * 10.0
    tile_px = int(round(tile_mm * px_per_mm))
    margin_px = int(round(margin_mm * px_per_mm))

    # ROI interior
    x0, y0 = margin_px, margin_px
    x1, y1 = W - margin_px, H - margin_px
    if x1 <= x0 + tile_px or y1 <= y0 + tile_px:
        # Si el margen “se come” la tarjeta, lo anulamos
        x0, y0, x1, y1 = 0, 0, W, H

    roi = droplet_mask[y0:y1, x0:x1]
    roiH, roiW = roi.shape[:2]

    nx = roiW // tile_px
    ny = roiH // tile_px
    if nx == 0 or ny == 0:
        return None

    roi = roi[:ny * tile_px, :nx * tile_px]

    coverage_grid = np.zeros((ny, nx), dtype=np.float32)
    for j in range(ny):
        for i in range(nx):
            tile = roi[j*tile_px:(j+1)*tile_px, i*tile_px:(i+1)*tile_px]
            coverage_grid[j, i] = 100.0 * (cv2.countNonZero(tile) / (tile_px * tile_px))

    # Densidad por celda: contar gotas por centroide
    density_grid = np.zeros((ny, nx), dtype=np.float32)
    cell_area_cm2 = tile_cm * tile_cm

    for c in contours:
        M = cv2.moments(c)
        if M["m00"] == 0:
            continue
        cx = M["m10"] / M["m00"]
        cy = M["m01"] / M["m00"]

        # Dentro del ROI recortado a grid completo
        if not (x0 <= cx < x0 + nx * tile_px and y0 <= cy < y0 + ny * tile_px):
            continue

        i = int((cx - x0) // tile_px)
        j = int((cy - y0) // tile_px)
        density_grid[j, i] += 1.0

    # Convertir conteo por celda a gotas/cm²
    density_grid = density_grid / cell_area_cm2

    dens_vals = density_grid.flatten()
    cov_vals = coverage_grid.flatten()

    summary = {
        "tile_cm": tile_cm,
        "margin_mm": margin_mm,
        "grid_shape": [int(ny), int(nx)],

        "density_mean": float(np.mean(dens_vals)),
        "density_median": float(np.median(dens_vals)),
        "density_trimmed_mean_10pct": _trimmed_mean(dens_vals, 0.10),
        "density_cv_pct": _cv_pct(dens_vals),

        "coverage_mean": float(np.mean(cov_vals)),
        "coverage_median": float(np.median(cov_vals)),
        "coverage_trimmed_mean_10pct": _trimmed_mean(cov_vals, 0.10),
        "coverage_cv_pct": _cv_pct(cov_vals),
    }

    return {
        "density_grid": density_grid,
        "coverage_grid": coverage_grid,
        "summary": summary
    }


# -------------------------
# FUNCIÓN PRINCIPAL
# -------------------------
def analyze_card(
    image_path,
    paper_dim_mm=(30, 20),   # 3 cm x 2 cm
    px_per_mm=20,            # buena resolución para tarjetas pequeñas
    margin_mm=2.0,           # descartar borde interno
    tile_cm=0.5,             # micro-grid recomendado para 2x3 cm
    min_diam_um=50,          # filtro físico de ruido
    use_watershed=True,
    save_debug=True
):
    """
    Devuelve:
    - coverage_global (% en toda la tarjeta)
    - density_global (gotas/cm² en toda la tarjeta) [menos robusto]
    - density_robust (mediana por grid) [recomendado]
    - métricas de uniformidad (CV)
    - histograma de tamaños (mancha) y mapas de calor
    """

    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"No se pudo leer la imagen: {image_path}")

    quad, card_mask = _find_card_quad(img)
    if quad is None:
        return {
            "error": "No se pudo detectar la tarjeta (amarillo). Prueba con mejor luz/encuadre o ajusta HSV.",
            "coverage": None, "density": None
        }

    warp, (Wpx, Hpx) = _warp_to_standard(img, quad, paper_dim_mm=paper_dim_mm, px_per_mm=px_per_mm)

    droplet_mask = _segment_droplets(warp)

    if use_watershed:
        droplet_mask = _watershed_split(droplet_mask)

    # Área real (cm²): 3x2 cm = 6 cm²
    L_mm, W_mm = paper_dim_mm
    card_area_cm2 = (L_mm / 10.0) * (W_mm / 10.0)

    # Cobertura global (% sobre toda la tarjeta ya rectificada)
    stained_px = int(cv2.countNonZero(droplet_mask))
    total_px = int(Wpx * Hpx)
    coverage = round((stained_px / total_px) * 100.0, 2)

    # Contornos y filtro físico por tamaño mínimo
    contours, _ = cv2.findContours(droplet_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    mm_per_px = 1.0 / px_per_mm
    mm2_per_px = mm_per_px ** 2

    min_diam_mm = min_diam_um / 1000.0
    min_area_mm2 = np.pi * (min_diam_mm / 2.0) ** 2
    min_area_px = min_area_mm2 / mm2_per_px

    kept = []
    areas_px = []
    for c in contours:
        a = cv2.contourArea(c)
        if a >= min_area_px:
            kept.append(c)
            areas_px.append(a)

    droplet_count = len(kept)
    density_global = round(droplet_count / card_area_cm2, 2)

    # Diámetro equivalente de MANCHA en µm (para histograma)
    areas_mm2 = np.array(areas_px, dtype=np.float64) * mm2_per_px
    diams_mm = 2.0 * np.sqrt(areas_mm2 / np.pi)
    diams_um = diams_mm * 1000.0

    stats = {
        "mean_um": float(diams_um.mean()) if diams_um.size else None,
        "median_um": float(np.median(diams_um)) if diams_um.size else None,
        "p10_um": float(np.percentile(diams_um, 10)) if diams_um.size else None,
        "p90_um": float(np.percentile(diams_um, 90)) if diams_um.size else None,
        "min_um": float(diams_um.min()) if diams_um.size else None,
        "max_um": float(diams_um.max()) if diams_um.size else None,
    }

    # Grid robusto (recomendado)
    grid = _grid_metrics(droplet_mask, kept, px_per_mm=px_per_mm, tile_cm=tile_cm, margin_mm=margin_mm)
    density_robust = None
    if grid is not None:
        density_robust = round(grid["summary"]["density_median"], 2)

    # Guardar outputs
    base = os.path.basename(image_path)
    name, _ = os.path.splitext(base)

    warp_filename = f"warp_{name}.png"
    mask_filename = f"mask_{name}.png"
    overlay_filename = f"overlay_{name}.png"
    hist_filename = f"hist_{name}.png"
    heat_density_filename = f"heat_density_{name}.png"
    heat_coverage_filename = f"heat_coverage_{name}.png"

    if save_debug:
        cv2.imwrite(os.path.join(settings.MEDIA_ROOT, warp_filename), warp)
        cv2.imwrite(os.path.join(settings.MEDIA_ROOT, mask_filename), droplet_mask)

        overlay = warp.copy()
        cv2.drawContours(overlay, kept, -1, (0, 0, 255), 1)
        cv2.imwrite(os.path.join(settings.MEDIA_ROOT, overlay_filename), overlay)

        # Histograma de diámetros (mancha)
        plt.figure()
        if diams_um.size:
            plt.hist(diams_um, bins=25)
            plt.title("Histograma de diámetros equivalentes de mancha (µm)")
            plt.xlabel("Diámetro equivalente (µm)")
            plt.ylabel("Frecuencia")
        else:
            plt.text(0.5, 0.5, "Sin gotas detectadas", ha="center", va="center")
            plt.axis("off")
        plt.tight_layout()
        plt.savefig(os.path.join(settings.MEDIA_ROOT, hist_filename), dpi=150)
        plt.close()

        # Heatmaps (densidad y cobertura por grid)
        if grid is not None:
            # Densidad
            plt.figure()
            plt.imshow(grid["density_grid"], aspect="auto")
            plt.colorbar(label="gotas/cm²")
            plt.title(f"Mapa de calor densidad (tile={tile_cm}cm, margen={margin_mm}mm)")
            plt.tight_layout()
            plt.savefig(os.path.join(settings.MEDIA_ROOT, heat_density_filename), dpi=150)
            plt.close()

            # Cobertura
            plt.figure()
            plt.imshow(grid["coverage_grid"], aspect="auto")
            plt.colorbar(label="% cobertura")
            plt.title(f"Mapa de calor cobertura (tile={tile_cm}cm, margen={margin_mm}mm)")
            plt.tight_layout()
            plt.savefig(os.path.join(settings.MEDIA_ROOT, heat_coverage_filename), dpi=150)
            plt.close()

    result = {
        "coverage": coverage,  # % global (robusto)
        "droplet_count": droplet_count,
        "density_global": density_global,       # total/área (menos robusto si hay solapes)
        "density_robust": density_robust,       # MEDIANA por grid (recomendado)
        "card_area_cm2": round(card_area_cm2, 2),
        "diameter_stats_um_stain": stats,       # tamaños de MANCHA (no gota real)
        "grid_summary": grid["summary"] if grid is not None else None,

        "warp_url": settings.MEDIA_URL + warp_filename if save_debug else None,
        "mask_url": settings.MEDIA_URL + mask_filename if save_debug else None,
        "overlay_url": settings.MEDIA_URL + overlay_filename if save_debug else None,
        "hist_url": settings.MEDIA_URL + hist_filename if save_debug else None,
        "heat_density_url": settings.MEDIA_URL + heat_density_filename if (save_debug and grid is not None) else None,
        "heat_coverage_url": settings.MEDIA_URL + heat_coverage_filename if (save_debug and grid is not None) else None,
    }

    # Recomendación automática (solo orientativa) sobre fiabilidad del conteo
    # A coberturas altas, el conteo se vuelve sensible por solapes. [3](https://sprayers101.com/assessing_wsp_pt3/)[4](https://upcommons.upc.edu/bitstreams/d2e74f77-44a8-4885-9e55-eb3e9d804624/download)
    if coverage is not None and coverage >= 20:
        result["note"] = "Cobertura alta: el conteo de gotas puede estar subestimado por solapes. Prioriza coverage% y densidad robusta."
    else:
        result["note"] = "Cobertura moderada/baja: coverage% y densidad robusta suelen ser consistentes."

    return result


def upload_card(request):
    if request.method == "POST" and request.FILES.get("image"):
        img = request.FILES["image"]

        fs = FileSystemStorage()
        filename = fs.save(img.name, img)
        img_path = fs.path(filename)

        result = analyze_card(img_path)

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



