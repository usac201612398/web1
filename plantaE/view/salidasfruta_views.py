import json
import datetime
import pandas as pd
from .auxiliares import *
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.utils import timezone
from django.urls import reverse
from django.db.models import Q, Sum
from django.db import transaction

from plantaE.models import (
    salidasFruta,
    AcumFruta,
    usuariosAppFruta,
    detallesEstructuras,
    datosProduccion,
    Recepciones
)

from plantaE.forms import salidasFrutaForm

def article_list(request):

    today = timezone.localtime(timezone.now()).date()
    nombre_usuario = request.user.username
    salidas = salidasFruta.objects.filter(fecha=today,correo=nombre_usuario, status__isnull=True)
    salidas = salidas.order_by('-created_at')
    
    return render(request, 'plantaE/salidasFruta/salidasFruta_list.html', {'registros': salidas})

def salidasFruta_list(request):
    today = timezone.localtime(timezone.now()).date()

    salidas = salidasFruta.objects.filter(
        id__gte=8688
    ).filter(
        Q(fecha=today) | Q(status__isnull=True) | Q(status='')
    ).order_by('-created_at')

    return render(request, 'plantaE/salidasFruta/salidasFruta_list2.html', {'registros': salidas})

def article_listValle(request):
    
    today = timezone.localtime(timezone.now()).date()
    nombre_usuario = request.user.username
    salidas = salidasFruta.objects.filter(fecha=today,correo=nombre_usuario, status__isnull=True)
    salidas = salidas.order_by('-created_at')
    
    return render(request, 'plantaE/salidasFruta/salidasFruta_listValle.html', {'registros': salidas})

def article_detail(request, pk):
    salidas = get_object_or_404(salidasFruta, pk=pk)
    return render(request, 'plantaE/salidasFruta/salidasFruta_detail.html', {'registros': salidas})

def guardar_plantilla(request):
    data = json.loads(request.body)
    mensaje = data['array']
    #mensaje = request.POST.get('array')
    acumuladolibras = 0
    for i in mensaje:
        datos = salidasFruta.objects.filter(fecha=i[8],finca=i[7],cultivo=i[2]).exclude(status='Anulado')
        # Calcular las sumas
        suma_cajas = datos.aggregate(Sum('cajas'))['cajas__sum'] or 0
        suma_libras = datos.aggregate(Sum('libras'))['libras__sum'] or 0

        pesoxcaja = suma_libras/suma_cajas
        cajas = int(i[5])
        librasestructura = cajas*pesoxcaja
        acumuladolibras = acumuladolibras+librasestructura
        AcumFruta.objects.create(fecha=i[8],finca=i[7],orden=i[1],cultivo=i[2],estructura=i[3],variedad=i[4],cajas=i[5],correo=i[9],libras=librasestructura)
    
    return JsonResponse({'mensaje':mensaje})

def guardar_plantillaRio(request):
    data = json.loads(request.body)
    mensaje = data['array']
    #mensaje = request.POST.get('array')
    for i in mensaje:
        
        salidasFruta.objects.create(fecha=i[7],finca=i[5],cultivo=i[1],variedad=i[2],cajas=i[3],correo=i[8],viaje=i[6],encargado=i[0])
        
    return JsonResponse({'mensaje':mensaje})

