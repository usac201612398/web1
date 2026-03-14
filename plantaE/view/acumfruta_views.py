import json
import datetime
import pandas as pd

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.utils import timezone
from django.urls import reverse
from django.db.models import Q

from plantaE.models import (
    AcumFruta,
    salidasFruta,
    Recepciones
)

from plantaE.forms import acumFrutaForm

def acumFruta_consulta(request):
    if request.method == 'POST':
        # Leer los datos JSON del cuerpo de la solicitud
        data = json.loads(request.body)
        opcion1 = data.get('opcion1')
        opcion2 = data.get('opcion2')
        nombre_usuario = request.user.username

        # Filtra tus datos según la opción seleccionada
        datos = AcumFruta.objects.filter(cultivo=opcion1, fecha=opcion2, correo=nombre_usuario, libras__isnull=False).exclude(status="Anulado")

        df = pd.DataFrame(list(datos.values()), columns=['id', 'fecha', 'finca', 'viaje', 'orden', 'cultivo', 'variedad', 'cajas', 'libras', 'estructura'])

        df_agrupado = df.groupby(['orden', 'estructura', 'variedad'], as_index=False).agg(
            total_cajas=('cajas', 'sum'),
            total_libras=('libras', 'sum'),
            cultivo=('cultivo', 'first'),
            id=('id', 'first'),
            fecha=('fecha', 'first'),
            finca=('finca', 'first'),
            viaje=('viaje', 'first'),
            orden=('orden', 'first'),
            variedad=('variedad', 'first'),
            estructura=('estructura', 'first')
        )

        df_agrupado = df_agrupado.sort_values(by=['viaje', 'orden'])

        registros_finales = df_agrupado.to_dict(orient='records')

        # Crear un DataFrame a partir de los registros, incluyendo todas las columnas
        df_resumen = pd.DataFrame(list(datos.values()), columns=['fecha', 'finca', 'viaje', 'cultivo', 'cajas', 'libras'])

        # Agrupar por 'cultivo' y sumar las 'cajas' y 'libras'
        df_resumen_agrupado = df_resumen.groupby('cultivo', as_index=False).agg(
            total_cajas=('cajas', 'sum'),
            total_libras=('libras', 'sum'),
            viaje=('viaje', 'first'),
            cultivo=('cultivo', 'first'),
            fecha=('fecha', 'first'),
            finca=('finca', 'first')
        )

        registros_finales2 = df_resumen_agrupado.to_dict(orient='records')

        return JsonResponse({'datos': registros_finales, 'opcion1': opcion1, 'opcion2': opcion2, 'resumen': registros_finales2, 'correo': nombre_usuario}, safe=False)
    return render(request, 'plantaE/AcumFrutaDia_list.html')

def acumFruta_consultaValle(request):
    if request.method == 'POST':
        try:
            opcion1 = request.POST.get('opcion1')
            opcion2 = request.POST.get('opcion2')
            nombre_usuario = request.user.username

            # Filtra tus datos según la opción seleccionada
            datos = AcumFruta.objects.filter(cultivo=opcion1, fecha=opcion2, correo=nombre_usuario, libras__isnull=False).exclude(status="Anulado")
            registros = AcumFruta.objects.filter(cultivo=opcion1, fecha=opcion2, correo=nombre_usuario, libras__isnull=False).exclude(status="Anulado")

            if not datos.exists():
                return JsonResponse({'error': 'No se encontraron registros para los filtros aplicados.'}, status=404)

            # Crear DataFrame a partir de los datos
            df = pd.DataFrame(list(datos.values()), columns=['id', 'fecha', 'finca', 'viaje', 'orden', 'cultivo', 'variedad', 'cajas', 'libras', 'estructura'])

            # Agrupar los datos
            df_agrupado = df.groupby(['orden', 'estructura', 'variedad'], as_index=False).agg(
                total_cajas=('cajas', 'sum'),
                total_libras=('libras', 'sum'),
                cultivo=('cultivo', 'first'),
                id=('id', 'first'),
                fecha=('fecha', 'first'),
                finca=('finca', 'first'),
                viaje=('viaje', 'first'),
                orden=('orden', 'first'),
                variedad=('variedad', 'first'),
                estructura=('estructura', 'first')
            )
            df_agrupado = df_agrupado.sort_values(by=['viaje', 'orden'])
            registros_finales = df_agrupado.to_dict(orient='records')

            # Agrupar resumen
            df_resumen = pd.DataFrame(list(registros.values()), columns=['fecha', 'finca', 'cultivo', 'viaje', 'cajas', 'libras'])
            df_agrupado_resumen = df_resumen.groupby('cultivo', as_index=False).agg(
                total_cajas=('cajas', 'sum'),
                total_libras=('libras', 'sum'),
                viaje=('viaje', 'first'),
                cultivo=('cultivo', 'first'),
                fecha=('fecha', 'first'),
                finca=('finca', 'first')
            )

            registros_finales2 = df_agrupado_resumen.to_dict(orient='records')

            return JsonResponse({'datos': registros_finales, 'opcion1': opcion1, 'opcion2': opcion2, 'resumen': registros_finales2}, safe=False)

        except Exception as e:
            # Manejo de excepciones
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'plantaE/AcumFrutaDia_listValle.html')

