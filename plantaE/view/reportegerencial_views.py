# Create your views here.

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from openpyxl import Workbook
from django.shortcuts import get_object_or_404, redirect
from plantaE.models import Actpeso,supervision,supervisionproduccion,pedidos,tipoCajas,controlcajas, proyecciones,paramenvlocales,enviosrec,AcumFrutaaux,salidacontenedores, inventarioProdTermAux,productores,contenedores,Boletas, detallerecaux,detallerec,salidasFruta, usuariosAppFruta, datosProduccion, detallesProduccion, detallesEstructuras, Recepciones, Ccalidad,causasRechazo,inventarioProdTerm,productoTerm,cultivoxFinca,AcumFruta
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

def boletas_constanciarecepcion(request):
    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        recepcion = request.POST.get('recepcion')
        proveedor = request.POST.get('proveedor')
        cultivo = request.POST.get('cultivo')
        libras = request.POST.get('libras')
        aprovechamiento = request.POST.get('aprovechamiento')
        mediano = request.POST.get('mediano')
        devolucion = request.POST.get('devolucion')

        try:
            vector1 = json.loads(request.POST.get('vector1', '[]'))
            vector2 = json.loads(request.POST.get('vector2', '[]'))
        except json.JSONDecodeError:
            vector1 = []
            vector2 = []
        fecha_obj = datetime.datetime.strptime(fecha, '%Y-%m-%d').date()
        semana = fecha_obj.isocalendar()[1]
        llave = str(semana) + " | " + str(proveedor) + " | " +str(cultivo)
        causasrechazo = Ccalidad.objects.filter(llave = llave)
        fechahoy = timezone.now().date()
        context = {
            'fecha': fecha,
            'recepcion': int(recepcion),
            'proveedor': proveedor,
            'orden': vector1[0],
            'cultivo': cultivo,
            'libras': libras,
            'aprovechamiento': aprovechamiento,
            'mediano': mediano,
            'devolucion': devolucion,
            'planta': "SDC - Nueva Santa Rosa",
            'vector1': vector1,
            'vector2': vector2,
            'fechahoy': fechahoy,
            'causas': causasrechazo
        }
        return render(request, 'plantaE/reportegerencial/boletasFruta_constanciarecepcion.html', context)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

def boletas_constanciatrazarecepcion(request):

    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        recepcion = request.POST.get('recepcion')
        proveedor = request.POST.get('proveedor')
        cultivo = request.POST.get('cultivo')
        libras = request.POST.get('libras')

        detallefruta = AcumFrutaaux.objects.filter(recepcion=recepcion)
        cajas = detallerec.objects.get(recepcion=recepcion).cajas
        fechahoy = timezone.now().date()

        context = {
            'fecha': fecha,
            'recepcion': recepcion,
            'productor':proveedor,
            'cultivo': cultivo,
            'libras': libras,
            'cajas': cajas,
            'planta': "SDC - Nueva Santa Rosa",
            'vector1': list(detallefruta.values()),
            'fechahoy': fechahoy
        }
        return render(request, 'plantaE/reportegerencial/boletasFruta_constanciatrazarecepcion.html', context)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

def boletas_constanciatrazarexpo(request):

    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        palet=request.POST.get('palet')
        contenedor = request.POST.get('contenedor')
        cultivo = request.POST.get('cultivo')
        proveedor = request.POST.get('proveedor')
        itemsapcode = request.POST.get('itemsapcode')
        itemsapname = request.POST.get('itemsapname')
        empaque_tipo = request.POST.get('empaque_tipo')
        empaque_cnt = request.POST.get('empaque_cnt')
        total_libras = request.POST.get('total_libras')
        total_cajas = request.POST.get('total_cajas')

        conten2=salidacontenedores.objects.filter(
            itemsapcode=itemsapcode,
            palet=int(palet),
            proveedor=proveedor,
            fechasalcontenedor=fecha,
            contenedor=contenedor).exclude(status="Anulado")
        salcontentids = conten2.values_list('registro',flat=True).distinct()
        ids = [str(x) for x in salcontentids]
        datosinvaux = inventarioProdTermAux.objects.filter(salidacontenedores__in=ids).exclude(status="Anulado")
        registrosinv= datosinvaux.values_list('inventarioreg',flat=True)
        datosinv = inventarioProdTerm.objects.filter(registro__in=registrosinv).exclude(status="Anulado")
        boletasid=datosinv.values_list('boleta',flat=True)
        detallefruta = AcumFrutaaux.objects.filter(boleta__in=boletasid).exclude(status="Anulado")
        fecha_obj = datetime.datetime.strptime(fecha, '%Y-%m-%d').date()
        fechahoy = timezone.now().date()
        conten=salidacontenedores.objects.exclude(status="Anulado")
        totalboletainv= inventarioProdTerm.objects.filter(boleta__in=boletasid).exclude(status="Anulado")
        
        invboletasid=totalboletainv.values_list('registro',flat=True)
        conten_dict = {
            str(obj.registro): {
                'palet': obj.palet,
                'contenedor': obj.contenedor
            }
            for obj in conten
        }
        #totalboletainvaux= inventarioProdTermAux.objects.filter(inventarioreg__in=invboletasid)
        totalboletainvaux = inventarioProdTermAux.objects.filter(
            inventarioreg__in=invboletasid
        ).values()

        # Agregar el palet de forma manual
        vector3 = []
        for item in totalboletainvaux:
            registro = str(item['salidacontenedores'])  # debe coincidir con las claves del dict
            data_conten = conten_dict.get(registro, {})
            
            item['palet'] = data_conten.get('palet', 'N/D')
            item['contenedor'] = data_conten.get('contenedor', 'N/D')
            
            vector3.append(item)

        context = {
            'fecha': fecha,
            'itemsapcode': itemsapcode,
            'productor':proveedor,
            'cultivo': cultivo,
            'itemsapname': itemsapname,
            'cajas': total_cajas,
            'libras': total_libras,
            'empaque_tipo': empaque_tipo,
            'empaque_cnt': empaque_cnt,
            'planta': "SDC - Nueva Santa Rosa",
            'vector1': list(detallefruta.values()),
            'vector2': list(totalboletainv.values()),
            'vector3': vector3,
            'fechahoy': fechahoy,
            'contenedor':conten2.first().contenedor,
            'mercado': datosinv.first().categoria,
            'palet': palet
        }

        return render(request, 'plantaE/reportegerencial/boletasFruta_constanciatrazaexpo.html', context)
    
def boletas_constanciatraza(request):

    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        envio=request.POST.get('envio')
        proveedor = request.POST.get('productor')
        registro = request.POST.get('registro')
        itemsapcode = request.POST.get('itemsapcode')
        itemsapname = request.POST.get('itemsapname')
        empaque_tipo = request.POST.get('empaque_tipo')
        empaque_cnt = request.POST.get('empaque_cnt')
        libras = request.POST.get('libras')
        datosinv=inventarioProdTerm.objects.filter(itemsapcode=itemsapcode,enviorec=int(envio))
        boletas = datosinv.values_list('boleta',flat=True)  
        detallefruta = AcumFrutaaux.objects.filter(boleta__in=boletas)

        fecha_obj = datetime.datetime.strptime(fecha, '%Y-%m-%d').date()
        fechahoy = timezone.now().date()
        context = {
            'fecha': fecha,
            'itemsapcode': itemsapcode,
            'productor':proveedor,
            'cultivo': datosinv.first().cultivo,
            'itemsapname': itemsapname,
            'libras': libras,
            'registro': registro,
            'empaque_tipo': empaque_tipo,
            'empaque_cnt': empaque_cnt,
            'planta': "SDC - Nueva Santa Rosa",
            'vector1': list(detallefruta.values()),
            'fechahoy': fechahoy,
            'envio':envio,
            'mercado': datosinv.first().categoria
        }
        return render(request, 'plantaE/reportegerencial/boletasFruta_constanciatraza.html', context)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