def cuadrar_RioDia(request):
    today = timezone.now().date()
    nombre_usuario = request.user.username
     # Obtener todos los registros para el usuario y la fecha
    registros = salidasFruta.objects.filter(fecha=today, correo=nombre_usuario, libras__isnull=False).exclude(status='Anulado')

   # Crear un DataFrame a partir de los registros, incluyendo todas las columnas
    df = pd.DataFrame(list(registros.values()),columns=['fecha','finca','cultivo','variedad','cajas','libras','created_at'])

    # Agrupar por 'variedad' y sumar las 'cajas'
    df_agrupado = df.groupby(['variedad','cultivo'], as_index=False).agg(
        total_cajas=('cajas', 'sum'),
        total_libras=('libras', 'sum'),
            cultivo=('cultivo', 'first'),  # Conservar el primer correo asociado
        fecha=('fecha', 'first'),
        variedad=('variedad', 'first'),
        finca=('finca', 'first'),
        created_at=('created_at', 'first')    # Conservar la primera fecha asociada
    )
    df_agrupado['total_libras'] = df_agrupado['total_libras'].round(0)
    # Convertir el DataFrame a una lista de diccionarios para pasarlo a la plantilla
    registros_finales = df_agrupado.to_dict(orient='records')

    # Agrupar por 'cultivo' y sumar las 'cajas'
    df_agrupado = df.groupby('cultivo', as_index=False).agg(
        total_cajas=('cajas', 'sum'),
        total_libras=('libras', 'sum'),
        cultivo=('cultivo', 'first'),  # Conservar el primer correo asociado
        fecha=('fecha', 'first'),
        variedad=('variedad', 'first'),
        finca=('finca', 'first'),
        created_at=('created_at', 'first')    # Conservar la primera fecha asociada
    )
    df_agrupado['total_libras'] = df_agrupado['total_libras'].round(0)
    registros_finales2 = df_agrupado.to_dict(orient='records')

    if request.method == 'POST':
        opcion1 = request.POST.get('opcion1')
        opcion2 = request.POST.get('opcion2')
         # Obtener todos los registros para el usuario y la fecha
        registros = salidasFruta.objects.filter(fecha=opcion2,cultivo=opcion1,correo=nombre_usuario,libras__isnull=False).exclude(status='Anulado')

    # Crear un DataFrame a partir de los registros, incluyendo todas las columnas
        df = pd.DataFrame(list(registros.values()),columns=['fecha','finca','cultivo','variedad','cajas','libras','created_at'])

        # Agrupar por 'variedad' y sumar las 'cajas'
        df_agrupado = df.groupby(['variedad','cultivo'], as_index=False).agg(
            total_cajas=('cajas', 'sum'),
            total_libras=('libras', 'sum'),
            cultivo=('cultivo', 'first'),  # Conservar el primer correo asociado
            fecha=('fecha', 'first'),
            variedad=('variedad', 'first'),
            finca=('finca', 'first'),
            created_at=('created_at', 'first')    # Conservar la primera fecha asociada
        )
        df_agrupado['total_libras'] = df_agrupado['total_libras'].round(0)
        # Convertir el DataFrame a una lista de diccionarios para pasarlo a la plantilla
        registros_finales = df_agrupado.to_dict(orient='records')

        # Agrupar por 'cultivo' y sumar las 'cajas'
        df_agrupado = df.groupby('cultivo', as_index=False).agg(
            total_cajas=('cajas', 'sum'),
            total_libras=('libras', 'sum'),
            cultivo=('cultivo', 'first'),  # Conservar el primer correo asociado
            fecha=('fecha', 'first'),
            variedad=('variedad', 'first'),
            finca=('finca', 'first'),
            created_at=('created_at', 'first')    # Conservar la primera fecha asociada
        )
        df_agrupado['total_libras'] = df_agrupado['total_libras'].round(0)
        registros_finales2 = df_agrupado.to_dict(orient='records')
        return JsonResponse({'datos': list(registros_finales),'opcion1':opcion1,'opcion2':opcion2,'resumen':registros_finales2}, safe=False)

    return render(request, 'plantaE/salidasFruta/salidasFruta_cuadre.html', {'registros': registros_finales, 'registros2': registros_finales2})

