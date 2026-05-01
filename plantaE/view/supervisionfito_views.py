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

# ----------------------------
# Utilidades
# ----------------------------
def _order_points(pts):
    pts = pts.astype(np.float32)
    s = pts.sum(axis=1)
    d = np.diff(pts, axis=1)
    rect = np.zeros((4, 2), dtype=np.float32)
    rect[0] = pts[np.argmin(s)]      # TL
    rect[2] = pts[np.argmax(s)]      # BR
    rect[1] = pts[np.argmin(d)]      # TR
    rect[3] = pts[np.argmax(d)]      # BL
    return rect


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


# ----------------------------
# 1) Detectar rectángulo por BORDES, partiendo de ROI por amarillo
# ----------------------------
def _detect_card_quad_edges(img_bgr, pad=60, canny1=50, canny2=150):
    """
    - Usa amarillo SOLO para acotar ROI.
    - Dentro del ROI detecta el rectángulo por bordes (Canny + contornos).
    Devuelve: quad (4 puntos en coordenadas globales), edges_roi, edges_roi_closed.
    """
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

    # Amarillo típico WSP (solo para ROI)
    lower_y = np.array([12, 50, 50], np.uint8)
    upper_y = np.array([45, 255, 255], np.uint8)
    y = cv2.inRange(hsv, lower_y, upper_y)

    k = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    y = cv2.morphologyEx(y, cv2.MORPH_CLOSE, k, iterations=2)
    y = cv2.morphologyEx(y, cv2.MORPH_OPEN, k, iterations=1)

    ys, xs = np.where(y > 0)
    if len(xs) == 0:
        return None, None, None

    x0, x1 = xs.min(), xs.max()
    y0, y1 = ys.min(), ys.max()

    x0 = max(0, x0 - pad); y0 = max(0, y0 - pad)
    x1 = min(img_bgr.shape[1] - 1, x1 + pad)
    y1 = min(img_bgr.shape[0] - 1, y1 + pad)

    roi = img_bgr[y0:y1+1, x0:x1+1].copy()

    # Bordes
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(gray, canny1, canny2)

    # Cerrar huecos para contorno sólido
    ke = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    edges2 = cv2.dilate(edges, ke, iterations=1)
    edges2 = cv2.morphologyEx(edges2, cv2.MORPH_CLOSE, ke, iterations=2)

    contours, _ = cv2.findContours(edges2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None, edges, edges2

    H, W = roi.shape[:2]
    min_area = 0.10 * (H * W)

    quad = None
    for c in sorted(contours, key=cv2.contourArea, reverse=True):
        if cv2.contourArea(c) < min_area:
            continue
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            quad = approx.reshape(4, 2).astype(np.float32)
            break

    if quad is None:
        # Fallback: rectángulo mínimo del mayor contorno
        c = max(contours, key=cv2.contourArea)
        rect = cv2.minAreaRect(c)
        quad = cv2.boxPoints(rect).astype(np.float32)

    quad = _order_points(quad)

    # A coords globales
    quad[:, 0] += x0
    quad[:, 1] += y0

    return quad, edges, edges2


# ----------------------------
# 2) Quitar fondo: máscara del rectángulo (alpha)
# ----------------------------
def _cutout_rgba_from_quad(img_bgr, quad, scale=1.03):
    """
    Crea una máscara poligonal del rectángulo (quad) y devuelve RGBA con alpha (fondo transparente).
    """
    quad = quad.astype(np.float32)
    center = quad.mean(axis=0)
    quad_exp = (quad - center) * scale + center

    mask = np.zeros(img_bgr.shape[:2], dtype=np.uint8)
    cv2.fillConvexPoly(mask, np.round(quad_exp).astype(np.int32), 255)

    b, g, r = cv2.split(img_bgr)
    rgba = cv2.merge([b, g, r, mask])

    # Recorte tight
    ys, xs = np.where(mask > 0)
    ymin, ymax = ys.min(), ys.max()
    xmin, xmax = xs.min(), xs.max()
    rgba_crop = rgba[ymin:ymax+1, xmin:xmax+1]
    mask_crop = mask[ymin:ymax+1, xmin:xmax+1]

    return rgba_crop, mask_crop, quad_exp


# ----------------------------
# 3) Warp / enderezado a tamaño fijo 3×2 cm
# ----------------------------
def _warp_card(img_bgr, quad, paper_dim_mm=(30, 20), px_per_mm=20):
    """
    Warp a tamaño fijo: 30×20mm por defecto (3×2cm).
    """
    L_mm, W_mm = paper_dim_mm
    out_w = int(round(L_mm * px_per_mm))  # eje X = largo
    out_h = int(round(W_mm * px_per_mm))  # eje Y = ancho

    quad = _order_points(quad)
    dst = np.array([[0, 0], [out_w - 1, 0], [out_w - 1, out_h - 1], [0, out_h - 1]], dtype=np.float32)

    M = cv2.getPerspectiveTransform(quad, dst)
    warp = cv2.warpPerspective(img_bgr, M, (out_w, out_h), flags=cv2.INTER_LINEAR)
    return warp, (out_w, out_h)


# ----------------------------
# 4) Segmentación de gotas “color-aware” (robusta en campo) + Otsu
# ----------------------------
def _segment_droplets_coloraware(warp_bgr):
    """
    1) Estima el color de fondo amarillo (mediana en zonas amarillas).
    2) Calcula distancia cromática en LAB al fondo (A,B).
    3) Umbral Otsu en esa distancia + condición de oscuridad en L.
    """
    hsv = cv2.cvtColor(warp_bgr, cv2.COLOR_BGR2HSV)
    lower_yellow = np.array([12, 40, 60], dtype=np.uint8)
    upper_yellow = np.array([45, 255, 255], dtype=np.uint8)
    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # fallback si hay poca zona amarilla por reflejos
    if cv2.countNonZero(yellow_mask) < 0.20 * (warp_bgr.shape[0] * warp_bgr.shape[1]):
        yellow_mask[:] = 255

    lab = cv2.cvtColor(warp_bgr, cv2.COLOR_BGR2LAB).astype(np.int16)
    L = lab[:, :, 0]
    A = lab[:, :, 1]
    B = lab[:, :, 2]

    ys = yellow_mask > 0
    L0 = int(np.median(L[ys]))
    A0 = int(np.median(A[ys]))
    B0 = int(np.median(B[ys]))

    d2 = (A - A0) ** 2 + (B - B0) ** 2
    d2u8 = cv2.normalize(d2.astype(np.float32), None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    # Otsu sobre la distancia (baseline frecuente en segmentación WSP) [2](https://link.springer.com/article/10.1007/s11042-025-20697-2)
    _, thr = cv2.threshold(d2u8, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    dark = (L < (L0 - 8)).astype(np.uint8) * 255
    droplet_mask = cv2.bitwise_and(thr, dark)

    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    droplet_mask = cv2.morphologyEx(droplet_mask, cv2.MORPH_OPEN, k, iterations=1)

    return droplet_mask


# ----------------------------
# 5) Grid robusto para densidad (0.5×0.5 cm) y margen interior (2 mm)
# ----------------------------
def _grid_metrics(droplet_mask, contours, px_per_mm, tile_cm=0.5, margin_mm=2.0):
    H, W = droplet_mask.shape[:2]
    tile_mm = tile_cm * 10.0
    tile_px = int(round(tile_mm * px_per_mm))
    margin_px = int(round(margin_mm * px_per_mm))

    x0, y0 = margin_px, margin_px
    x1, y1 = W - margin_px, H - margin_px
    if x1 <= x0 + tile_px or y1 <= y0 + tile_px:
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

    density_grid = np.zeros((ny, nx), dtype=np.float32)
    cell_area_cm2 = tile_cm * tile_cm

    for c in contours:
        M = cv2.moments(c)
        if M["m00"] == 0:
            continue
        cx = M["m10"] / M["m00"]
        cy = M["m01"] / M["m00"]

        if not (x0 <= cx < x0 + nx * tile_px and y0 <= cy < y0 + ny * tile_px):
            continue

        i = int((cx - x0) // tile_px)
        j = int((cy - y0) // tile_px)
        density_grid[j, i] += 1.0

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


# ----------------------------
# FUNCIÓN PRINCIPAL
# ----------------------------
def analyze_card(
    image_path,
    paper_dim_mm=(30, 20),     # 3×2 cm
    px_per_mm=20,              # 600×400 px
    margin_mm=2.0,
    tile_cm=0.5,
    min_diam_um=50,            # filtro de ruido
    rect_scale=1.03,           # expandir rectángulo un poco (plástico/borde)
    save_debug=True
):
    """
    Pipeline completo:
    1) Detecta rectángulo por bordes
    2) Quita fondo (RGBA) + máscara
    3) Warp / enderezado a 3×2 cm
    4) Segmenta gotas solo en tarjeta
    5) Métricas (coverage, densidad global y robusta grid)
    6) Guarda debug: overlay rect, warp, masks, overlay drops, hist, heatmaps
    """

    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"No se pudo leer la imagen: {image_path}")

    quad, edges_roi, edges_roi_closed = _detect_card_quad_edges(img)
    if quad is None:
        return {"error": "No se pudo detectar el rectángulo por bordes (revisa encuadre/luz).",
                "coverage": None, "density_global": None, "density_robust": None}

    # Quitar fondo (RGBA + máscara)
    rgba_crop, mask_crop, quad_exp = _cutout_rgba_from_quad(img, quad, scale=rect_scale)

    # Warp/enderezado usando el rectángulo expandido
    warp, (Wpx, Hpx) = _warp_card(img, quad_exp, paper_dim_mm=paper_dim_mm, px_per_mm=px_per_mm)

    # Segmentar gotas SOLO en warp
    droplet_mask = _segment_droplets_coloraware(warp)

    # Máscara interior para excluir borde (evita gotas cortadas/sombras del borde)
    margin_px = int(round(margin_mm * px_per_mm))
    inner = np.zeros((Hpx, Wpx), dtype=np.uint8)
    inner[margin_px:Hpx-margin_px, margin_px:Wpx-margin_px] = 255
    droplet_mask_in = cv2.bitwise_and(droplet_mask, inner)

    # Contornos y filtro físico de tamaño mínimo
    contours, _ = cv2.findContours(droplet_mask_in, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

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

    # Métricas globales
    L_mm, W_mm = paper_dim_mm
    card_area_cm2 = (L_mm / 10.0) * (W_mm / 10.0)

    coverage = round(100.0 * (cv2.countNonZero(droplet_mask_in) / (Wpx * Hpx)), 2)
    droplet_count = len(kept)
    density_global = round(droplet_count / card_area_cm2, 2) if card_area_cm2 > 0 else 0.0

    # Métrica robusta por grid
    grid = _grid_metrics(droplet_mask_in, kept, px_per_mm=px_per_mm, tile_cm=tile_cm, margin_mm=margin_mm)
    density_robust = round(grid["summary"]["density_median"], 2) if grid is not None else None

    # Histograma de diámetros equivalentes (MANCHA) en µm
    areas_mm2 = np.array(areas_px, dtype=np.float64) * mm2_per_px
    diams_um = (2.0 * np.sqrt(areas_mm2 / np.pi) * 1000.0) if areas_mm2.size else np.array([])

    stats = {
        "mean_um": float(diams_um.mean()) if diams_um.size else None,
        "median_um": float(np.median(diams_um)) if diams_um.size else None,
        "p10_um": float(np.percentile(diams_um, 10)) if diams_um.size else None,
        "p90_um": float(np.percentile(diams_um, 90)) if diams_um.size else None,
        "min_um": float(diams_um.min()) if diams_um.size else None,
        "max_um": float(diams_um.max()) if diams_um.size else None,
    }

    # ----------------------------
    # Guardar debug
    # ----------------------------
    base = os.path.basename(image_path)
    name, _ = os.path.splitext(base)

    def _save(path, img_to_save):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        cv2.imwrite(path, img_to_save)

    urls = {}

    if save_debug:
        overlay_rect = img.copy()
        cv2.polylines(overlay_rect, [np.round(quad_exp).astype(np.int32)], True, (0, 0, 255), 3)

        overlay_drops = warp.copy()
        cv2.drawContours(overlay_drops, kept, -1, (0, 0, 255), 1)

        # Nombres
        fn_overlay_rect = f"overlay_rect_{name}.png"
        fn_rgba_cutout  = f"cutout_{name}.png"         # RGBA
        fn_mask_card    = f"mask_card_{name}.png"
        fn_warp         = f"warp_{name}.png"
        fn_mask_drops   = f"mask_drops_{name}.png"
        fn_mask_drops_in= f"mask_drops_in_{name}.png"
        fn_overlay_drops= f"overlay_drops_{name}.png"
        fn_hist         = f"hist_{name}.png"
        fn_heat_dens    = f"heat_density_{name}.png"
        fn_heat_cov     = f"heat_coverage_{name}.png"

        _save(os.path.join(settings.MEDIA_ROOT, fn_overlay_rect), overlay_rect)
        _save(os.path.join(settings.MEDIA_ROOT, fn_mask_card), mask_crop)
        _save(os.path.join(settings.MEDIA_ROOT, fn_warp), warp)
        _save(os.path.join(settings.MEDIA_ROOT, fn_mask_drops), droplet_mask)
        _save(os.path.join(settings.MEDIA_ROOT, fn_mask_drops_in), droplet_mask_in)
        _save(os.path.join(settings.MEDIA_ROOT, fn_overlay_drops), overlay_drops)

        # RGBA cutout (con alpha): cv2.imwrite sí lo guarda como PNG con 4 canales
        _save(os.path.join(settings.MEDIA_ROOT, fn_rgba_cutout), rgba_crop)

        # Histograma
        plt.figure()
        if diams_um.size:
            plt.hist(diams_um, bins=25)
            plt.title("Diámetro equivalente de mancha (µm)")
            plt.xlabel("µm")
            plt.ylabel("Frecuencia")
        else:
            plt.text(0.5, 0.5, "Sin gotas detectadas", ha="center", va="center")
            plt.axis("off")
        plt.tight_layout()
        plt.savefig(os.path.join(settings.MEDIA_ROOT, fn_hist), dpi=150)
        plt.close()

        # Heatmaps
        if grid is not None:
            plt.figure()
            plt.imshow(grid["density_grid"], aspect="auto")
            plt.colorbar(label="gotas/cm²")
            plt.title(f"Mapa densidad (tile={tile_cm}cm, margen={margin_mm}mm)")
            plt.tight_layout()
            plt.savefig(os.path.join(settings.MEDIA_ROOT, fn_heat_dens), dpi=150)
            plt.close()

            plt.figure()
            plt.imshow(grid["coverage_grid"], aspect="auto")
            plt.colorbar(label="% cobertura")
            plt.title(f"Mapa cobertura (tile={tile_cm}cm, margen={margin_mm}mm)")
            plt.tight_layout()
            plt.savefig(os.path.join(settings.MEDIA_ROOT, fn_heat_cov), dpi=150)
            plt.close()

        # URLs
        urls = {
            "overlay_rect_url": settings.MEDIA_URL + fn_overlay_rect,
            "cutout_rgba_url": settings.MEDIA_URL + fn_rgba_cutout,
            "mask_card_url": settings.MEDIA_URL + fn_mask_card,
            "warp_url": settings.MEDIA_URL + fn_warp,
            "mask_drops_url": settings.MEDIA_URL + fn_mask_drops,
            "mask_drops_in_url": settings.MEDIA_URL + fn_mask_drops_in,
            "overlay_drops_url": settings.MEDIA_URL + fn_overlay_drops,
            "hist_url": settings.MEDIA_URL + fn_hist,
            "heat_density_url": settings.MEDIA_URL + fn_heat_dens if grid is not None else None,
            "heat_coverage_url": settings.MEDIA_URL + fn_heat_cov if grid is not None else None,
        }

    # Nota de fiabilidad por cobertura (limitación por solapes) [3](https://sprayers101.com/assessing_wsp_pt3/)[4](https://upcommons.upc.edu/bitstreams/d2e74f77-44a8-4885-9e55-eb3e9d804624/download)
    note = "OK"
    if coverage >= 20:
        note = "Cobertura alta: el conteo de gotas puede subestimar por solapes; prioriza coverage% y densidad robusta."

    return {
        "coverage": coverage,
        "droplet_count": droplet_count,
        "density_global": density_global,
        "density_robust": density_robust,
        "card_area_cm2": round(card_area_cm2, 2),
        "diameter_stats_um_stain": stats,
        "grid_summary": grid["summary"] if grid is not None else None,
        "note": note,
        **urls
    }

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