def acumFruta_list(request):
    today = timezone.localtime(timezone.now()).date()
    nombre_usuario = request.user.username
    salidas = AcumFruta.objects.filter(fecha=today,correo=nombre_usuario).exclude(status="Anulado")
    
    salidas = salidas.order_by('-created_at')
    
    return render(request, 'plantaE/AcumFrutaDia_list.html', {'registros': salidas})

def acumFruta_list2(request):
    today = timezone.localtime(timezone.now()).date()
    salidas = AcumFruta.objects.filter(
        id__gte=10519
    ).filter(
        Q(fecha=today) | Q(status__isnull=True) | Q(status='')
    ).order_by('-created_at')

    return render(request, 'plantaE/AcumFrutaDia_list2.html', {'registros': salidas})

def acumFruta_detail(request, pk):
    salidas = get_object_or_404(AcumFruta, pk=pk)
    return render(request, 'plantaE/AcumFrutaDia_detail.html', {'registros': salidas})

def acumFruta_detail2(request, pk):
    salidas = get_object_or_404(AcumFruta, pk=pk)
    return render(request, 'plantaE/AcumFrutaDia_detail2.html', {'registros': salidas})

def  acumFruta_create(request):
    if request.method == 'POST':
        form = acumFrutaForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                # Manejar excepciones específicas (por ejemplo, UniqueConstraintError)
                return JsonResponse({'error': str(e)}, status=400)
            return redirect('acumFruta_list')
        else:
             # Imprimir errores para depuración
            return JsonResponse({'errores': form.errors}, status=400)
    else:

        hoy = datetime.date.today()
        #dia_semana = calendar.day_name[hoy.weekday()]  # e.g., 'Monday'
        
        initial_data = {
            'fecha': hoy
        }
        form = acumFrutaForm(initial=initial_data)
    return render(request, 'plantaE/AcumFrutaDia_form.html', {'form': form})

def acumFruta_update(request, pk):
    salidas = get_object_or_404(AcumFruta, pk=pk)
    if request.method == 'POST':
        form = acumFrutaForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('acumFruta_list2')
    else:
        form = acumFrutaForm(instance=salidas)
    return render(request, 'plantaE/AcumFrutaDia_form.html', {'form': form})

def acumFruta_delete(request, pk):

    salidas = get_object_or_404(AcumFruta, pk=pk)

    
    # Verificamos si tiene una recepción activa
    tiene_recepcion = (
        salidas.recepcion and
        Recepciones.objects.filter(recepcion=salidas.recepcion).exists()
    )

    # Si ya tiene recepción, mostrar alerta y redireccionar
    if tiene_recepcion:
        return render(request, 'plantaE/acumFruta_confirm_delete.html', {
            'alert_message': "No se puede anular este viaje porque ya tiene una recepción asignada. Anule la recepción primero.",
            'redirect_url': reverse('acumFrutaDia_list')
        })

    if request.method == 'POST':
        salidas.status = 'Anulado'
        salidas.save()
        salidasFruta.objects.filter(
            fecha=salidas.fecha,
            finca=salidas.finca,
            cultivo=salidas.cultivo,
            variedad=salidas.variedad,
            viaje=salidas.viaje,
            orden = salidas.orden,
            correo = salidas.correo,
            status__isnull=True  # Solo los abiertos
        ).update(status='Anulado')
        
        return render(request, 'plantaE/acumFruta_confirm_delete.html', {
            'alert_message': "El registro fue anulado correctamente.",
            'redirect_url': reverse('acumFrutaDia_list')
        })

    return render(request, 'plantaE/acumFruta_confirm_delete.html', {'registros': salidas})

def acumFruta_delete2(request, pk):

    salidas = get_object_or_404(AcumFruta, pk=pk)

    # Verificamos si tiene una recepción activa
    tiene_recepcion = (
        salidas.recepcion and
        Recepciones.objects.filter(recepcion=salidas.recepcion).exists()
    )

    # Si ya tiene recepción, mostrar alerta y redireccionar
    if tiene_recepcion:
        return render(request, 'plantaE/acumFruta_confirm_delete2.html', {
            'alert_message': "No se puede anular este viaje porque ya tiene una recepción asignada. Anule la recepción primero.",
            'redirect_url': reverse('acumFruta_list2')
        })
    
    if request.method == 'POST':
        salidas.status = 'Anulado'
        salidas.save()
        salidasFruta.objects.filter(
            fecha=salidas.fecha,
            finca=salidas.finca,
            cultivo=salidas.cultivo,
            variedad=salidas.variedad,
            viaje=salidas.viaje,
            correo = salidas.correo,
            orden = salidas.orden,
            status__isnull=True  # Solo los abiertos
        ).update(status='Anulado')
        
        return render(request, 'plantaE/acumFruta_confirm_delete2.html', {
            'alert_message': "El registro fue anulado correctamente.",
            'redirect_url': reverse('acumFruta_list2')
        })
    
    return render(request, 'plantaE/acumFruta_confirm_delete2.html', {'registros': salidas})