def cuadrar_ValleDia(request):
    
    today = timezone.now().date()
    nombre_usuario = request.user.username
    
    # Obtener todos los registros para el usuario y la fecha
    registros = salidasFruta.objects.filter(fecha=today, correo=nombre_usuario,libras__isnull=False).exclude(status='Anulado')

    # Crear un DataFrame a partir de los registros, incluyendo todas las columnas
    df = pd.DataFrame(list(registros.values()),columns=['fecha','finca','cultivo','variedad','cajas','libras','created_at'])

    # Agrupar por 'variedad' y sumar las 'cajas'
    df_agrupado = df.groupby(['variedad','cultivo'], as_index=False).agg(
        total_cajas=('cajas', 'sum'),
        total_libras=('libras', 'sum'),
        cultivo=('cultivo', 'first'),  # Conservar el primer correo asociado
        fecha=('fecha', 'first'),
        variedad=('variedad', 'first'),
        finca=('finca', 'first'),
        created_at=('created_at', 'first')    # Conservar la primera fecha asociada
    )
    df_agrupado['total_libras'] = df_agrupado['total_libras'].round(0)
    # Convertir el DataFrame a una lista de diccionarios para pasarlo a la plantilla
    registros_finales = df_agrupado.to_dict(orient='records')

    # Agrupar por 'cultivo' y sumar las 'cajas'
    df_agrupado = df.groupby('cultivo', as_index=False).agg(
        total_cajas=('cajas', 'sum'),
        total_libras=('libras', 'sum'),
        cultivo=('cultivo', 'first'),  # Conservar el primer correo asociado
        fecha=('fecha', 'first'),
        variedad=('variedad', 'first'),
        finca=('finca', 'first'),
        created_at=('created_at', 'first')    # Conservar la primera fecha asociada
    )
    df_agrupado['total_libras'] = df_agrupado['total_libras'].round(0)
    registros_finales2 = df_agrupado.to_dict(orient='records')

    if request.method == 'POST':

        opcion1 = request.POST.get('opcion1')
        opcion2 = request.POST.get('opcion2')
         # Obtener todos los registros para el usuario y la fecha
        registros = salidasFruta.objects.filter(fecha=opcion2,cultivo=opcion1,correo=nombre_usuario,libras__isnull=False).exclude(status='Anulado')

    # Crear un DataFrame a partir de los registros, incluyendo todas las columnas
        df = pd.DataFrame(list(registros.values()),columns=['fecha','finca','cultivo','variedad','cajas','libras','created_at'])

        # Agrupar por 'variedad' y sumar las 'cajas'
        df_agrupado = df.groupby(['variedad','cultivo'], as_index=False).agg(
            total_cajas=('cajas', 'sum'),
            total_libras=('libras', 'sum'),
            cultivo=('cultivo', 'first'),  # Conservar el primer correo asociado
            fecha=('fecha', 'first'),
            variedad=('variedad', 'first'),
            finca=('finca', 'first'),
            created_at=('created_at', 'first')    # Conservar la primera fecha asociada
        )
        df_agrupado['total_libras'] = df_agrupado['total_libras'].round(0)
        # Convertir el DataFrame a una lista de diccionarios para pasarlo a la plantilla
        registros_finales = df_agrupado.to_dict(orient='records')

        # Agrupar por 'cultivo' y sumar las 'cajas'
        df_agrupado = df.groupby('cultivo', as_index=False).agg(
            total_cajas=('cajas', 'sum'),
            total_libras=('libras', 'sum'),
            cultivo=('cultivo', 'first'),  # Conservar el primer correo asociado
            fecha=('fecha', 'first'),
            variedad=('variedad', 'first'),
            finca=('finca', 'first'),
            created_at=('created_at', 'first')    # Conservar la primera fecha asociada
        )
        df_agrupado['total_libras'] = df_agrupado['total_libras'].round(0)
        registros_finales2 = df_agrupado.to_dict(orient='records')
        return JsonResponse({'datos': list(registros_finales),'opcion1':opcion1,'opcion2':opcion2,'resumen':registros_finales2}, safe=False)

    return render(request, 'plantaE/salidasFruta/salidasFruta_cuadreValle.html', {'registros': registros_finales, 'registros2': registros_finales2})