def boletas_reporterecepcion(request):
    if request.method == 'POST':
        try:
            opcion1 = request.POST.get('opcion1')  # cultivo
            opcion2 = request.POST.get('opcion2')  # proveedor
            opcion3 = request.POST.get('opcion3')  # fecha

            # === 1. Recepciones base ===
            recepciones_raw = (
                detallerec.objects
                .filter(status="En proceso", cultivo=opcion1,fechasalidafruta=opcion3)
                .values('recepcion', 'llave', 'finca', 'cultivo', 'fecha')
                .annotate(total_libras=Sum('libras'))
                .order_by('-recepcion')
            )

            recepciones_filtradas = []
            for r in recepciones_raw:
                proveedor = obtener_proveedor_desde_finca_llave(r['finca'], r['llave'])
                if proveedor == opcion2:
                    r['proveedor'] = proveedor
                    recepciones_filtradas.append(r)

            recepciones_filtradas = recepciones_filtradas[:10]

            recepciones_dict = {
                r['recepcion']: {
                    'total_libras': r['total_libras'],
                    'proveedor': r['proveedor'],
                    'cultivo': r['cultivo'],
                    'fecha': r['fecha'],
                }
                for r in recepciones_filtradas
            }

            # === 2. Detalles y boletas ===
            detalles = detallerecaux.objects.filter(recepcion__in=recepciones_dict.keys()).exclude(status='Anulado')
            boleta_ids = detalles.values_list('boleta', flat=True).distinct()
            boletas = Boletas.objects.filter(boleta__in=boleta_ids)
            boletas_dict = {b.boleta: b for b in boletas}

            # === 3. Inicializar estructuras ===
            resumen = defaultdict(lambda: {'aprovechamiento': 0, 'mediano': 0, 'devolución': 0, 'total': 0})
            resumen_temporal = defaultdict(lambda: defaultdict(float))  # recepcion -> calidad -> libras

            # === 4. Recorrer detalles ===
            for detalle in detalles:
                boleta = boletas_dict.get(detalle.boleta)
                if not boleta:
                    continue

                calidad = (boleta.calidad or '').strip().lower()
                libras = detalle.libras or 0
                recepcion = detalle.recepcion

                # Clasificación resumen
                if 'aprovechamiento' in calidad:
                    resumen[recepcion]['aprovechamiento'] += libras
                elif 'mediano' in calidad:
                    resumen[recepcion]['mediano'] += libras
                elif 'devolución' in calidad:
                    resumen[recepcion]['devolución'] += libras

                resumen[recepcion]['total'] += libras

                # === vector1: desglose por boleta ===
                # Calculamos porcentaje por recepción
                total_actual = resumen[recepcion]['total']
                porcentaje = round((libras * 100 / total_actual), 2) if total_actual else 0


                # === Acumular en resumen_temporal para vector2 ===
                resumen_temporal[recepcion][calidad] += libras
            vector1 = []
            for detalle in detalles:
                boleta = boletas_dict.get(detalle.boleta)
                if not boleta:
                    continue

                calidad = (boleta.calidad or '').strip().lower()
                calidad1 = (boleta.calidad1 or '').strip().lower()
                ordenfinca = (boleta.ordenfinca or '').strip().lower()
                categoria = (boleta.categoria or '').strip().lower()
                cajas = boleta.cajas or 0
                libras = detalle.libras or 0
                recepcion = detalle.recepcion

                total_actual = resumen[recepcion]['total']
                porcentaje = round((libras * 100 / total_actual), 2) if total_actual else 0

                vector1.append({
                    'recepcion': recepcion,
                    'boleta': detalle.boleta,
                    'categoria': categoria,
                    'calidad': calidad,
                    'calidad1': calidad1,
                    'orden': ordenfinca,
                    'cajas': cajas,
                    'libras': libras,
                    'porcentaje': porcentaje
                })
            # === 5. Armar vector2 (resumen por calidad) ===
            vector2 = []

            for recepcion, calidades in resumen_temporal.items():
                total = sum(calidades.values())
                for calidad, libras in calidades.items():
                    porcentaje = round(libras * 100 / total, 2) if total else 0
                    vector2.append({
                        'recepcion': recepcion,
                        'calidad': calidad,
                        'libras': libras,
                        'porcentaje': porcentaje
                    })

            # === 6. Resultado principal (tabla de resumen) ===
            resultado = []
            for recepcion_id, datos in resumen.items():
                meta = recepciones_dict.get(recepcion_id)
                if not meta:
                    continue

                total_recepcion = meta['total_libras'] or 0
                total_distribuido = datos['total'] or 0
                pendiente = max(total_recepcion - total_distribuido, 0)

                resultado.append({
                    'fecha': str(meta['fecha']),
                    'recepcion': recepcion_id,
                    'proveedor': meta['proveedor'],
                    'cultivo': meta['cultivo'],
                    'libras': round(total_recepcion, 2),
                    'aprovechamiento': round(datos['aprovechamiento'] * 100 / total_distribuido, 2) if total_distribuido else 0,
                    'mediano': round(datos['mediano'] * 100 / total_distribuido, 2) if total_distribuido else 0,
                    'devolucion': round(datos['devolución'] * 100 / total_recepcion, 2) if total_recepcion else 0,
                    'porcentaje_pendiente': round(pendiente * 100 / total_recepcion, 2) if total_recepcion else 0,
                })

            orden_personalizado = {
                'exportación': 0,
                'carreta': 1,
                'cenma': 2,
                'devolución': 3
            }
            vector1.sort(key=lambda x: orden_personalizado.get(x['categoria'], 99))
            # === 7. Enviar respuesta JSON ===
            return JsonResponse({
                'recdic': list(recepciones_dict),
                'datos': resultado,
                'vector1': vector1,
                'vector2': vector2,
                
            }, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    # GET
    return render(request, 'plantaE/reportegerencial/boletasFruta_reporterecepciones.html')

def boletas_trazarecepcion(request):
    if request.method == 'POST':
        try:
            opcion1 = request.POST.get('opcion1')  # cultivo
            opcion2 = request.POST.get('opcion2')  # proveedor
            opcion3 = request.POST.get('opcion3')  # fecha

            # === 1. Recepciones base ===
            recepciones_raw = (
                detallerec.objects
                .filter(status="En proceso", cultivo=opcion1,fechasalidafruta=opcion3)
                .values('recepcion', 'llave', 'finca', 'cultivo', 'fecha')
                .annotate(total_libras=Sum('libras'))
                .order_by('-recepcion')
            )

            recepciones_filtradas = []
            for r in recepciones_raw:
                proveedor = obtener_proveedor_desde_finca_llave(r['finca'], r['llave'])
                if proveedor == opcion2:
                    r['proveedor'] = proveedor
                    recepciones_filtradas.append(r)

            recepciones_filtradas = recepciones_filtradas[:10]

            recepciones_dict = {
                r['recepcion']: {
                    'total_libras': r['total_libras'],
                    'proveedor': r['proveedor'],
                    'cultivo': r['cultivo'],
                    'fecha': r['fecha'],
                }
                for r in recepciones_filtradas
            }

            # === 2. Detalles y boletas ===
            detalles = detallerecaux.objects.filter(recepcion__in=recepciones_dict.keys()).exclude(status='Anulado')
            boleta_ids = detalles.values_list('boleta', flat=True).distinct()
            boletas = Boletas.objects.filter(boleta__in=boleta_ids)
            boletas_dict = {b.boleta: b for b in boletas}

            # === 3. Inicializar estructuras ===
            resumen = defaultdict(lambda: {'aprovechamiento': 0, 'mediano': 0, 'devolución': 0, 'total': 0})
            resumen_temporal = defaultdict(lambda: defaultdict(float))  # recepcion -> calidad -> libras

            # === 4. Recorrer detalles ===
            for detalle in detalles:
                boleta = boletas_dict.get(detalle.boleta)
                if not boleta:
                    continue

                calidad = (boleta.calidad or '').strip().lower()
                libras = detalle.libras or 0
                recepcion = detalle.recepcion

                # Clasificación resumen
                if 'aprovechamiento' in calidad:
                    resumen[recepcion]['aprovechamiento'] += libras
                elif 'mediano' in calidad:
                    resumen[recepcion]['mediano'] += libras
                elif 'devolución' in calidad:
                    resumen[recepcion]['devolución'] += libras

                resumen[recepcion]['total'] += libras

                # === vector1: desglose por boleta ===
                # Calculamos porcentaje por recepción
                total_actual = resumen[recepcion]['total']
                porcentaje = round((libras * 100 / total_actual), 2) if total_actual else 0


                # === Acumular en resumen_temporal para vector2 ===
                resumen_temporal[recepcion][calidad] += libras
            vector1 = []
            for detalle in detalles:
                boleta = boletas_dict.get(detalle.boleta)
                if not boleta:
                    continue

                calidad = (boleta.calidad or '').strip().lower()
                calidad1 = (boleta.calidad1 or '').strip().lower()
                ordenfinca = (boleta.ordenfinca or '').strip().lower()
                categoria = (boleta.categoria or '').strip().lower()
                cajas = boleta.cajas or 0
                libras = detalle.libras or 0
                recepcion = detalle.recepcion

                total_actual = resumen[recepcion]['total']
                porcentaje = round((libras * 100 / total_actual), 2) if total_actual else 0

                vector1.append({
                    'recepcion': recepcion,
                    'boleta': detalle.boleta,
                    'categoria': categoria,
                    'calidad': calidad,
                    'calidad1': calidad1,
                    'orden': ordenfinca,
                    'cajas': cajas,
                    'libras': libras,
                    'porcentaje': porcentaje
                })
            # === 5. Armar vector2 (resumen por calidad) ===
            vector2 = []

            for recepcion, calidades in resumen_temporal.items():
                total = sum(calidades.values())
                for calidad, libras in calidades.items():
                    porcentaje = round(libras * 100 / total, 2) if total else 0
                    vector2.append({
                        'recepcion': recepcion,
                        'calidad': calidad,
                        'libras': libras,
                        'porcentaje': porcentaje
                    })

            # === 6. Resultado principal (tabla de resumen) ===
            resultado = []
            for recepcion_id, datos in resumen.items():
                meta = recepciones_dict.get(recepcion_id)
                if not meta:
                    continue

                total_recepcion = meta['total_libras'] or 0
                total_distribuido = datos['total'] or 0
                pendiente = max(total_recepcion - total_distribuido, 0)

                resultado.append({
                    'fecha': str(meta['fecha']),
                    'recepcion': recepcion_id,
                    'proveedor': meta['proveedor'],
                    'cultivo': meta['cultivo'],
                    'libras': round(total_recepcion, 2),
                    'aprovechamiento': round(datos['aprovechamiento'] * 100 / total_distribuido, 2) if total_distribuido else 0,
                    'mediano': round(datos['mediano'] * 100 / total_distribuido, 2) if total_distribuido else 0,
                    'devolucion': round(datos['devolución'] * 100 / total_recepcion, 2) if total_recepcion else 0,
                    'porcentaje_pendiente': round(pendiente * 100 / total_recepcion, 2) if total_recepcion else 0,
                })

            orden_personalizado = {
                'exportación': 0,
                'carreta': 1,
                'cenma': 2,
                'devolución': 3
            }
            vector1.sort(key=lambda x: orden_personalizado.get(x['categoria'], 99))
            # === 7. Enviar respuesta JSON ===
            return JsonResponse({
                'recdic': list(recepciones_dict),
                'datos': resultado,
                'vector1': vector1,
                'vector2': vector2,
                
            }, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    # GET
    return render(request, 'plantaE/reportegerencial/boletasFruta_trazarecepcion.html')

def boletas_reportetrazaexpo(request):
    if request.method == 'POST':
        try:
            opcion1 = request.POST.get('opcion1')  # contenedor
            opcion2 = request.POST.get('opcion2')  # fecha
            opcion3 = request.POST.get('opcion3')  # cultivo

            # Convertir fecha
            fecha_obj = datetime.datetime.strptime(opcion2, '%Y-%m-%d').date()

            # Base queryset
            qs = salidacontenedores.objects.filter(
                contenedor=opcion1,
                fechasalcontenedor=fecha_obj
            )

            # Si se seleccionó cultivo, filtrar
            if opcion3:
                qs = qs.filter(cultivo=opcion3)

            # Query final
            conten = qs.values(
                'palet',
                'itemsapcode',
                'proveedor',
                'cultivo'
            ).annotate(
                total_cajas=Sum('cajas'),
                total_libras=Sum('lbsintara'),
                fecha=Min('fechasalcontenedor'),
                itemsapname=Min('itemsapname')
            ).order_by('palet')

            return JsonResponse({'datos': list(conten)})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    # GET
    return render(request, 'plantaE/reportegerencial/boletasFruta_reportetrazaexpo.html')

def boletas_reportetraza(request):
    if request.method == 'POST':
        try:
            opcion1 = request.POST.get('opcion1')  # envio}

            envios = enviosrec.objects.filter(envio=opcion1).values()
            # === 7. Enviar respuesta JSON ===
            return JsonResponse({
                'datos': list(envios)
            }, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    # GET
    return render(request, 'plantaE/reportegerencial/boletasFruta_reportetraza.html')

def dashboard_acumfrutakgxm2(request):

    filtros_get = {
        'finca': request.GET.get('finca'),
        'orden': request.GET.get('orden'),
        'cultivo': request.GET.get('cultivo'),
        'estructura': request.GET.get('estructura'),
    }

    ordenes_abiertas = datosProduccion.objects.filter(status='Abierta').values_list('orden', flat=True)

    qs = AcumFruta.objects.filter(orden__in=ordenes_abiertas).exclude(finca="CIP").exclude(libras__isnull=True)

    for campo, valor in filtros_get.items():
        if valor:
            qs = qs.filter(**{campo: valor})

    datos_agrupados = qs.annotate(
        semana=ExtractWeek('fecha'),
        anio=ExtractIsoYear('fecha')
    ).values('anio', 'semana').annotate(
        libras_totales=Sum('libras')
    ).order_by('anio', 'semana')

    ordenes_por_semana = defaultdict(set)
    for record in qs.annotate(semana=ExtractWeek('fecha'), anio=ExtractIsoYear('fecha')).values('anio', 'semana', 'orden'):
        ordenes_por_semana[(record['anio'], record['semana'])].add(record['orden'])

    fechas = []
    kgxm2 = []
    derivadas = []

    for i, d in enumerate(datos_agrupados):
        anio = d['anio']
        semana = d['semana']
        fecha = get_date_from_week(anio, semana)

        kg_totales = d['libras_totales'] / 2.20462

        ordenes_semana = list(ordenes_por_semana[(anio, semana)])

        estructura_filter = {}
        for campo in ['orden', 'finca', 'cultivo', 'estructura']:
            if filtros_get.get(campo):
                estructura_filter[campo] = filtros_get[campo]

        estructura_filter['orden__in'] = ordenes_semana

        area_total = detallesEstructuras.objects.filter(**estructura_filter).aggregate(
            total_area=Sum('area')
        )['total_area'] or 0

        kg_m2 = round(kg_totales / area_total, 2) if area_total > 0 else 0

        fechas.append(fecha.isoformat())
        kgxm2.append(kg_m2)
        derivadas.append(0 if i == 0 else kgxm2[i] - kgxm2[i - 1])

    # PROYECCIONES – solo por finca, orden y cultivo
    proy_qs = proyecciones.objects.all()

    for campo in ['finca', 'orden', 'cultivo']:
        if filtros_get.get(campo):
            proy_qs = proy_qs.filter(**{campo: filtros_get[campo]})

    proy_qs = proy_qs.exclude(kgm2__isnull=True)

    # Dict para acceso rápido
    proy_data = proy_qs.values('año', 'semana', 'kgm2').order_by('año', 'semana')
    proy_dict = {(p['año'], p['semana']): p['kgm2'] for p in proy_data}

    # Solo mostrar proyecciones para las semanas que existen en datos reales
    fechas_proy = []
    proy_kgxm2 = []

    for d in datos_agrupados:
        key = (d['anio'], d['semana'])
        fecha = get_date_from_week(*key)
        fechas_proy.append(fecha.isoformat())
        proy_kgxm2.append(round(proy_dict.get(key, 0), 2))
    # Acumulado real hasta ahora (filtrado y calculado previamente)
    acumulado_real = round(sum(kgxm2), 2)

    # Proyección total de la temporada (NO limitada a fechas reales)
    proyeccion_total_temp = proyecciones.objects.all()

    for campo in ['finca', 'orden', 'cultivo']:
        if filtros_get.get(campo):
            proyeccion_total_temp = proyeccion_total_temp.filter(**{campo: filtros_get[campo]})

    proyeccion_total_temp = proyeccion_total_temp.exclude(kgm2__isnull=True)

    total_proyectado = round(proyeccion_total_temp.aggregate(total=Sum('kgm2'))['total'] or 0, 2)
    filtros_completos = [
        ('Finca', 'finca', AcumFruta.objects.filter(orden__in=ordenes_abiertas).exclude(finca__isnull=True).exclude(finca='').values_list('finca', flat=True).distinct()),
        ('Orden', 'orden', AcumFruta.objects.filter(orden__in=ordenes_abiertas).exclude(orden__isnull=True).exclude(orden='').values_list('orden', flat=True).distinct()),
        ('Variedad', 'variedad', AcumFruta.objects.filter(orden__in=ordenes_abiertas).exclude(variedad__isnull=True).exclude(variedad='').values_list('variedad', flat=True).distinct()),
        ('Cultivo', 'cultivo', AcumFruta.objects.filter(orden__in=ordenes_abiertas).exclude(cultivo__isnull=True).exclude(cultivo='').values_list('cultivo', flat=True).distinct()),
        ('Estructura', 'estructura', AcumFruta.objects.filter(orden__in=ordenes_abiertas).exclude(estructura__isnull=True).exclude(estructura='').values_list('estructura', flat=True).distinct()),
    ]

    context = {
        'filtros_completos': filtros_completos,
        'acumulado_real_json': json.dumps(acumulado_real),
        'total_proyectado_json': json.dumps(total_proyectado),
        'fechas_json': json.dumps(fechas),
        'kgxm2_json': json.dumps(kgxm2),
        'proy_kgxm2_json': json.dumps(proy_kgxm2),
        'fechas_proy_json': json.dumps(fechas_proy),
        'derivadas_json': json.dumps(derivadas),
        'request': request,
    }

    return render(request, 'plantaE/reportegerencial/dashboard_acumfrutakgxm2.html', context)

def dashboard_acumfruta(request):

    # Filtros desde GET
    filtros_get = {
        'finca': request.GET.get('finca'),
        'orden': request.GET.get('orden'),
        'variedad': request.GET.get('variedad'),
        'cultivo': request.GET.get('cultivo'),
        'estructura': request.GET.get('estructura'),
    }

    ordenes_abiertas = datosProduccion.objects.filter(status='Abierta').values_list('orden', flat=True)

    # Query base
    qs = AcumFruta.objects.filter(orden__in=ordenes_abiertas).exclude(finca="CIP").exclude(libras__isnull=True)

    # Aplicar filtros
    for campo, valor in filtros_get.items():
        if valor:
            qs = qs.filter(**{campo: valor})

    # Agrupación por semana
    datos = qs.annotate(
        semana=ExtractWeek('fecha'),
        anio=ExtractIsoYear('fecha')
    ).values('anio', 'semana').annotate(
        libras_totales=Sum('libras')
    ).order_by('anio', 'semana')

    # Ejes para la gráfica
    fechas = [get_date_from_week(d['anio'], d['semana']).isoformat() for d in datos]
    kilos = [round(d['libras_totales'] / 2.20462, 2) for d in datos]
    derivadas = [0] + [kilos[i] - kilos[i - 1] for i in range(1, len(kilos))]


    # Filtros disponibles
    filtros_completos = [
        ('Finca', 'finca', AcumFruta.objects.filter(orden__in=ordenes_abiertas).exclude(finca__isnull=True).exclude(finca='').values_list('finca', flat=True).distinct()),
        ('Orden', 'orden', AcumFruta.objects.filter(orden__in=ordenes_abiertas).exclude(orden__isnull=True).exclude(orden='').values_list('orden', flat=True).distinct()),
        ('Variedad', 'variedad', AcumFruta.objects.filter(orden__in=ordenes_abiertas).exclude(variedad__isnull=True).exclude(variedad='').values_list('variedad', flat=True).distinct()),
        ('Cultivo', 'cultivo', AcumFruta.objects.filter(orden__in=ordenes_abiertas).exclude(cultivo__isnull=True).exclude(cultivo='').values_list('cultivo', flat=True).distinct()),
        ('Estructura', 'estructura', AcumFruta.objects.filter(orden__in=ordenes_abiertas).exclude(estructura__isnull=True).exclude(estructura='').values_list('estructura', flat=True).distinct()),
    ]

    context = {
        'filtros_completos': filtros_completos,
        'fechas_json': json.dumps(fechas),
        'libras_json': json.dumps(kilos),
        'derivadas_json': json.dumps(derivadas),
        'request': request,
    }
    return render(request, 'plantaE/reportegerencial/dashboard_acumfruta.html', context)

def contenedores_grafico_view(request):
    # Filtros desde GET
    tipo = request.GET.get('tipo', 'dia')
    fecha_inicio = request.GET.get('inicio')
    fecha_fin = request.GET.get('fin')

    hoy = timezone.now().date()
    fecha_inicio = datetime.datetime.strptime(fecha_inicio, '%Y-%m-%d').date() if fecha_inicio else hoy.replace(day=1)
    fecha_fin = datetime.datetime.strptime(fecha_fin, '%Y-%m-%d').date() if fecha_fin else hoy

    # Filtrar registros base
    registros = salidacontenedores.objects.filter(
        fechasalcontenedor__range=(fecha_inicio, fecha_fin)
    ).exclude(fechasalcontenedor__isnull=True).exclude(status="Anulado")

    # Agrupación para gráfico
    if tipo == 'dia':
        agrupado = (
            registros.annotate(fecha_trunc=TruncDate('fechasalcontenedor'))
            .values('fecha_trunc')
            .annotate(total=Count('contenedor', distinct=True))
            .order_by('fecha_trunc')
        )
        labels = [str(item['fecha_trunc']) for item in agrupado]
        data = [item['total'] for item in agrupado]
    else:  # semana
        agrupado = (
            registros.annotate(
                semana=ExtractWeek('fechasalcontenedor'),
                anio=ExtractIsoYear('fechasalcontenedor')
            )
            .values('anio', 'semana')
            .annotate(total=Count('contenedor', distinct=True))
            .order_by('anio', 'semana')
        )
        labels = [f'{item["anio"]}-W{item["semana"]:02d}' for item in agrupado]
        data = [item['total'] for item in agrupado]

    # Obtener lista de contenedores únicos (por contenedor y fecha)
    claves_unicas = registros.values_list('contenedor', 'fechasalcontenedor').distinct()

    contenedores_list = []
    for contenedor_id, fecha in claves_unicas:
        subquery = registros.filter(contenedor=contenedor_id, fechasalcontenedor=fecha)

        total_cajas = subquery.aggregate(s=Sum('cajas'))['s'] or 0
        cajas_sdc = subquery.filter(proveedor="SDC").aggregate(s=Sum('cajas'))['s'] or 0
        cajas_no_sdc = total_cajas - cajas_sdc
        pct_sdc = round(cajas_sdc * 100 / total_cajas, 2) if total_cajas else 0
        pct_no_sdc = 100 - pct_sdc if total_cajas else 0


        contenedores_list.append({
            'fecha': fecha,
            'contenedor': contenedor_id,
            'cajas_sdc': cajas_sdc,
            'cajas_no_sdc': cajas_no_sdc,
            'total_cajas': total_cajas,
            'pct_sdc': pct_sdc,
            'pct_no_sdc': pct_no_sdc,
        })
    # Obtener los registros de la tabla contenedores que coincidan con (contenedor, fecha)
    claves_join = [(c['contenedor'], c['fecha']) for c in contenedores_list]

    # Consultar contenedores con esas claves
    navieras_qs = contenedores.objects.filter(
        contenedor__in=[c[0] for c in claves_join],
        fecha__in=[c[1] for c in claves_join]
    ).exclude(status="Anulado")

    # Crear diccionario clave (contenedor, fecha) → naviera
    navieras_dict = {
        (c.contenedor, c.fecha): c.transportista for c in navieras_qs
    }

    # Asociar naviera en contenedores_list
    for item in contenedores_list:
        clave = (item['contenedor'], item['fecha'])
        item['naviera'] = navieras_dict.get(clave, 'No registrada')
    total_contenedores = len(contenedores_list)
    total_cajas = sum(item['total_cajas'] for item in contenedores_list)
    total_cajas_sdc = sum(item['cajas_sdc'] for item in contenedores_list)
    total_cajas_no_sdc = total_cajas - total_cajas_sdc

    pct_cajas_sdc = round((total_cajas_sdc * 100 / total_cajas), 2) if total_cajas else 0
    pct_cajas_no_sdc = 100 - pct_cajas_sdc if total_cajas else 0
    return render(request, 'plantaE/reportegerencial/grafico_contenedores.html', {
        'tipo': tipo,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'por_dia': json.dumps({'labels': labels, 'data': data}, default=str),
        'contenedores': contenedores_list,
        'total_contenedores': total_contenedores,
        'pct_cajas_sdc': pct_cajas_sdc,
        'pct_cajas_no_sdc': pct_cajas_no_sdc,
    })


def inventariogeneralger_list(request):
    today = timezone.now().date()

    salidas = inventarioProdTerm.objects.filter(
        fecha__lte=today,
        categoria="Exportación"
    ).filter(
        Q(status='') | Q(status__isnull=True)
    ).order_by('registro')

    salidas2 = inventarioProdTermAux.objects.filter(
        fecha__lte=today,
        categoria="Exportación"
    ).exclude(
        Q(status='En proceso') | Q(status='Anulado')
    )

    agrupaciones = {}

    for salida in salidas:
        # Reemplazo de nombre de ítem si aplica
        if (
            salida.pesostdxcaja == 11 and
            salida.cultivo == 'BLOCKY ORGANICO' and
            salida.itemsapcode != '305.100.268' and
            salida.categoria == 'Exportación'
        ):
            salida.itemsapname = 'CHILE ORGANICO DE COLORES (CAJA 11 LIBRAS)'

        elif (
            salida.pesostdxcaja == 11 and
            salida.cultivo == 'BLOCKY' and
            salida.itemsapcode != '305.100.268' and
            salida.categoria == 'Exportación'
        ):
            salida.itemsapname = 'CHILE DE COLORES (CAJA 11 LIBRAS)'

        clave = (salida.proveedor, salida.cultivo, salida.itemsapcode)

        if clave not in agrupaciones:
            agrupaciones[clave] = {
                'proveedor': salida.proveedor,
                'cultivo': salida.cultivo,
                'itemsapname': salida.itemsapname,
                'itemsapcode': salida.itemsapcode,
                'cajas_salidas': 0,
                'cajas_salidas2': 0
            }

        agrupaciones[clave]['cajas_salidas'] += salida.cajas or 0

    for salida2 in salidas2:
        clave = (salida2.proveedor, salida2.cultivo, salida2.itemsapcode)

        if clave in agrupaciones:
            agrupaciones[clave]['cajas_salidas2'] += salida2.cajas or 0

    registros_agrupados = []

    for agrupacion in agrupaciones.values():
        cajas_restantes = agrupacion['cajas_salidas'] - agrupacion['cajas_salidas2']
        if cajas_restantes > 0:
            agrupacion['cajas_restantes'] = cajas_restantes

            # Buscar productoTerm para obtener cajasxtarima
            try:
                producto = productoTerm.objects.get(itemsapcode=agrupacion['itemsapcode'])
                cajasxtarima = producto.cajasxtarima or 0
            except productoTerm.DoesNotExist:
                cajasxtarima = 0

            agrupacion['cajasxtarima'] = cajasxtarima

            if cajasxtarima > 0:
                agrupacion['tarimas_restantes'] = round(cajas_restantes / cajasxtarima, 2)
            else:
                agrupacion['tarimas_restantes'] = 0

            registros_agrupados.append(agrupacion)

    # Agrupar registros por itemsapname (segunda agrupación)
    agrupados_final = defaultdict(lambda: {
        'proveedor': '',
        'cultivo': '',
        'itemsapname': '',
        'cajas_restantes': 0,
        'cajasxtarima': 0,
        'tarimas_restantes': 0,
    })

    for registro in registros_agrupados:
        key = (registro['proveedor'], registro['cultivo'], registro['itemsapname'])
        grupo = agrupados_final[key]

        grupo['proveedor'] = registro['proveedor']
        grupo['cultivo'] = registro['cultivo']
        grupo['itemsapname'] = registro['itemsapname']
        grupo['cajas_restantes'] += registro['cajas_restantes']

        # Considera el promedio de cajasxtarima si hay diferencias
        if registro['cajasxtarima'] > 0:
            if grupo['cajasxtarima'] == 0:
                grupo['cajasxtarima'] = registro['cajasxtarima']
            else:
                grupo['cajasxtarima'] = (grupo['cajasxtarima'] + registro['cajasxtarima']) / 2

    # Calcular tarimas restantes nuevamente
    for grupo in agrupados_final.values():
        if grupo['cajasxtarima'] > 0:
            grupo['tarimas_restantes'] = round(grupo['cajas_restantes'] / grupo['cajasxtarima'], 2)

    # Convertir a lista y ordenar
    registros_agrupados_final = sorted(agrupados_final.values(), key=lambda x: x['proveedor'])

    registros_json = json.dumps(registros_agrupados_final, default=str)
    query = json.dumps(list(salidas2.values()), default=str)
    
    return render(
        request,
        'plantaE/reportegerencial/inventarioProd_inventariogeneralger.html',
        {
            'registros': registros_agrupados_final,
            'registros_json': registros_json,
            'query': query
        }
    )

def semanalprodterm_pivot(request):
    hoy = timezone.now().date()
    fecha_max = AcumFruta.objects.aggregate(max_fecha=Max('fecha'))['max_fecha'] or hoy

    ordenes_abiertas = datosProduccion.objects.filter(status='Abierta').values_list('orden', flat=True)

    inventario_datos = Boletas.objects.filter(ordenfinca__in=ordenes_abiertas).annotate(
        semana=ExtractWeek('fecha'),
        anio=ExtractIsoYear('fecha')
    ).values('itemsapname', 'categoria', 'cultivo', 'semana', 'anio').annotate(
        total_libras=Sum('libras')
    ).exclude(categoria="Devolución").order_by('anio', 'semana', 'itemsapname', 'categoria')

    resultado = []
    total_por_semana_cultivo = defaultdict(float)

    for registro in inventario_datos:
        clave = (registro['anio'], registro['semana'], registro['cultivo'])
        total_libras = registro['total_libras'] or 0
        total_por_semana_cultivo[clave] += total_libras
        kilos = total_libras / 2.20462 if total_libras else 0

    for registro in inventario_datos:
        clave = (registro['anio'], registro['semana'], registro['cultivo'])
        total_cultivo_semana = total_por_semana_cultivo[clave]
        total_libras = registro['total_libras'] or 0
        porcentaje = (total_libras / total_cultivo_semana) * 100 if total_cultivo_semana else 0
        kilos = total_libras / 2.20462 if total_libras else 0

        resultado.append({
            'itemsapname': registro['itemsapname'],
            'categoria': registro['categoria'],
            'cultivo': registro['cultivo'],
            'semana': registro['semana'],
            'anio': registro['anio'],
            'libras': round(total_libras, 2),
            'porcentaje': round(porcentaje, 2),
            'kilos': round(kilos, 2),
        })

    registros_json = json.dumps(resultado, default=str)

    if not resultado:
        tabla_html = "<p class='text-danger'>No hay datos disponibles para mostrar.</p>"
    else:
        df = pd.DataFrame(resultado)

        metrica = request.GET.get('metrica', 'porcentaje')
        if metrica not in ['porcentaje', 'libras', 'kilos']:
            metrica = 'porcentaje'

        if metrica not in ['porcentaje', 'libras', 'kilos'] or metrica not in df.columns:
            tabla_html = f"<p class='text-warning'>Métrica '{metrica}' inválida o no disponible.</p>"
        else:
            tabla_pivote = df.pivot_table(
                index=['cultivo', 'categoria', 'itemsapname'],
                columns=['semana', 'anio'],
                values=metrica,
                aggfunc='sum'
            )
           
            tabla_pivote = tabla_pivote.fillna("")

            # Aplanar índices (convertir multiindex filas a columnas normales)
            tabla_pivote_reset = tabla_pivote.reset_index()

            # Aplanar multiindex de columnas, por ejemplo: (semana, anio) -> "semana_anio"
            tabla_pivote_reset.columns = [
                '_'.join(map(str, col)).strip() if isinstance(col, tuple) else col
                for col in tabla_pivote_reset.columns.values
            ]

            # Ahora sí, convertir a HTML
            tabla_html = tabla_pivote_reset.to_html(
                classes="table table-striped",
                index=False,
                na_rep="",
                table_id="tabla-pivote"
            )

    return render(request, 'plantaE/reportegerencial/inventarioProd_reportesemanalprodterm_pivot.html', {
        'tabla_html': tabla_html,
        'registros_json': registros_json,
    })

def reporte_mermas_view(request):
    # Parámetros desde GET
    tipo = request.GET.get('tipo', 'acumulado')  # "dia", "semana", "mes", "acumulado"
    fecha_inicio = request.GET.get('inicio')
    fecha_fin = request.GET.get('fin')

    hoy = timezone.now().date()
    fecha_inicio = datetime.datetime.strptime(fecha_inicio, '%Y-%m-%d').date() if fecha_inicio else hoy.replace(day=1)
    fecha_fin = datetime.datetime.strptime(fecha_fin, '%Y-%m-%d').date() if fecha_fin else hoy

    # Filtrar datos base
    registros = inventarioProdTerm.objects.filter(
        fecha__range=(fecha_inicio, fecha_fin),
        categoria="Exportación"
    ).exclude(status__in=[ 'Anulado'])

    agrupaciones = defaultdict(lambda: {
        'cajas': 0,
        'peso_real': 0,
        'peso_teorico': 0,
    })

    for r in registros:
        # Agrupación dinámica
        if tipo == 'dia':
            clave_fecha = r.fecha.strftime('%Y-%m-%d')
        elif tipo == 'semana':
            iso_year, iso_week, _ = r.fecha.isocalendar()
            clave_fecha = f"{iso_year}-W{iso_week:02d}"
        elif tipo == 'mes':
            clave_fecha = r.fecha.strftime('%Y-%m')
        else:  # acumulado
            clave_fecha = 'ACUMULADO'
        # Corrección de itemSAPName según condiciones específicas
        if (
            r.pesostdxcaja == 11 and
            r.cultivo == "BLOCKY ORGANICO" and
            r.itemsapcode != "305.100.268" and
            r.categoria == "Exportación"
        ):
            itemsapname = "CHILE ORGANICO DE COLORES (CAJA 11 LIBRAS)"
        elif (
            r.pesostdxcaja == 11 and
            r.cultivo == "BLOCKY" and
            r.itemsapcode != "305.100.268" and
            r.categoria == "Exportación"
        ):
            itemsapname = "CHILE DE COLORES (CAJA 11 LIBRAS)"
        else:
            itemsapname = r.itemsapname  # Usa el nombre original si no cumple condición

        clave = (clave_fecha, itemsapname)

        pesostd = r.pesostdxcaja or 0
        cajas = r.cajas or 0
        libras = r.lbsintara or 0
        peso_teorico = cajas * pesostd

        agrupaciones[clave]['cajas'] += cajas
        agrupaciones[clave]['peso_real'] += libras
        agrupaciones[clave]['peso_teorico'] += peso_teorico

    # Preparar datos para la tabla
    reporte = []
    for (fecha_grupo, item), valores in agrupaciones.items():

        exceso = valores['peso_real'] - valores['peso_teorico']
        
        exceso_pct = (exceso / valores['peso_teorico']) * 100 if valores['peso_teorico'] > 0 else 0

        reporte.append({
            'fecha_grupo': fecha_grupo,
            'itemsapname': item,
            'cajas': valores['cajas'],
            'peso_real': round(valores['peso_real'], 2),
            'peso_teorico': round(valores['peso_teorico'], 2),
            'exceso': round(exceso, 2),
            'exceso_pct': round(exceso_pct, 2)
        })

    reporte = sorted(reporte, key=lambda x: (x['fecha_grupo'], x['itemsapname']))
    return render(request, 'plantaE/reportegerencial/reporte_mermas.html', {
        'reporte': reporte,
        'reporte_json': json.dumps(reporte, default=str),
        'tipo': tipo,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin
    })

def reporte_tabla_pivote(request):
    filtros_get = {
        'finca': request.GET.get('finca'),
        'orden': request.GET.get('orden'),
        'estructura': request.GET.get('estructura'),
        'variedad': request.GET.get('variedad'),
        'cultivo': request.GET.get('cultivo'),
    }
    ordenes_abiertas = datosProduccion.objects.filter(status='Abierta').values_list('orden', flat=True)
    
    qs = AcumFruta.objects.filter(orden__in=ordenes_abiertas).exclude(finca="CIP").exclude(libras__isnull=True).exclude(status="Anulado")

    for campo, valor in filtros_get.items():
        if valor:
            qs = qs.filter(**{campo: valor})

    data = qs.values('fecha', 'finca', 'orden','cultivo', 'estructura').annotate(
        total_libras=Sum('libras')
    )

    if data:
        df = pd.DataFrame(data)
        df['fecha'] = pd.to_datetime(df['fecha'])
        iso = df['fecha'].dt.isocalendar()
        df['semana'] = iso['year'].astype(str) + '-W' + iso['week'].astype(str).str.zfill(2)
        df['kg'] = df['total_libras'] / 2.20462  # convertir a kilogramos

        # Crear tabla pivote: kilos por semana
        pivot = pd.pivot_table(
            df,
            values='kg',
            index=['finca', 'orden','cultivo', 'estructura'],
            columns='semana',
            aggfunc='sum',
            fill_value=0
        ).round(2)

        # Obtener áreas por finca-orden-estructura
        areas_qs = detallesEstructuras.objects.values('finca', 'orden', 'cultivo', 'estructura').annotate(
            area_total=Sum('area')
        )
        df_areas = pd.DataFrame(list(areas_qs))

        # Unir pivot con áreas
        pivot = pivot.reset_index()
        df_merge = pd.merge(pivot, df_areas, on=['finca', 'orden', 'cultivo','estructura'], how='left')

        # Calcular rendimiento (kg/m²) por semana
        semanas = [col for col in df_merge.columns if col.startswith('20')]
        for semana in semanas:
            df_merge[semana] = df_merge[semana] / df_merge['area_total']
         
        df_merge[semanas] = df_merge[semanas].round(2)

        # Agregar columna total kilos por fila (sumar las semanas en kg)
        # Para total kilos, sumamos las semanas en el pivot original
        df_merge['total_kilos'] = pivot[semanas].sum(axis=1).round(2)

        # Agregar columna total kg/m² (sumar las semanas ya divididas por área)
        df_merge['total_kg_m2'] = df_merge[semanas].sum(axis=1).round(2)
        # Convertir resultado final a tabla HTML
        tabla_html = df_merge.to_html(
            classes='table table-striped table-bordered table-sm table-hover',
            index=False,
            table_id='tabla-pivote'
        )
    else:
        tabla_html = "<p>No hay datos para los filtros aplicados.</p>"

    # Filtros disponibles
    filtros_completos = [
        ('Finca', 'finca', AcumFruta.objects.filter(orden__in=ordenes_abiertas).exclude(finca__isnull=True).exclude(finca='').values_list('finca', flat=True).distinct()),
        ('Orden', 'orden', AcumFruta.objects.filter(orden__in=ordenes_abiertas).exclude(orden__isnull=True).exclude(orden='').values_list('orden', flat=True).distinct()),
        ('Variedad', 'variedad', AcumFruta.objects.filter(orden__in=ordenes_abiertas).exclude(variedad__isnull=True).exclude(variedad='').values_list('variedad', flat=True).distinct()),
        ('Cultivo', 'cultivo', AcumFruta.objects.filter(orden__in=ordenes_abiertas).exclude(cultivo__isnull=True).exclude(cultivo='').values_list('cultivo', flat=True).distinct()),
        ('Estructura', 'estructura', AcumFruta.objects.filter(orden__in=ordenes_abiertas).exclude(estructura__isnull=True).exclude(estructura='').values_list('estructura', flat=True).distinct()),
    ]

    return render(request, 'plantaE/reportegerencial/reporte_tabla_pivote.html', {
        'tabla_html': tabla_html,
        'filtros_completos': filtros_completos,
        'request': request
    })

def poraprovechamientosemp(request):
    hoy = timezone.now().date()
    nombre_usuario = request.user.username
    datos = usuariosAppFruta.objects.filter(correo=nombre_usuario).values('finca', 'encargado')

    fecha_max = AcumFruta.objects.aggregate(max_fecha=Max('fecha'))['max_fecha']
    if not fecha_max:
        fecha_max = hoy

    ordenes_abiertas = datosProduccion.objects.filter(status='Abierta').values_list('orden', flat=True)

    # Total de libras por variedad desde AcumFruta
    acumfrutadatos = AcumFruta.objects.filter(orden__in=ordenes_abiertas,correo=nombre_usuario).annotate(
        semana=ExtractWeek('fecha'),
        anio=ExtractIsoYear('fecha')
    ).values('finca', 'cultivo', 'orden', 'estructura', 'variedad'
    ).annotate(total_libras=Sum('libras')).exclude(status="Anulado").order_by()

    recepciones_dict = {
        formar_clave2(r['finca'], r['cultivo'], r['orden'], r['estructura'], r['variedad']): r['total_libras']
        for r in acumfrutadatos
    }

    # Detalles por calidad
    detalles = AcumFrutaaux.objects.annotate(
        semana=ExtractWeek('fecha'),
        anio=ExtractIsoYear('fecha')
    ).filter(orden__in=ordenes_abiertas,correo=nombre_usuario).exclude(status="Anulado")

    boleta_ids = detalles.values_list('boleta', flat=True).distinct()
    boletas = Boletas.objects.filter(boleta__in=boleta_ids)
    boletas_dict = {b.boleta: b for b in boletas}

    agrupados = defaultdict(lambda: {
        'aprovechamiento_libras': 0,
        'total_distribuido_libras': 0,
    })

    for detalle in detalles:
        boleta = boletas_dict.get(detalle.boleta)
        if not boleta:
            continue

        clave = formar_clave2(detalle.finca, detalle.cultivo, detalle.orden, detalle.estructura, detalle.variedad)
        calidad = (boleta.calidad or '').strip().lower()
        libras = detalle.libras or 0

        if 'aprovechamiento' in calidad:
            agrupados[clave]['aprovechamiento_libras'] += libras

        agrupados[clave]['total_distribuido_libras'] += libras

    
    
    areas_sumadas_qs = detallesEstructuras.objects.values('orden', 'cultivo','estructura','variedad').annotate(total_area=Sum('area'))
    areas_sumadas = {(a['orden'], a['cultivo'], a['estructura'], a['variedad']): a['total_area'] for a in areas_sumadas_qs}



    # Armar resultado final
    resultado = []
    for clave, datos in agrupados.items():
        finca, cultivo, orden, estructura, variedad = clave
        recepcion_libras = recepciones_dict.get(clave, 0)
        procesado_libras = datos['total_distribuido_libras']
        pendiente_libras = recepcion_libras - procesado_libras
        if pendiente_libras < 0:
            pendiente_libras = 0

        # Convertir libras a kilos
        kilos_recibidos = round(recepcion_libras / 2.20462, 2)
        kilos_procesados = round(procesado_libras / 2.20462, 2)
        kilos_pendientes = round(pendiente_libras / 2.20462, 2)

        # Calcular kg/m² con libras de aprovechamiento
        
        clave_area = (orden, cultivo, estructura, variedad)
        area_m2 = areas_sumadas.get(clave_area, 0)

        aprovechamiento_kg = datos['aprovechamiento_libras'] / 2.20462 if datos['aprovechamiento_libras'] else 0
        kg_m2 = round(aprovechamiento_kg / area_m2, 2) if area_m2 > 0 else 0
        

        resultado.append({
            'proveedor': finca,
            'cultivo': cultivo,
            'orden': orden,
            'estructura': estructura,
            'variedad': variedad,
            'kilos_totales': kilos_recibidos,
            'kilos_procesados': kilos_procesados,
            'kilos_pendientes': kilos_pendientes,
            'kg_m2': kg_m2,
            'area':area_m2,
            'libras':procesado_libras
        })

    registros_json = json.dumps(resultado, default=str)
    df = pd.DataFrame(resultado)
    tabla_html = df.to_html(classes="table table-striped", index=False)

    return render(request, 'plantaE/reportegerencial/salidasFruta_aprovechamientosemp.html', {
        'registros': resultado,
        'tabla_html': tabla_html,
        'registros_json': registros_json,
    })

def poraprovechamientosempger(request):
    hoy = timezone.now().date()

    fecha_max = AcumFruta.objects.aggregate(max_fecha=Max('fecha'))['max_fecha']
    if not fecha_max:
        fecha_max = hoy

    ordenes_abiertas = datosProduccion.objects.filter(status='Abierta').values_list('orden', flat=True)

    # Total de libras por variedad desde AcumFruta
    acumfrutadatos = AcumFruta.objects.filter(orden__in=ordenes_abiertas).annotate(
        semana=ExtractWeek('fecha'),
        anio=ExtractIsoYear('fecha')
    ).values('finca', 'cultivo', 'orden', 'estructura', 'variedad'
    ).annotate(total_libras=Sum('libras')).exclude(status="Anulado").order_by()

    recepciones_dict = {
        formar_clave2(r['finca'], r['cultivo'], r['orden'], r['estructura'], r['variedad']): r['total_libras']
        for r in acumfrutadatos
    }

    # Detalles por calidad
    detalles = AcumFrutaaux.objects.annotate(
        semana=ExtractWeek('fecha'),
        anio=ExtractIsoYear('fecha')
    ).filter(orden__in=ordenes_abiertas).exclude(status="Anulado")

    boleta_ids = detalles.values_list('boleta', flat=True).distinct()
    boletas = Boletas.objects.filter(boleta__in=boleta_ids)
    boletas_dict = {b.boleta: b for b in boletas}

    agrupados = defaultdict(lambda: {
        'aprovechamiento_libras': 0,
        'total_distribuido_libras': 0,
    })

    for detalle in detalles:
        boleta = boletas_dict.get(detalle.boleta)
        if not boleta:
            continue

        clave = formar_clave2(detalle.finca, detalle.cultivo, detalle.orden, detalle.estructura, detalle.variedad)
        calidad = (boleta.calidad or '').strip().lower()
        libras = detalle.libras or 0

        if 'aprovechamiento' in calidad:
            agrupados[clave]['aprovechamiento_libras'] += libras

        agrupados[clave]['total_distribuido_libras'] += libras

    
    
    areas_sumadas_qs = detallesEstructuras.objects.values('orden', 'cultivo','estructura','variedad').annotate(total_area=Sum('area'))
    areas_sumadas = {(a['orden'], a['cultivo'], a['estructura'], a['variedad']): a['total_area'] for a in areas_sumadas_qs}



    # Armar resultado final
    resultado = []
    for clave, datos in agrupados.items():
        finca, cultivo, orden, estructura, variedad = clave
        recepcion_libras = recepciones_dict.get(clave, 0)
        procesado_libras = datos['total_distribuido_libras']
        pendiente_libras = recepcion_libras - procesado_libras
        if pendiente_libras < 0:
            pendiente_libras = 0

        # Convertir libras a kilos
        kilos_recibidos = round(recepcion_libras / 2.20462, 2)
        kilos_procesados = round(procesado_libras / 2.20462, 2)
        kilos_pendientes = round(pendiente_libras / 2.20462, 2)

        # Calcular kg/m² con libras de aprovechamiento
        
        clave_area = (orden, cultivo, estructura, variedad)
        area_m2 = areas_sumadas.get(clave_area, 0)

        aprovechamiento_kg = datos['aprovechamiento_libras'] / 2.20462 if datos['aprovechamiento_libras'] else 0
        kg_m2 = round(aprovechamiento_kg / area_m2, 2) if area_m2 > 0 else 0
        

        resultado.append({
            'proveedor': finca,
            'cultivo': cultivo,
            'orden': orden,
            'estructura': estructura,
            'variedad': variedad,
            'kilos_totales': kilos_recibidos,
            'kilos_procesados': kilos_procesados,
            'kilos_pendientes': kilos_pendientes,
            'kg_m2': kg_m2,
            'area':area_m2,
            'libras':procesado_libras
        })

    registros_json = json.dumps(resultado, default=str)
    df = pd.DataFrame(resultado)
    tabla_html = df.to_html(classes="table table-striped", index=False)

    return render(request, 'plantaE/reportegerencial/salidasFruta_aprovechamientosempger.html', {
        'registros': resultado,
        'tabla_html': tabla_html,
        'registros_json': registros_json,
    })

def poraprovechamientosger(request):
    hoy = timezone.now().date()
    # Obtener fecha máxima en detallerecaux
    fecha_max = AcumFruta.objects.aggregate(max_fecha=Max('fecha'))['max_fecha']
    if not fecha_max:
        fecha_max = hoy  # fallback si no hay registros
    ordenes_abiertas = datosProduccion.objects.filter(status='Abierta').values_list('orden', flat=True)

    # Filtrar las libras totales por variedad desde AcumFruta
    acumfrutadatos = AcumFruta.objects.filter(orden__in=ordenes_abiertas
    ).annotate(
        semana=ExtractWeek('fecha'),
        anio=ExtractIsoYear('fecha')
    ).values('finca', 'cultivo', 'orden', 'estructura', 'variedad').annotate(total_libras=Sum('libras')).order_by()

    recepciones_dict = {
        formar_clave2(r['finca'], r['cultivo'], r['orden'], r['estructura'], r['variedad']): r['total_libras'] for r in acumfrutadatos
    }

    # Filtrar distribuciones desde AcumFrutaaux
    detalles = AcumFrutaaux.objects.annotate(
        semana=ExtractWeek('fecha'),
        anio=ExtractIsoYear('fecha')
    ).filter(orden__in=ordenes_abiertas)

    boleta_ids = detalles.values_list('boleta', flat=True).distinct()
    boletas = Boletas.objects.filter(boleta__in=boleta_ids)
    boletas_dict = {b.boleta: b for b in boletas}

    # Agrupar las libras por boleta
    agrupados = defaultdict(lambda: {'aprovechamiento': 0, 'devolución': 0, 'mediano': 0, 'total': 0})

    for detalle in detalles:
        boleta = boletas_dict.get(detalle.boleta)
        if not boleta:
            continue
        
        clave = formar_clave2(detalle.finca, detalle.cultivo, detalle.orden, detalle.estructura, detalle.variedad)
        calidad = (boleta.calidad or '').strip().lower()
        libras = detalle.libras or 0

        if 'aprovechamiento' in calidad:
            agrupados[clave]['aprovechamiento'] += libras
        elif 'devolución' in calidad:
            agrupados[clave]['devolución'] += libras
        elif 'mediano' in calidad:
            agrupados[clave]['mediano'] += libras

        agrupados[clave]['total'] += libras

    # Calcular los porcentajes de calidad
    resultado = []
    for (finca, cultivo, orden, estructura, variedad), datos in agrupados.items():
        total_distribuido = datos['total'] or 0
        recepcion_libras = recepciones_dict.get((finca, cultivo, orden, estructura, variedad), 0)
        pendiente = recepcion_libras - total_distribuido
        if pendiente < 0:
            pendiente = 0
        porcentaje_pendiente = round(pendiente * 100 / recepcion_libras, 2) if recepcion_libras else 0

        # Calcular porcentaje de devolución
        #porcentaje_devolucion = round(datos['devolución'] * 100 / recepcion_libras, 2) if recepcion_libras else 0

        resultado.append({
            'proveedor': finca,
            'cultivo': cultivo,
            'orden': orden,
            'estructura': estructura,
            'variedad': variedad,
            'libras': round(recepcion_libras, 2),
            'aprovechamiento': round(datos['aprovechamiento'] * 100 / total_distribuido, 2) if total_distribuido else 0,
            'mediano': round(datos['mediano'] * 100 / total_distribuido, 2) if total_distribuido else 0,
            'devolucion': round(datos['devolución'] * 100 / total_distribuido, 2) if total_distribuido else 0,
            'procesado': total_distribuido,
            'porcentaje_pendiente': porcentaje_pendiente,
        })

    registros_json = json.dumps(resultado, default=str)

    # Convertir los resultados en una tabla HTML
    df = pd.DataFrame(resultado)
    tabla_html = df.to_html(classes="table table-striped", index=False)

    return render(request, 'plantaE/reportegerencial/salidasFruta_aprovechamientosger.html', {
        'registros': resultado,
        'tabla_html': tabla_html,
        'registros_json': registros_json,
    })

def kgm2_semanal_aprovechamiento(request):
    ordenes_abiertas = datosProduccion.objects.filter(
        status='Abierta'
    ).values_list('orden', flat=True)

    # 🔹 Boletas que sean exactamente "Aprovechamiento"
    boletas_aprovechamiento = Boletas.objects.filter(
        calidad__iexact='Aprovechamiento'
    ).values_list('boleta', flat=True)

    # 🔹 Detalles filtrados SOLO por esas boletas
    detalles = AcumFrutaaux.objects.annotate(
        semana=ExtractWeek('fecha'),
        anio=ExtractIsoYear('fecha')
    ).filter(
        orden__in=ordenes_abiertas,
        boleta__in=boletas_aprovechamiento
    ).exclude(status="Anulado")

    # 🔹 Áreas por estructura
    areas_qs = detallesEstructuras.objects.values(
        'orden', 'cultivo', 'estructura', 'variedad'
    ).annotate(total_area=Sum('area'))

    areas = {
        (a['orden'], a['cultivo'], a['estructura'], a['variedad']): a['total_area']
        for a in areas_qs
    }

    # 🔹 Agrupar libras por semana
    agrupados = defaultdict(float)

    for d in detalles:
        clave = (
            d.finca,
            d.cultivo,
            d.orden,
            d.estructura,
            d.variedad,
            d.anio,
            d.semana
        )

        agrupados[clave] += d.libras or 0

    # 🔹 Construir resultado final
    resultado = []

    for clave, libras in agrupados.items():
        finca, cultivo, orden, estructura, variedad, anio, semana = clave

        area = areas.get((orden, cultivo, estructura, variedad), 0)
        kg = libras / 2.20462
        kg_m2 = round(kg / area, 2) if area > 0 else 0

        resultado.append({
            'finca': finca,
            'cultivo': cultivo,
            'orden': orden,
            'estructura': estructura,
            'variedad': variedad,
            'anio': anio,
            'semana': semana,
            'kg_m2': kg_m2,
            'area_m2': area
        })

    # 🔹 Tabla pivote
    df = pd.DataFrame(resultado)

    if not df.empty:
        tabla_pivote = pd.pivot_table(
            df,
            values='kg_m2',
            index=['finca', 'cultivo', 'orden', 'estructura', 'variedad'],
            columns=['anio', 'semana'],
            aggfunc='sum',
            fill_value=0
        )

        tabla_pivote.columns = [
            f"{sem}-{anio}" for anio, sem in tabla_pivote.columns
        ]

        tabla_pivote = (
            tabla_pivote
            .sort_index(axis=1)
            .replace(0, "")
            .reset_index()
        )

        tabla_html = tabla_pivote.to_html(
            table_id="tabla-pivote",
            index=False
        )
    else:
        tabla_html = "<p>No hay datos</p>"

    return render(
        request,
        'plantaE/reportegerencial/salidasFruta_aprovechamientosempgersem.html',
        {
            'tabla_html': tabla_html,
            'registros_json': json.dumps(resultado, default=str),
        }
    )

def poraprovechamientos(request):
    hoy = timezone.now().date()
    nombre_usuario=request.user.username
    # Obtener fecha máxima en detallerecaux
    fecha_max = AcumFruta.objects.filter(correo=nombre_usuario).aggregate(max_fecha=Max('fecha'))['max_fecha']
    if not fecha_max:
        fecha_max = hoy  # fallback si no hay registros
    ordenes_abiertas = datosProduccion.objects.filter(status='Abierta').values_list('orden', flat=True)

    # Filtrar las libras totales por variedad desde AcumFruta
    acumfrutadatos = AcumFruta.objects.filter(correo=nombre_usuario,orden__in=ordenes_abiertas
    ).annotate(
        semana=ExtractWeek('fecha'),
        anio=ExtractIsoYear('fecha')
    ).values('finca', 'cultivo', 'orden', 'estructura', 'variedad').annotate(total_libras=Sum('libras')).order_by()

    recepciones_dict = {
        formar_clave2(r['finca'], r['cultivo'], r['orden'], r['estructura'], r['variedad']): r['total_libras'] for r in acumfrutadatos
    }

    # Filtrar distribuciones desde AcumFrutaaux
    detalles = AcumFrutaaux.objects.annotate(
        semana=ExtractWeek('fecha'),
        anio=ExtractIsoYear('fecha')
    ).filter(correo=nombre_usuario,orden__in=ordenes_abiertas)

    boleta_ids = detalles.values_list('boleta', flat=True).distinct()
    boletas = Boletas.objects.filter(boleta__in=boleta_ids)
    boletas_dict = {b.boleta: b for b in boletas}

    # Agrupar las libras por boleta
    agrupados = defaultdict(lambda: {'aprovechamiento': 0, 'devolución': 0, 'mediano': 0, 'total': 0})

    for detalle in detalles:
        boleta = boletas_dict.get(detalle.boleta)
        if not boleta:
            continue
        
        clave = formar_clave2(detalle.finca, detalle.cultivo, detalle.orden, detalle.estructura, detalle.variedad)
        calidad = (boleta.calidad or '').strip().lower()
        libras = detalle.libras or 0

        if 'aprovechamiento' in calidad:
            agrupados[clave]['aprovechamiento'] += libras
        elif 'devolución' in calidad:
            agrupados[clave]['devolución'] += libras
        elif 'mediano' in calidad:
            agrupados[clave]['mediano'] += libras

        agrupados[clave]['total'] += libras

    # Calcular los porcentajes de calidad
    resultado = []
    for (finca, cultivo, orden, estructura, variedad), datos in agrupados.items():
        total_distribuido = datos['total'] or 0
        recepcion_libras = recepciones_dict.get((finca, cultivo, orden, estructura, variedad), 0)
        pendiente = recepcion_libras - total_distribuido
        if pendiente < 0:
            pendiente = 0
        porcentaje_pendiente = round(pendiente * 100 / recepcion_libras, 2) if recepcion_libras else 0

        # Calcular porcentaje de devolución
        #porcentaje_devolucion = round(datos['devolución'] * 100 / recepcion_libras, 2) if recepcion_libras else 0

        resultado.append({
            'proveedor': finca,
            'cultivo': cultivo,
            'orden': orden,
            'estructura': estructura,
            'variedad': variedad,
            'libras': round(recepcion_libras, 2),
            'aprovechamiento': round(datos['aprovechamiento'] * 100 / total_distribuido, 2) if total_distribuido else 0,
            'mediano': round(datos['mediano'] * 100 / total_distribuido, 2) if total_distribuido else 0,
            'devolucion': round(datos['devolución'] * 100 / total_distribuido, 2) if total_distribuido else 0,
            'procesado': total_distribuido,
            'porcentaje_pendiente': porcentaje_pendiente,
        })

    registros_json = json.dumps(resultado, default=str)

    # Convertir los resultados en una tabla HTML
    df = pd.DataFrame(resultado)
    tabla_html = df.to_html(classes="table table-striped", index=False)

    return render(request, 'plantaE/reportegerencial/salidasFruta_aprovechamientos.html', {
        'registros': resultado,
        'tabla_html': tabla_html,
        'registros_json': registros_json,
    })