#API que crea registros para salidasFruta y acumFruta en cada viaje.
def guardar_plantillaValle(request):
    data = json.loads(request.body)
    mensaje = data['array']
    #mensaje = request.POST.get('array')
   
    for elemento in mensaje:
        elemento[5] = int(elemento[5])

    df = pd.DataFrame(mensaje,columns=['Encargado','Orden','Cultivo','Estructura','Variedad','Cajas','Blank','Finca','Viaje','Fecha','Correo'])
    
    resultado = df.groupby(['Orden','Cultivo','Variedad',] ).agg({
        'Encargado': 'first',  # O 'last', 'min', 'max', etc.
        'Finca': 'first',
        'Viaje': 'first',
        'Fecha': 'first',
        'Correo': 'first',
        'Cajas': 'sum'
    }).reset_index()
    resultado_lista = resultado.to_dict(orient='records')
    
    fecha = df['Fecha'].iloc[0]
    viaje = df['Viaje'].iloc[0]
    correo = df['Correo'].iloc[0]

    existe = salidasFruta.objects.filter(
        fecha=fecha,
        viaje=viaje,
        correo = correo
    ).exclude(status='Anulado').exists()

    if existe:
        return JsonResponse({
            'error': f'El {viaje} del día {fecha} ya fue cargado.'
        }, status=400)
     # Creación de registros en la base de datos
    with transaction.atomic():
        for i in resultado_lista:

            salida = salidasFruta.objects.create(
                fecha=i['Fecha'],
                finca=i['Finca'],
                encargado=i['Encargado'],
                cultivo=i['Cultivo'],
                variedad=i['Variedad'],
                cajas=i['Cajas'],
                viaje=i['Viaje'],
                orden=i['Orden'],
                correo=i['Correo']
            )

            registros = df[
                (df['Orden'] == i['Orden']) &
                (df['Cultivo'] == i['Cultivo']) &
                (df['Variedad'] == i['Variedad'])
            ]

            for _, row in registros.iterrows():
                AcumFruta.objects.create(
                    fecha=row['Fecha'],
                    finca=row['Finca'],
                    orden=row['Orden'],
                    cultivo=row['Cultivo'],
                    estructura=row['Estructura'],
                    variedad=row['Variedad'],
                    cajas=row['Cajas'],
                    correo=row['Correo'],
                    viaje=row['Viaje'],
                    nsalidafruta=salida.id
                )
    return JsonResponse({'mensaje':resultado_lista})                  

def article_create_plantilla(request):
    
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
    datos = usuariosAppFruta.objects.filter(correo=nombre_usuario).values('finca','encargado')
    estructura = detallesEstructuras.objects.filter(finca=list(datos)[0]['finca']).values('finca','orden','estructura','variedad','cultivo').distinct()
    estructura = estructura.order_by('estructura')
    context = {

        'usuario': nombre_usuario,
        'registros': list(estructura),
        'fecha': fecha_,
        'encargado': list(datos)[0]['encargado']
    }
    
    return render(request, 'plantaE/salidasFruta/salidasFruta_envio.html',context)

def article_create_plantillaValle(request):
    
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
    datos = usuariosAppFruta.objects.filter(correo=nombre_usuario).values('finca','encargado')
    estructura = detallesEstructuras.objects.filter(finca=list(datos)[0]['finca'],encargado=list(datos)[0]['encargado']).values('finca','orden','estructura','variedad','cultivo').distinct()
    estructura = estructura.order_by('orden')
    
    # Ahora filtramos por el estado 'abierto' desde la tabla datosproduccion
    # Hacemos una segunda consulta para obtener los status de las órdenes y filtramos las abiertas
    ordenes_abiertas = datosProduccion.objects.filter(  # Filtramos las ordenes que están en la lista de ordenes de estructura
    status='Abierta'  # Filtramos solo las órdenes abiertas
    ).values('orden')
    
    # Extraemos los números de orden de las órdenes abiertas
    ordenes_abiertas = [item['orden'] for item in ordenes_abiertas]
    #JsonResponse({'ordenes':list(ordenes_abiertas)})
    # Filtramos la estructura para que solo contenga las órdenes abiertas
    estructura_abierta = estructura.filter(orden__in=ordenes_abiertas)

    estructura_abierta = estructura_abierta.order_by('orden')

    context = {

        'usuario': nombre_usuario,
        'registros': list(estructura_abierta),
        'fecha': fecha_,
        'encargado': list(datos)[0]['encargado']
    }
    
    return render(request, 'plantaE/salidasFruta/salidasFruta_envioValle.html',context)

def article_create(request):
    if request.method == 'POST':
        form = salidasFrutaForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                # Manejar excepciones específicas (por ejemplo, UniqueConstraintError)
                return JsonResponse({'error': str(e)}, status=400)
            return redirect('salidasFruta_list2')
        else:
             # Imprimir errores para depuración
            return JsonResponse({'errores': form.errors}, status=400)
    else:
        hoy = datetime.date.today()
        #dia_semana = calendar.day_name[hoy.weekday()]  # e.g., 'Monday'
        
        initial_data = {
            'fecha': hoy
        }
        form = salidasFrutaForm(initial=initial_data)
    return render(request, 'plantaE/salidasFruta/salidasFruta_form.html', {'form': form})

def get_correos_por_encargado(request):
    encargado = request.GET.get('encargado')

    # Correos y fincas asociadas al encargado
    correos = usuariosAppFruta.objects.filter(encargado=encargado).values_list('correo', flat=True).distinct()
    fincas = usuariosAppFruta.objects.filter(encargado=encargado).values_list('finca', flat=True).distinct()
    finca_list = list(fincas)

    # Cultivos y variedades filtrados por las fincas encontradas
    cultivos = detallesEstructuras.objects.filter(finca__in=finca_list).values_list('cultivo', flat=True).distinct()
    variedades = detallesEstructuras.objects.filter(finca__in=finca_list).values_list('variedad', flat=True).distinct()
    ordenes = detallesEstructuras.objects.filter(finca__in=finca_list).values_list('orden', flat=True).distinct()
    estructuras = detallesEstructuras.objects.filter(finca__in=finca_list).values_list('estructura', flat=True).distinct()

    return JsonResponse({
        'correos': list(correos),
        'fincas': finca_list,
        'ordenes':list(ordenes),
        'cultivos': list(cultivos),
        'variedades': list(variedades),
        'estructura': list(estructuras),
    })

def article_formPlantilla(request):
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
    datos = usuariosAppFruta.objects.filter(correo=nombre_usuario).values('finca','encargado')
    variedad = detallesEstructuras.objects.filter(finca=list(datos)[0]['finca']).values('finca','variedad','cultivo').distinct()
    estructura = variedad.order_by('cultivo')
    
    context = {
        'usuario': nombre_usuario,
        'registros': list(estructura),
        'fecha': fecha_,
        'encargado': list(datos)[0]['encargado']
    }
    
    return render(request, 'plantaE/salidasFruta/salidasFruta_formplantilla.html',context)

def article_update(request, pk):
    salidas = get_object_or_404(salidasFruta, pk=pk)
    if request.method == 'POST':
        form = salidasFrutaForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('salidasFruta_list2')
    else:
        form = salidasFrutaForm(instance=salidas)
    return render(request, 'plantaE/salidasFruta/salidasFruta_form.html', {'form': form})

def article_delete(request, pk):
    salidas = get_object_or_404(salidasFruta, pk=pk)
    # Verificamos si tiene una recepción activa
    tiene_recepcion = (
        salidas.recepcion and
        Recepciones.objects.filter(recepcion=salidas.recepcion).exists()
    )

    # Si ya tiene recepción, mostrar alerta y redireccionar
    if tiene_recepcion:
        return render(request, 'plantaE/salidasFruta/salidasFruta_confirm_delete.html', {
            'alert_message': "No se puede anular este viaje porque ya tiene una recepción asignada. Anule la recepción primero.",
            'redirect_url': reverse('salidasFruta_list')
        })
    
    if request.method == 'POST':
        salidas.status = 'Anulado'
        salidas.save()
        AcumFruta.objects.filter(
            fecha=salidas.fecha,
            finca=salidas.finca,
            cultivo=salidas.cultivo,
            variedad=salidas.variedad,
            viaje=salidas.viaje,
            orden=salidas.orden,
            correo = salidas.correo,
            status__isnull=True  # Solo los abiertos
        ).update(status='Anulado')
        return render(request, 'plantaE/salidasFruta/salidasFruta_confirm_delete.html', {
            'alert_message': "El registro fue anulado correctamente.",
            'redirect_url': reverse('salidasFruta_list')
        })
    return render(request, 'plantaE/salidasFruta/salidasFruta_confirm_delete.html', {'registros': salidas})

def article_delete2(request, pk):
    salidas = get_object_or_404(salidasFruta, pk=pk)

    # Verificamos si tiene una recepción activa
    tiene_recepcion = (
        salidas.recepcion and
        Recepciones.objects.filter(recepcion=salidas.recepcion).exists()
    )

    # Si ya tiene recepción, mostrar alerta y redireccionar
    if tiene_recepcion:
        return render(request, 'plantaE/salidasFruta/salidasFruta_confirm_delete2.html', {
            'alert_message': "No se puede anular este viaje porque ya tiene una recepción asignada. Anule la recepción primero.",
            'redirect_url': reverse('salidasFruta_list2')
        })

    # Si es POST, entonces anular
    if request.method == 'POST':
        salidas.status = 'Anulado'
        salidas.save()

        AcumFruta.objects.filter(
            fecha=salidas.fecha,
            finca=salidas.finca,
            cultivo=salidas.cultivo,
            variedad=salidas.variedad,
            viaje=salidas.viaje,
            orden=salidas.orden,
            correo=salidas.correo,
            status__isnull=True
        ).update(status='Anulado')

        return render(request, 'plantaE/salidasFruta/salidasFruta_confirm_delete2.html', {
            'alert_message': "El registro fue anulado correctamente.",
            'redirect_url': reverse('salidasFruta_list2')
        })

    # Si no hay recepción y aún no es POST, mostrar confirmación normal
    return render(request, 'plantaE/salidasFruta/salidasFruta_confirm_delete2.html', {
        'registros': salidas
    })

def article_deleteValle(request, pk):

    salidas = get_object_or_404(salidasFruta, pk=pk)

    # Verificamos si tiene una recepción activa
    tiene_recepcion = (
        salidas.recepcion and
        Recepciones.objects.filter(recepcion=salidas.recepcion).exclude(status='Anulado').exists()
    )

    if tiene_recepcion:
        return render(request, 'plantaE/salidasFruta/salidasFruta_confirm_deleteValle.html', {
            'alert_message': "No se puede anular este viaje porque ya tiene una recepción asignada. Anule la recepción primero.",
            'redirect_url': reverse('salidasFruta_listValle')
        })

    if request.method == 'POST':

        with transaction.atomic():

            # anular salida
            salidas.status = 'Anulado'
            salidas.save()

            # anular todos los acumFruta relacionados
            AcumFruta.objects.filter(
                nsalidafruta=salidas.id
            ).exclude(status='Anulado').update(status='Anulado')

        return render(request, 'plantaE/salidasFruta/salidasFruta_confirm_deleteValle.html', {
            'alert_message': "El registro fue anulado correctamente.",
            'redirect_url': reverse('salidasFruta_listValle')
        })

    return render(request, 'plantaE/salidasFruta/salidasFruta_confirm_deleteValle.html', {'registros': salidas})

def salidasFruta_detail2(request, pk):
    salidas = get_object_or_404(salidasFruta, pk=pk)
    return render(request, 'plantaE/salidasFruta/salidasFruta_detail2.html', {'registros': salidas})

