from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from openpyxl import Workbook
# Create your views here.
from django.shortcuts import get_object_or_404, redirect
from .models import Actpeso, paramenvlocales,enviosrec,AcumFrutaaux,salidacontenedores, inventarioProdTermAux,productores,contenedores,Boletas, detallerecaux,detallerec,salidasFruta, usuariosAppFruta, datosProduccion, detallesProduccion, detallesEstructuras, Recepciones, Ccalidad,causasRechazo,inventarioProdTerm,productoTerm,cultivoxFinca,AcumFruta
from .forms import boletasForm,itemsForm, itemsenviosForm,salidacontenedoresForm,salidasFrutaForm, contenedoresForm,recepcionesForm, ccalidadForm, inventarioFrutaForm, acumFrutaForm
from django.db.models import Sum, Q, Max,Value as V
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
from django.db.models.functions import ExtractWeek, ExtractYear
from django.views.decorators.http import require_GET
from django.urls import reverse

def vascula_monitor(request):
    return render(request, 'plantaE/vascula.html')

def exportar_excel(request):
    if request.method == 'POST':
        opcion1 = request.POST.get('opcion1')
        # Crea un libro de Excel y una hoja
        wb = Workbook()
        ws = wb.active
        ws.title = 'Rio'

        # Obtén los datos de tu modelo
        datos_rio = AcumFruta.objects.filter(fecha=opcion1, finca="RIO").exclude(status='Anulado').values(
            "id","fecha", "finca", "orden", "cultivo", "variedad", "estructura", "cajas","correo","libras"
        ).order_by("orden")

        # Agrega los encabezados
        ws.append(["id","fecha", "finca", "orden", "cultivo", "variedad", "estructura", "cajas","correo","libras"])
        
        # Agrega los datos  
        for obj in datos_rio:
            row = [obj['id'],obj['fecha'], obj['finca'], obj['orden'], obj['cultivo'], obj['variedad'], obj['estructura'], obj['cajas'], obj['correo'], obj['libras']]
            ws.append(row)

        ws_valle = wb.create_sheet(title='Valle')
        
        # Filtra tus datos según la opción seleccionada
        datos_valle = AcumFruta.objects.filter(fecha=opcion1, finca="VALLE").exclude('Anulado').values(
            "id", "fecha", "finca", "orden", "cultivo", "variedad", "estructura", "cajas","correo","libras"
        )

        # Crea un DataFrame a partir de los datos
        df = pd.DataFrame(list(datos_valle))
        if not df.empty:
            # Agrupa los datos
            df_agrupado = df.groupby(['orden', 'estructura', 'variedad'], as_index=False).agg(
                id=('id', 'first'),
                fecha=('fecha', 'first'),
                finca=('finca', 'first'),
                orden=('orden', 'first'),
                cultivo=('cultivo', 'first'),
                variedad=('variedad', 'first'),
                estructura=('estructura', 'first'),
                total_cajas=('cajas', 'sum'),
                total_libras=('libras', 'sum'),
                correo = ('correo', 'first'),
            )

            df_agrupado = df_agrupado.sort_values(by='orden')

            # Agrega encabezados a la hoja Valle
            ws_valle.append(df_agrupado.columns.tolist())

            # Agrega los registros agrupados a la hoja Valle
            for record in df_agrupado.itertuples(index=False):
                ws_valle.append(record)  # Excluir el índice, si es necesario

        
        ws_provalle = wb.create_sheet(title='Provalle')
        
        # Filtra tus datos según la opción seleccionada
        datos_provalle = AcumFruta.objects.filter(fecha=opcion1, finca="PRODUCTOS DEL VALLE, S.A.").exclude(status='Anulado').values(
            "id", "fecha", "finca", "orden", "cultivo", "variedad", "estructura", "cajas","correo","libras"
        )
        df = pd.DataFrame(list(datos_provalle))
        if not df.empty:
            # Crea un DataFrame a partir de los datos

            # Agrupa los datos
            df_agrupado = df.groupby(['orden', 'estructura', 'variedad'], as_index=False).agg(
                id=('id', 'first'),
                fecha=('fecha', 'first'),
                finca=('finca', 'first'),
                orden=('orden', 'first'),
                cultivo=('cultivo', 'first'),
                variedad=('variedad', 'first'),
                estructura=('estructura', 'first'),
                total_cajas=('cajas', 'sum'),
                total_libras=('libras', 'sum'),
                correo = ('correo', 'first'),
            )

            df_agrupado = df_agrupado.sort_values(by='orden')

            # Agrega encabezados a la hoja Valle
            ws_provalle.append(df_agrupado.columns.tolist())

            # Agrega los registros agrupados a la hoja Valle
            for record in df_agrupado.itertuples(index=False):
                ws_provalle.append(record)  # Excluir el índice, si es necesario
        
        # Crea una respuesta HTTP que sirva el archivo Excel
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=envios.xlsx'

        # Guarda el libro de Excel en la respuesta
        wb.save(response)

        return response

    return render(request, 'plantaE/consulta_envios.html')

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

def pesos_list(request):
    today = timezone.now().date()
    salidas = Actpeso.objects.filter(fecha=today).exclude(status='Anulado')
    salidas = salidas.order_by('created')
    
    return render(request, 'plantaE/pesos_list.html', {'registros': salidas})

def pesos_detail(request, pk):
    salidas = get_object_or_404(Actpeso, pk=pk)
    return render(request, 'plantaE/pesos_detail.html', {'registros': salidas})

def article_list(request):

    today = timezone.localtime(timezone.now()).date()
    nombre_usuario = request.user.username
    salidas = salidasFruta.objects.filter(fecha=today,correo=nombre_usuario, status__isnull=True)
    salidas = salidas.order_by('-created_at')
    
    return render(request, 'plantaE/salidasFruta_list.html', {'registros': salidas})

def salidasFruta_list(request):
    today = timezone.localtime(timezone.now()).date()

    salidas = salidasFruta.objects.filter(
        id__gte=8688
    ).filter(
        Q(fecha=today) | Q(status__isnull=True) | Q(status='')
    ).order_by('-created_at')

    return render(request, 'plantaE/salidasFruta_list2.html', {'registros': salidas})

def pesos_delete(request, pk):
    salidas = get_object_or_404(Actpeso, pk=pk)
    recepcion = Recepciones.objects.filter(recepcion=salidas.recepcion)
    # Validar si tiene recepción asignada
    if recepcion.exists():
        return render(request, 'plantaE/pesos_confirm_delete.html', {
            'registros': salidas,
            'alert_message': "No se puede anular este peso porque ya tiene una recepción asignada, anule la recepcion.",
            'redirect_url': reverse('pesos_list')
        })

    if request.method == 'POST':
        salidas.status = 'Anulado'
        salidas.save()
        return render(request, 'plantaE/pesos_confirm_delete.html', {
            'alert_message': "El registro fue anulado correctamente.",
            'redirect_url': reverse('pesos_list')
        })

    return render(request, 'plantaE/pesos_confirm_delete.html', {'registros': salidas})

def article_listValle(request):
    
    today = timezone.localtime(timezone.now()).date()
    nombre_usuario = request.user.username
    salidas = salidasFruta.objects.filter(fecha=today,correo=nombre_usuario, status__isnull=True)
    salidas = salidas.order_by('-created_at')
    
    return render(request, 'plantaE/salidasFruta_listValle.html', {'registros': salidas})

def article_detail(request, pk):
    salidas = get_object_or_404(salidasFruta, pk=pk)
    return render(request, 'plantaE/salidasFruta_detail.html', {'registros': salidas})

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

def inventarioProd_grabarplantilla(request):
    data = json.loads(request.body)
    mensaje = data['array']
    
    for i in mensaje:
        pesostd = productoTerm.objects.filter(itemsapcode=i[0]).first()
        productor_ = productores.objects.filter(productor=i[4]).first()

        if not pesostd:
            return JsonResponse({'error': f"No se encontró producto estándar para código: {i[0]}"}, status=400)

        if not productor_:
            return JsonResponse({'error': f"No se encontró productor para: {i[4]}"}, status=400)

        try:
            pesotarima = 57
            tara = float(pesostd.taraxcaja) * int(i[2]) + pesotarima
            pesosintara = int(i[3]) - tara
            pesoestandar = float(pesostd.pesostdxcaja) * int(i[2])
            pesostdxcaja = pesostd.pesostdxcaja

            merma = max(0, pesosintara - pesoestandar)
            pesosinmerma = pesosintara - merma
            pesoporcaja = pesosintara / int(i[2]) if int(i[2]) != 0 else 0
            ordenemp = pesostd.orden
            pormerma = (merma / pesoestandar) * 100 if pesoestandar > 0 else 0

            if productor_.tipo == "EM":
                orden = "EM"
            else:
                orden = ordenemp

            inventarioProdTerm.objects.create(
                fecha=i[7],
                proveedor=i[4],
                cultivo=i[5],
                itemsapcode=i[0],
                itemsapname=i[1],
                cajas=i[2],
                categoria=i[6],
                libras=i[3],
                lbsintara=pesosintara,
                pesostd=pesoestandar,
                merma=merma,
                pesorxcaja=pesoporcaja,
                orden=orden,
                pesostdxcaja=pesostdxcaja,
                tara=tara,
                pesosinmerma=pesosinmerma,
                calidad1=pesostd.calidad1
            )
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({
        'mensaje': mensaje,
        'msm': f"Listo, se tiene una merma de: {round(pormerma, 2)}%"
    })  

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

    return render(request, 'plantaE/salidasFruta_cuadre.html', {'registros': registros_finales, 'registros2': registros_finales2})

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

    return render(request, 'plantaE/salidasFruta_cuadreValle.html', {'registros': registros_finales, 'registros2': registros_finales2})
    
def guardar_plantillaValle(request):
    data = json.loads(request.body)
    mensaje = data['array']
    #mensaje = request.POST.get('array')
   
    for elemento in mensaje:
        elemento[5] = int(elemento[5])

    df = pd.DataFrame(mensaje,columns=['Encargado','Orden','Cultivo','Estructura','Variedad','Cajas','Blank','Finca','Viaje','Fecha','Correo'])
    
    resultado = df.groupby(['Variedad','Orden'] ).agg({
        'Encargado': 'first',  # O 'last', 'min', 'max', etc.
        'Finca': 'first',
        'Viaje': 'first',
        'Fecha': 'first',
        'Cultivo': 'first',
        'Correo': 'first',
        'Cajas': 'sum'
    }).reset_index()
    resultado_lista = resultado.to_dict(orient='records')
     # Creación de registros en la base de datos
    for i in resultado_lista:
        salidasFruta.objects.create(
            fecha=i['Fecha'],       # Ajusta el nombre según tu modelo
            finca=i['Finca'],
            encargado=i['Encargado'],
            cultivo=i['Cultivo'],
            variedad=i['Variedad'],
            cajas=i['Cajas'],
            viaje=i['Viaje'],
            orden=i['Orden'],
            correo=i['Correo']
        )
    
    for i in mensaje:
        
        AcumFruta.objects.create(fecha=i[9],finca=i[7],orden=i[1],cultivo=i[2],estructura=i[3],variedad=i[4],cajas=i[5],correo=i[10],viaje=i[8])
    
    
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
    
    return render(request, 'plantaE/salidasFruta_envio.html',context)

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
    
    return render(request, 'plantaE/salidasFruta_envioValle.html',context)

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
    return render(request, 'plantaE/salidasFruta_form.html', {'form': form})

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
    
    return render(request, 'plantaE/salidasFruta_formplantilla.html',context)


def article_update(request, pk):
    salidas = get_object_or_404(salidasFruta, pk=pk)
    if request.method == 'POST':
        form = salidasFrutaForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('salidasFruta_list2')
    else:
        form = salidasFrutaForm(instance=salidas)
    return render(request, 'plantaE/salidasFruta_form.html', {'form': form})

def article_delete(request, pk):
    salidas = get_object_or_404(salidasFruta, pk=pk)
    # Verificamos si tiene una recepción activa
    tiene_recepcion = (
        salidas.recepcion and
        Recepciones.objects.filter(recepcion=salidas.recepcion).exists()
    )

    # Si ya tiene recepción, mostrar alerta y redireccionar
    if tiene_recepcion:
        return render(request, 'plantaE/salidasFruta_confirm_delete.html', {
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
        return render(request, 'plantaE/salidasFruta_confirm_delete.html', {
            'alert_message': "El registro fue anulado correctamente.",
            'redirect_url': reverse('salidasFruta_list')
        })
    return render(request, 'plantaE/salidasFruta_confirm_delete.html', {'registros': salidas})

def article_delete2(request, pk):
    salidas = get_object_or_404(salidasFruta, pk=pk)

    # Verificamos si tiene una recepción activa
    tiene_recepcion = (
        salidas.recepcion and
        Recepciones.objects.filter(recepcion=salidas.recepcion).exists()
    )

    # Si ya tiene recepción, mostrar alerta y redireccionar
    if tiene_recepcion:
        return render(request, 'plantaE/salidasFruta_confirm_delete2.html', {
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

        return render(request, 'plantaE/salidasFruta_confirm_delete2.html', {
            'alert_message': "El registro fue anulado correctamente.",
            'redirect_url': reverse('salidasFruta_list2')
        })

    # Si no hay recepción y aún no es POST, mostrar confirmación normal
    return render(request, 'plantaE/salidasFruta_confirm_delete2.html', {
        'registros': salidas
    })

def article_deleteValle(request, pk):

    salidas = get_object_or_404(salidasFruta, pk=pk)
    # Verificamos si tiene una recepción activa
    tiene_recepcion = (
        salidas.recepcion and
        Recepciones.objects.filter(recepcion=salidas.recepcion).exists()
    )

    # Si ya tiene recepción, mostrar alerta y redireccionar
    if tiene_recepcion:
        return render(request, 'plantaE/salidasFruta_confirm_deleteValle.html', {
            'alert_message': "No se puede anular este viaje porque ya tiene una recepción asignada. Anule la recepción primero.",
            'redirect_url': reverse('salidasFruta_listValle')
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
        return render(request, 'plantaE/salidasFruta_confirm_deleteValle.html', {
            'alert_message': "El registro fue anulado correctamente.",
            'redirect_url': reverse('salidasFruta_listValle')
        })
    return render(request, 'plantaE/salidasFruta_confirm_deleteValle.html', {'registros': salidas})

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

def salidasFruta_detail2(request, pk):
    salidas = get_object_or_404(salidasFruta, pk=pk)
    return render(request, 'plantaE/salidasFruta_detail2.html', {'registros': salidas})

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

def procesarrecepcion(request):

    data = json.loads(request.body)
    mensaje = data['array']
    #mensaje = request.POST.get('array')
    registros =  []
    
    for i in mensaje:
        ref=detallerec.objects.get(registro = i[0])
        if ref.fechasalidafruta == None:
            ref.fechasalidafruta = ref.fecha
        
        detallerecaux.objects.create(recepcion=i[1],fecha=str(ref.fecha),finca=i[3],cultivo=i[4],cajas=i[5],libras=i[6],status="En proceso",observaciones=i[8],llave=str(ref.llave),criterio=str(ref.criterio),classorigen=str(ref.classorigen),fechasalidafruta=str(ref.fechasalidafruta))
    
        # Crea un diccionario con los datos
    '''
    registro = {
        'recepcion': i[1],
        'fecha': str(ref.fecha),
        'finca': i[3],
        'cultivo': i[4],
        'cajas': i[5],
        'libras': i[6],
        'status': "En proceso",
        'observaciones': i[8],
        'llave': str(ref.llave),
        'criterio': str(ref.criterio),
        'classorigen': str(ref.classorigen),
        'fechasalidafruta': str(ref.fechasalidafruta),
    }
    
    # Añade el diccionario a la lista de registros
    registros.append(registro)
    '''
    
    for i in mensaje:
        salidas = detallerec.objects.get(recepcion=i[1])
        
        salidas2= detallerecaux.objects.all().filter(recepcion=i[1]).aggregate(sumalibras=Sum('libras'))['sumalibras']
        
        if str(salidas2) == str(salidas.libras):
            salidas.status = "En proceso"
            salidas.save()
    
    return JsonResponse({'mensaje':mensaje,'registros':registros})   

def recepciones_list(request):

    today = timezone.localtime(timezone.now()).date()
    current_month = today.month
    current_year = today.year
    #salidas = Recepciones.objects.filter(fecha=today)
    salidas= detallerec.objects.filter(fecha__year=current_year,fecha__month=current_month).order_by('-recepcion').exclude(status="Anulado")
    
    #for i in salidas:
    #    cajasacum = salidas2.order_by('-created').filter(Q(status="En proceso") | Q(status="Cerrado"),recepcion=i.recepcion).aggregate(sumacajas=Sum('cajas'))['sumacajas']
    #    librasacum = salidas2.order_by('-created').filter(Q(status="En proceso") | Q(status="Cerrado"),recepcion=i.recepcion).aggregate(sumalibras=Sum('libras'))['sumalibras']    
    #    if librasacum != None and cajasacum != None:
    #        i.cajas = i.cajas - int(cajasacum)
    #        i.libras = i.libras - float(librasacum)
        

    #existenciaCajas = finca=list(salidas)[0]['cajas']
    #existenciaLibras = finca=list(salidas)[0]['libras']
    #rebajaCajas = finca=list(salidas2)[0]['cajas']
    #rebajaLibras = finca=list(salidas2)[0]['libras']
    #for i in len(salidas):
    #    existenciaCajas 
    #paginator = Paginator(salidas, 10)  # 10 registros por página (ajusta según prefieras)
    #page_number = request.GET.get('page')  # Obtener el número de página de la URL
    #page_obj = paginator.get_page(page_number)

    return render(request, 'plantaE/recepciones_list.html', {'registros': salidas})

def recepcionesFruta_delete(request, pk):
    salidas = get_object_or_404(detallerec, pk=pk)

    # Verificar si existen registros en detallerecaux con la misma recepción
    existe_en_aux = detallerecaux.objects.filter(recepcion=salidas.recepcion).exists()

    if existe_en_aux:
        return render(request, 'plantaE/recepciones_confirm_delete.html', {
            'registros': salidas,
            'alert_message': "No se puede anular esta recepción porque tiene registros relacionados en boletas.",
            'redirect_url': reverse('recepcionesFruta_list')
        })

    if request.method == 'POST':
        # Anular detallerec
        salidas.status = 'Anulado'
        salidas.save()

        # Anular Actpeso y Recepciones
        Actpeso.objects.filter(recepcion=salidas.recepcion).exclude(status='Anulado').update(status='Anulado')
        Recepciones.objects.filter(recepcion=salidas.recepcion).exclude(status='Anulado').update(status='Anulado')

        # Limpiar campos en AcumFruta y salidasFruta
        AcumFruta.objects.filter(recepcion=salidas.recepcion).exclude(status='Anulado').update(
            libras=None,
            recepcion=None,
            viaje=None,
            nsalidafruta=None
        )
        salidasFruta.objects.filter(recepcion=salidas.recepcion).exclude(status='Anulado').update(
            libras=None,
            recepcion=None,
            status=None
        )

        return render(request, 'plantaE/recepciones_confirm_delete.html', {
            'registros': salidas,
            'alert_message': "Registro anulado correctamente.",
            'redirect_url': reverse('recepcionesFruta_list')
        })

    return render(request, 'plantaE/recepciones_confirm_delete.html', {'registros': salidas})

def envioslocal_list(request):

    today = timezone.localtime(timezone.now()).date()
    current_month = today.month
    current_year = today.year
    #salidas = Recepciones.objects.filter(fecha=today)
    salidas= enviosrec.objects.filter(fecha__year=current_year,fecha__month=current_month).order_by('-envio').exclude(status="Anulado")

    return render(request, 'plantaE/envioslocal_list.html', {'registros': salidas})

def envioslocal_detail(request, pk):
    salidas = get_object_or_404(enviosrec, pk=pk)
    return render(request, 'plantaE/envioslocal_detail.html', {'registros': salidas})

def envioslocal_delete(request, pk):

    envio_original = get_object_or_404(enviosrec, pk=pk)

    # Obtener todos los registros con el mismo "envio" (o 'registro')
    registros_a_anular = enviosrec.objects.filter(envio=envio_original.envio)

    # Registros de inventario relacionados
    inventarios_relacionados = inventarioProdTerm.objects.filter(
        enviorec=envio_original.envio
    ).exclude(status='Anulado')

    # Validar si alguno de esos registros ya tiene boleta asignada
    boletas_asignadas = inventarios_relacionados.filter(
        boleta__isnull=False
    ).exclude(boleta=0).exists()

    if boletas_asignadas:
        return render(request, 'plantaE/envioslocal_confirm_delete.html', {
            'registros': envio_original,
            'alert_message': "No se puede anular este envío porque uno o más registros tienen boletas asignadas.",
            'redirect_url': reverse('envioslocal_list')
        })

    if request.method == 'POST':
        # Anular todos los registros de envío relacionados
        registros_a_anular.update(status='Anulado')

        # Anular registros de inventario
        inventarios_relacionados.update(status='Anulado', status3='Anulado')

        return render(request, 'plantaE/envioslocal_confirm_delete.html', {
            'registros': envio_original,
            'alert_message': "El envío y todos los registros relacionados fueron anulados correctamente.",
            'redirect_url': reverse('envioslocal_list')
        })

    # Mostrar la confirmación inicial
    return render(request, 'plantaE/envioslocal_confirm_delete.html', {
        'registros': envio_original
    })

def recepciones_reporteAcum(request):
    today = timezone.now().date()

     # Obtener todos los registros para el usuario y la fecha
    registros = Recepciones.objects.filter(fecha=today)

   # Crear un DataFrame a partir de los registros, incluyendo todas las columnas
    df = pd.DataFrame(list(registros.values()),columns=['fecha','finca','cultivo','variedad','cajas','libras'])

    # Agrupar por 'variedad' y sumar las 'cajas'
    df_agrupado = df.groupby(['variedad','cultivo','finca'], as_index=False).agg(
        total_cajas=('cajas', 'sum'),
        cultivo=('cultivo', 'first'),  # Conservar el primer correo asociado
        fecha=('fecha', 'first'),
        variedad=('variedad', 'first'),
        finca=('finca', 'first'),
        total_libras=('libras', 'sum')    # Conservar la primera fecha asociada
    )

    # Convertir el DataFrame a una lista de diccionarios para pasarlo a la plantilla
    registros_finales = df_agrupado.to_dict(orient='records')

    # Agrupar por 'cultivo' y sumar las 'cajas'
    df_agrupado = df.groupby(['cultivo','finca'], as_index=False).agg(
        total_cajas=('cajas', 'sum'),
        cultivo=('cultivo', 'first'),  # Conservar el primer correo asociado
        fecha=('fecha', 'first'),
        variedad=('variedad', 'first'),
        finca=('finca', 'first'),
        total_libras=('libras', 'sum')    # Conservar la primera fecha asociada
    )

    registros_finales2 = df_agrupado.to_dict(orient='records')

    if request.method == 'POST':
        opcion2 = request.POST.get('opcion2')
         # Obtener todos los registros para el usuario y la fecha
        registros = Recepciones.objects.filter(fecha=opcion2)

    # Crear un DataFrame a partir de los registros, incluyendo todas las columnas
        df = pd.DataFrame(list(registros.values()),columns=['fecha','finca','cultivo','variedad','cajas','libras'])

        # Agrupar por 'variedad' y sumar las 'cajas'
        df_agrupado = df.groupby(['variedad','cultivo','finca'], as_index=False).agg(
            total_cajas=('cajas', 'sum'),
            cultivo=('cultivo', 'first'),  # Conservar el primer correo asociado
            fecha=('fecha', 'first'),
            variedad=('variedad', 'first'),
            finca=('finca', 'first'),
            total_libras=('libras', 'sum')    # Conservar la primera fecha asociada
        )

        # Convertir el DataFrame a una lista de diccionarios para pasarlo a la plantilla
        registros_finales = df_agrupado.to_dict(orient='records')

        # Agrupar por 'cultivo' y sumar las 'cajas'
        df_agrupado = df.groupby(['cultivo','finca'], as_index=False).agg(
            total_cajas=('cajas', 'sum'),
            cultivo=('cultivo', 'first'),  # Conservar el primer correo asociado
            fecha=('fecha', 'first'),
            variedad=('variedad', 'first'),
            finca=('finca', 'first'),
            total_libras=('libras', 'sum')    # Conservar la primera fecha asociada
        )

        registros_finales2 = df_agrupado.to_dict(orient='records')
        return JsonResponse({'datos': list(registros_finales),'opcion2':opcion2,'resumen':registros_finales2}, safe=False)

    return render(request, 'plantaE/recepciones_reporteAcum.html', {'registros': registros_finales, 'registros2': registros_finales2})

def recepciones_reporteAcumKgm2Orden(request):

    today = timezone.now().date()
    current_week = today.isocalendar()[1]  # Obtener el número de semana actual
    current_year = today.isocalendar()[0]  # Obtener el año actual

    # Obtener todos los registros
    registros = AcumFruta.objects.all()

    # Crear un DataFrame a partir de los registros
    df = pd.DataFrame(list(registros.values()), columns=['fecha', 'finca', 'orden','cultivo', 'libras'])
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    # Agregar columnas para el número de semana y el año
    df['semana'] = df['fecha'].dt.isocalendar().week
    df['año'] = df['fecha'].dt.isocalendar().year

    # Filtrar por la semana y el año actuales
    df_filtrado = df[(df['semana'] == current_week) & (df['año'] == current_year)]
    
    # Agrupar por 'variedad' y sumar las 'cajas'

    df_agrupado = df_filtrado.groupby(['orden', 'cultivo', 'finca'], as_index=False).agg(
        cultivo=('cultivo', 'first'),
        semana=('semana', 'first'),
        finca=('finca', 'first'),
        orden=('orden', 'first'),
        total_libras=('libras', 'sum')
    )
    df_agrupado['Kg'] = df_agrupado['total_libras']*0.453592
    areas = datosProduccion.objects.all()

    df_areas = pd.DataFrame(list(areas.values()), columns=['orden', 'area'])  # 'orden' y 'area'

    # Realizamos un merge para agregar las áreas correspondientes a cada 'orden'
    df_final = df_agrupado.merge(df_areas, on='orden', how='inner')
    df_final['kxm2'] = df_final['Kg']/df_final['area']
    # Convertir el DataFrame a una lista de diccionarios para pasarlo a la plantilla
    registros_finales = df_final.to_dict(orient='records')

    if request.method == 'POST':
        opcion2 = request.POST.get('opcion2')  # Esto es algo como "Semana 51 del 2024"
        opcion2 = opcion2.strip()  # Eliminar espacios adicionales o caracteres extraños
        # Obtener todos los registros para el usuario y la fecha
        registros = AcumFruta.objects.all()

        # Crear un DataFrame a partir de los registros
        df = pd.DataFrame(list(registros.values()), columns=['fecha', 'finca', 'orden', 'cultivo', 'libras'])
        df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')  # Convierte la fecha a datetime
        
        # Agregar columnas para el número de semana y el año
        df['semana'] = df['fecha'].dt.isocalendar().week  # Semana ISO
        df['año'] = df['fecha'].dt.isocalendar().year  # Año ISO
        df['semana-año'] = 'Semana ' + df['semana'].astype(str) + ' del ' + df['año'].astype(str)  # Texto para visualizar
        
        
        # Filtramos por las columnas 'semana-año'
        df_filtrado = df[df['semana-año'] == str(opcion2)]

        # Agrupar por 'orden', 'cultivo' y 'finca', sumando las libras
        df_agrupado = df_filtrado.groupby(['orden', 'cultivo', 'finca'], as_index=False).agg(
            cultivo=('cultivo', 'first'),
            semana=('semana', 'first'),
            finca=('finca', 'first'),
            orden=('orden', 'first'),
            total_libras=('libras', 'sum')
        )
        
        # Convertir las libras a kilogramos
        df_agrupado['Kg'] = df_agrupado['total_libras'] * 0.453592

        # Obtener las áreas
        areas = datosProduccion.objects.all()
        df_areas = pd.DataFrame(list(areas.values()), columns=['orden', 'area'])

        # Realizar un merge para agregar las áreas correspondientes a cada 'orden'
        df_final = df_agrupado.merge(df_areas, on='orden', how='inner')

        # Calcular kxm2 (kg por metro cuadrado)
        df_final['kxm2'] = df_final['Kg'] / df_final['area']

        # Convertir el DataFrame a una lista de diccionarios para pasarlo a la plantilla
        registros_finales = df_final.to_dict(orient='records')

        # Devolver los datos en formato JSON
        return JsonResponse({'datos': list(registros_finales), 'opcion2': opcion2}, safe=False)

    return render(request, 'plantaE/recepciones_reporteAcumKgm2Orden.html', {'registros': registros_finales})

def recepciones_reporteAcumKgm2Estruc(request):

    today = timezone.now().date()
    current_week = today.isocalendar()[1]  # Obtener el número de semana actual
    current_year = today.isocalendar()[0]  # Obtener el año actual

    # Obtener todos los registros
    registros = AcumFruta.objects.all()

    # Crear un DataFrame a partir de los registros
    df = pd.DataFrame(list(registros.values()), columns=['fecha', 'finca', 'orden','cultivo','estructura', 'libras'])
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    # Agregar columnas para el número de semana y el año
    df['semana'] = df['fecha'].dt.isocalendar().week
    df['año'] = df['fecha'].dt.isocalendar().year

    # Filtrar por la semana y el año actuales
    df_filtrado = df[(df['semana'] == current_week) & (df['año'] == current_year)]
    
    # Agrupar por 'variedad' y sumar las 'cajas'

    df_agrupado = df_filtrado.groupby(['orden', 'cultivo', 'finca','estructura'], as_index=False).agg(
        cultivo=('cultivo', 'first'),
        semana=('semana', 'first'),
        finca=('finca', 'first'),
        orden=('orden', 'first'),
        estructura=('estructura', 'first'),
        total_libras=('libras', 'sum')
    )
    df_agrupado['Kg'] = df_agrupado['total_libras']*0.453592
    areas = datosProduccion.objects.all()

    df_areas = pd.DataFrame(list(areas.values()), columns=['orden', 'area'])  # 'orden' y 'area'

    # Realizamos un merge para agregar las áreas correspondientes a cada 'orden'
    df_final = df_agrupado.merge(df_areas, on='orden', how='inner')
    df_final['kxm2'] = df_final['Kg']/df_final['area']
    # Convertir el DataFrame a una lista de diccionarios para pasarlo a la plantilla
    registros_finales = df_final.to_dict(orient='records')

    if request.method == 'POST':
        opcion2 = request.POST.get('opcion2')  # Esto es algo como "Semana 51 del 2024"
        opcion2 = opcion2.strip()  # Eliminar espacios adicionales o caracteres extraños
        # Obtener todos los registros para el usuario y la fecha
        registros = AcumFruta.objects.all()

        # Crear un DataFrame a partir de los registros
        df = pd.DataFrame(list(registros.values()), columns=['fecha', 'finca', 'orden', 'cultivo','estructura', 'libras'])
        df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')  # Convierte la fecha a datetime
        
        # Agregar columnas para el número de semana y el año
        df['semana'] = df['fecha'].dt.isocalendar().week  # Semana ISO
        df['año'] = df['fecha'].dt.isocalendar().year  # Año ISO
        df['semana-año'] = 'Semana ' + df['semana'].astype(str) + ' del ' + df['año'].astype(str)  # Texto para visualizar
        
        
        # Filtramos por las columnas 'semana-año'
        df_filtrado = df[df['semana-año'] == str(opcion2)]

        # Agrupar por 'orden', 'cultivo' y 'finca', sumando las libras
        df_agrupado = df_filtrado.groupby(['orden', 'cultivo', 'finca','estructura'], as_index=False).agg(
            cultivo=('cultivo', 'first'),
            semana=('semana', 'first'),
            finca=('finca', 'first'),
            orden=('orden', 'first'),
            estructura=('estructura', 'first'),
            total_libras=('libras', 'sum')
        )
        
        # Convertir las libras a kilogramos
        df_agrupado['Kg'] = df_agrupado['total_libras'] * 0.453592

        # Obtener las áreas
        areas = datosProduccion.objects.all()
        df_areas = pd.DataFrame(list(areas.values()), columns=['orden', 'area'])

        # Realizar un merge para agregar las áreas correspondientes a cada 'orden'
        df_final = df_agrupado.merge(df_areas, on='orden', how='inner')

        # Calcular kxm2 (kg por metro cuadrado)
        df_final['kxm2'] = df_final['Kg'] / df_final['area']

        # Convertir el DataFrame a una lista de diccionarios para pasarlo a la plantilla
        registros_finales = df_final.to_dict(orient='records')

        # Devolver los datos en formato JSON
        return JsonResponse({'datos': list(registros_finales), 'opcion2': opcion2}, safe=False)

    return render(request, 'plantaE/recepciones_reporteAcumKgm2Estruc.html', {'registros': registros_finales})

def recepciones_reporteAcumKgm2Variedad(request):

    today = timezone.now().date()
    current_week = today.isocalendar()[1]  # Obtener el número de semana actual
    current_year = today.isocalendar()[0]  # Obtener el año actual

    # Obtener todos los registros
    registros = AcumFruta.objects.all()

    # Crear un DataFrame a partir de los registros
    df = pd.DataFrame(list(registros.values()), columns=['fecha', 'finca', 'orden','cultivo','estructura','variedad', 'libras'])
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    # Agregar columnas para el número de semana y el año
    df['semana'] = df['fecha'].dt.isocalendar().week
    df['año'] = df['fecha'].dt.isocalendar().year

    # Filtrar por la semana y el año actuales
    df_filtrado = df[(df['semana'] == current_week) & (df['año'] == current_year)]
    
    # Agrupar por 'variedad' y sumar las 'cajas'

    df_agrupado = df_filtrado.groupby(['orden', 'cultivo', 'finca','variedad'], as_index=False).agg(
        cultivo=('cultivo', 'first'),
        semana=('semana', 'first'),
        finca=('finca', 'first'),
        orden=('orden', 'first'),
        variedad=('variedad', 'first'),
        total_libras=('libras', 'sum')
    )
    df_agrupado['Kg'] = df_agrupado['total_libras']*0.453592
    areas = datosProduccion.objects.all()

    df_areas = pd.DataFrame(list(areas.values()), columns=['orden', 'area'])  # 'orden' y 'area'

    # Realizamos un merge para agregar las áreas correspondientes a cada 'orden'
    df_final = df_agrupado.merge(df_areas, on='orden', how='inner')
    df_final['kxm2'] = df_final['Kg']/df_final['area']
    # Convertir el DataFrame a una lista de diccionarios para pasarlo a la plantilla
    registros_finales = df_final.to_dict(orient='records')

    if request.method == 'POST':
        opcion2 = request.POST.get('opcion2')  # Esto es algo como "Semana 51 del 2024"
        opcion2 = opcion2.strip()  # Eliminar espacios adicionales o caracteres extraños
        # Obtener todos los registros para el usuario y la fecha
        registros = AcumFruta.objects.all()

        # Crear un DataFrame a partir de los registros
        df = pd.DataFrame(list(registros.values()), columns=['fecha', 'finca', 'orden', 'cultivo','estructura','variedad', 'libras'])
        df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')  # Convierte la fecha a datetime
        
        # Agregar columnas para el número de semana y el año
        df['semana'] = df['fecha'].dt.isocalendar().week  # Semana ISO
        df['año'] = df['fecha'].dt.isocalendar().year  # Año ISO
        df['semana-año'] = 'Semana ' + df['semana'].astype(str) + ' del ' + df['año'].astype(str)  # Texto para visualizar
        
        
        # Filtramos por las columnas 'semana-año'
        df_filtrado = df[df['semana-año'] == str(opcion2)]

        # Agrupar por 'orden', 'cultivo' y 'finca', sumando las libras
        df_agrupado = df_filtrado.groupby(['orden', 'cultivo', 'finca','variedad'], as_index=False).agg(
            cultivo=('cultivo', 'first'),
            semana=('semana', 'first'),
            finca=('finca', 'first'),
            orden=('orden', 'first'),
            variedad=('variedad', 'first'),
            total_libras=('libras', 'sum')
        )
        
        # Convertir las libras a kilogramos
        df_agrupado['Kg'] = df_agrupado['total_libras'] * 0.453592

        # Obtener las áreas
        areas = datosProduccion.objects.all()
        df_areas = pd.DataFrame(list(areas.values()), columns=['orden', 'area'])

        # Realizar un merge para agregar las áreas correspondientes a cada 'orden'
        df_final = df_agrupado.merge(df_areas, on='orden', how='inner')

        # Calcular kxm2 (kg por metro cuadrado)
        df_final['kxm2'] = df_final['Kg'] / df_final['area']

        # Convertir el DataFrame a una lista de diccionarios para pasarlo a la plantilla
        registros_finales = df_final.to_dict(orient='records')

        # Devolver los datos en formato JSON
        return JsonResponse({'datos': list(registros_finales), 'opcion2': opcion2}, safe=False)

    return render(request, 'plantaE/recepciones_reporteAcumKgm2Variedad.html', {'registros': registros_finales})

def recepciones_reporteAcumSem(request):

    today = timezone.now().date()
    current_week = today.isocalendar()[1]  # Obtener el número de semana actual
    current_year = today.isocalendar()[0]  # Obtener el año actual

    # Obtener todos los registros
    registros = Recepciones.objects.all()

    # Crear un DataFrame a partir de los registros
    df = pd.DataFrame(list(registros.values()), columns=['fecha', 'finca', 'cultivo', 'variedad', 'cajas', 'libras'])
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    # Agregar columnas para el número de semana y el año
    df['semana'] = df['fecha'].dt.isocalendar().week
    df['año'] = df['fecha'].dt.isocalendar().year

    # Filtrar por la semana y el año actuales
    df_filtrado = df[(df['semana'] == current_week) & (df['año'] == current_year)]

    # Agrupar por 'variedad' y sumar las 'cajas'
    df_agrupado = df_filtrado.groupby(['variedad', 'cultivo', 'finca'], as_index=False).agg(
        total_cajas=('cajas', 'sum'),
        cultivo=('cultivo', 'first'),
        semana=('semana', 'first'),
        variedad=('variedad', 'first'),
        finca=('finca', 'first'),
        total_libras=('libras', 'sum')
    )

    # Convertir el DataFrame a una lista de diccionarios para pasarlo a la plantilla
    registros_finales = df_agrupado.to_dict(orient='records')

    # Agrupar por 'cultivo' y sumar las 'cajas'
    df_agrupado2 = df_filtrado.groupby(['cultivo', 'finca'], as_index=False).agg(
        total_cajas=('cajas', 'sum'),
        cultivo=('cultivo', 'first'),
        semana=('semana', 'first'),
        variedad=('variedad', 'first'),
        finca=('finca', 'first'),
        total_libras=('libras', 'sum')
    )

    registros_finales2 = df_agrupado2.to_dict(orient='records')

    return render(request, 'plantaE/recepciones_reporteAcumSem.html', {
        'registros': registros_finales,
        'registros2': registros_finales2
    })

def recepciones_reporteAcumSemPublic(request):
    today = timezone.now().date()
    current_week = today.isocalendar()[1]  # Obtener el número de semana actual
    current_year = today.isocalendar()[0]  # Obtener el año actual
    nombre_usuario = request.user.username
    # Obtener el objeto de usuario basado en el correo. Usamos .get() si esperamos un solo resultado

    try:
        finca_usuario = usuariosAppFruta.objects.get(correo=nombre_usuario)
        
    except usuariosAppFruta.DoesNotExist:
        # En caso de que no exista el usuario con ese correo, maneja el error apropiadamente.
        # Puedes lanzar una excepción o retornar un mensaje de error.
        finca_usuario = None

    # Verifica si se encontró el usuario
    if finca_usuario:
        # Obtener los registros de 'Recepciones' para la finca asociada al usuario
        registros = Recepciones.objects.filter(finca=finca_usuario.finca)

    # Crear un DataFrame a partir de los registros
    df = pd.DataFrame(list(registros.values()), columns=['fecha', 'finca', 'cultivo', 'variedad', 'cajas', 'libras'])
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    # Agregar columnas para el número de semana y el año
    df['semana'] = df['fecha'].dt.isocalendar().week
    df['año'] = df['fecha'].dt.isocalendar().year

    # Filtrar por la semana y el año actuales
    df_filtrado = df[(df['semana'] == current_week) & (df['año'] == current_year)]

    # Agrupar por 'variedad' y sumar las 'cajas'
    df_agrupado = df_filtrado.groupby(['variedad', 'cultivo', 'finca'], as_index=False).agg(
        total_cajas=('cajas', 'sum'),
        cultivo=('cultivo', 'first'),
        semana=('semana', 'first'),
        variedad=('variedad', 'first'),
        finca=('finca', 'first'),
        total_libras=('libras', 'sum')
    )

    # Convertir el DataFrame a una lista de diccionarios para pasarlo a la plantilla
    registros_finales = df_agrupado.to_dict(orient='records')

    # Agrupar por 'cultivo' y sumar las 'cajas'
    df_agrupado2 = df_filtrado.groupby(['cultivo', 'finca'], as_index=False).agg(
        total_cajas=('cajas', 'sum'),
        cultivo=('cultivo', 'first'),
        semana=('semana', 'first'),
        variedad=('variedad', 'first'),
        finca=('finca', 'first'),
        total_libras=('libras', 'sum')
    )

    registros_finales2 = df_agrupado2.to_dict(orient='records')

    return render(request, 'plantaE/recepciones_reporteAcumSemPublic.html', {
        'registros': registros_finales,
        'registros2': registros_finales2
    })

def recepciones_reportecurva(request):
    nombre_usuario = request.user.username
    #mensaje = request.POST.get('array')
    
    return render(request, 'plantaE/recepciones_reportegrafica.html', {'usuario': nombre_usuario})

def recepciones_reportecurva2(request):
    nombre_usuario = request.user.username
    #mensaje = request.POST.get('array')
    
    return render(request, 'plantaE/recepciones_reportegraficaPublic.html', {'usuario': nombre_usuario})

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


def boletas_list(request):
    #today = timezone.now().date()
    #salidas = Recepciones.objects.filter(fecha=today)
    salidas= Boletas.objects.all()
    salidas = salidas.order_by('-boleta')
     
    return render(request, 'plantaE/boletas_list.html', {'registros': salidas})

def boletas_update(request, pk):
    salidas = get_object_or_404(Boletas, pk=pk)
    if request.method == 'POST':
        form = boletasForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('boletasFruta_list')
        else:
            return JsonResponse({'errores': form.errors}, status=400)
    else:
        form = boletasForm(instance=salidas)
    return render(request, 'plantaE/boletas_form.html', {'form': form})

def boletas_detail(request, pk):
    salidas = get_object_or_404(Boletas, pk=pk)
    return render(request, 'plantaE/boletas_detail.html', {'registros': salidas})

def boletas_delete(request, pk):

    salidas = get_object_or_404(Boletas, pk=pk)
    boletas_relacionadas = Boletas.objects.filter(boleta=salidas.boleta)

    if request.method == 'POST':
        # Anular boletas relacionadas
        boletas_relacionadas.update(status='Anulado')

        # Actualizar inventario relacionado
        invrelacionado = inventarioProdTerm.objects.exclude(status='Anulado').filter(boleta=salidas.boleta)
        invrelacionado.update(status3=None)

        # Obtener recepciones relacionadas
        recepciones_ids = detallerecaux.objects.exclude(status='Anulado') \
                                               .filter(boleta=salidas.boleta) \
                                               .values_list('recepcion', flat=True).distinct()

        for recepcion_id in recepciones_ids:
            recepcion_aux = detallerecaux.objects.exclude(status='Anulado').filter(recepcion=recepcion_id)
            recepcion_aux.update(status='En proceso')

            recepcion_detalle = detallerec.objects.exclude(status='Anulado').filter(recepcion=recepcion_id)
            recepcion_detalle.update(status=None)

        # Anular detalles auxiliares
        detalleaux_anular = detallerecaux.objects.exclude(status='Anulado').filter(boleta=salidas.boleta)
        detalleaux_anular.update(status='Anulado')

        # Procesar AcumFruta relacionados
        acumfruta_ids = AcumFrutaaux.objects.exclude(status='Anulado') \
                                            .filter(boleta=salidas.boleta) \
                                            .values_list('acumfrutaid', flat=True).distinct()

        for acumfruta_id in acumfruta_ids:
            acumfruta_aux = AcumFrutaaux.objects.exclude(status='Anulado').filter(acumfrutaid=acumfruta_id)
            acumfruta_aux.update(status=None)

            acumfruta_detalle = AcumFruta.objects.exclude(status='Anulado').filter(id=acumfruta_id)
            acumfruta_detalle.update(status=None)

        # Anular acumfruta auxiliar
        acumfruta_anular = AcumFrutaaux.objects.exclude(status='Anulado').filter(boleta=salidas.boleta)
        acumfruta_anular.update(status='Anulado')

        messages.success(request, "Registro anulado correctamente.")
        return redirect('boletasFruta_list')

    return render(request, 'plantaE/boletas_confirm_delete.html', {'registros': salidas})

def recepciones_detail(request, pk):
    salidas = get_object_or_404(detallerec, pk=pk)

    return render(request, 'plantaE/recepciones_detail.html', {'registros': salidas})

def recepciones_update(request, pk):
    salidas = get_object_or_404(detallerec, pk=pk)
    if request.method == 'POST':
        form = recepcionesForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('recepcionesFruta_list')
        else:
            return JsonResponse({'errores': form.errors}, status=400)
    else:
        form = recepcionesForm(instance=salidas)
    return render(request, 'plantaE/recepciones_form.html', {'form': form})

def ccalidad_list(request):
    today = timezone.localtime(timezone.now()).date()
    current_month = today.month
    current_year = today.year
    salidas = Ccalidad.objects.filter(fecha__year=current_year,fecha__month=current_month).order_by('-registro').exclude(status="Anulado")
    

    return render(request, 'plantaE/ccalidad_list.html', {'registros': salidas})

def ccalidad_detail(request, pk):
    salidas = get_object_or_404(Ccalidad, pk=pk)
    return render(request, 'plantaE/ccalidad_detail.html', {'registros': salidas})

def ccalidad_create(request):
    if request.method == 'POST':
        form = ccalidadForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                # Manejar excepciones específicas (por ejemplo, UniqueConstraintError)
                return JsonResponse({'error': str(e)}, status=400)
            return redirect('ccalidad_list')
        else:
             # Imprimir errores para depuración
            return JsonResponse({'errores': form.errors}, status=400)
    else:
        form = ccalidadForm()
    return render(request, 'plantaE/ccalidad_form.html', {'form': form,'modo':'crear'})

def ccalidad_update(request, pk):
    salidas = get_object_or_404(Ccalidad, pk=pk)
    if request.method == 'POST':
        form = ccalidadForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('ccalidad_list')
    else:
        form = ccalidadForm(instance=salidas)
        
    return render(request, 'plantaE/ccalidad_form_edit.html', {'form': form,'modo':'actualizar'})

def ccalidad_update_aux(request):
    pk = request.GET.get('pk')
    salidas = get_object_or_404(Ccalidad, pk=pk)
    causa_rechazo = causasRechazo.objects.all().values('causa')
    return JsonResponse({'llave': salidas.llave,'recepcion':salidas.recepcion,'causa_select':salidas.causarechazo,'causas':list(causa_rechazo)})
    
def ccalidad_delete(request, pk):
    salidas = get_object_or_404(Ccalidad, pk=pk)

    if request.method == 'POST':
        salidas.status = 'Anulado'
        salidas.save()
        
        messages.success(request, "Registro anulado correctamente.")
    return render(request, 'plantaE/ccalidad_confirm_delete.html', {'registros': salidas})

def obtener_llave_recepcion(request):
    # Obtén los criterios únicos filtrando por 'recepcion' mayor o igual a 2875
    llave_recepcion = detallerec.objects.filter(recepcion__gte=2875).values('criterio').distinct()
    llave_recepcion2 = detallerec.objects.filter(recepcion__gte=2875).values('recepcion').distinct()

    # Crea un diccionario para almacenar las sumas de porcentaje por llave en Ccalidad
    suma_por_llave = Ccalidad.objects.values('llave').annotate(suma=Sum('porcentaje'))

    # Convierte el resultado a un diccionario para facilitar el acceso
    suma_dict = {item['llave']: item['suma'] for item in suma_por_llave}

    # Obtener los registros de detallerec filtrando por 'recepcion' y calculando la semana de 'fechasalidafruta'
    datos = detallerec.objects.filter(recepcion__gte=2875)

    # Lista para almacenar las concatenaciones de la semana, finca/llave y cultivo
    datos_modificados = []

    for item in datos:
        # Extraer el número de semana de la fecha 'fechasalidafruta'
        fecha = item.fechasalidafruta
        if fecha:
            semana = fecha.isocalendar()[1]  # Usamos isocalendar() para obtener el número de semana
        else:
            semana = None

        # Realizar la concatenación condicional de 'finca' o 'llave' y 'cultivo'
        if item.finca == "Productor":
            clave = f"{semana} | {item.llave} | {item.cultivo}"
        else:
            clave = f"{semana} | {item.finca} | {item.cultivo}"

        # Agregar la clave concatenada a la lista de datos modificados
        datos_modificados.append(clave)

    # Eliminar duplicados en la lista de concatenaciones
    datos_modificados = list(set(datos_modificados))

    # Filtrar los datos_modificados para mantener solo aquellos con suma de porcentaje menor a 1
    datos_modificados = [
        clave for clave in datos_modificados
        if suma_dict.get(clave, 0) < 1  # Solo mantener claves cuyo porcentaje es menor que 1
    ]

    # Obtener las causas de rechazo
    causa_rechazo = causasRechazo.objects.all().values('causa')

    # Obtener la fecha actual en formato 'YYYY-MM-DD'
    now = datetime.datetime.now()
    fecha = now.date()
    dia = fecha.day
    mes = fecha.month
    año = fecha.year

    # Asegurarse de que el día y el mes tengan 2 dígitos
    if mes < 10:
        mes = "0" + str(mes)
    if dia < 10:
        dia = "0" + str(dia)
    
    # Formatear la fecha
    fecha_ = f"{año}-{mes}-{dia}"

    # Devolver los datos en formato JSON
    return JsonResponse({
        'llaves': "",
        'causa': list(causa_rechazo),
        'fecha': fecha_,
        'llave': list(llave_recepcion2),
        'datos_filtrados': datos_modificados  # Aquí se agregan las claves filtradas
    })

def load_ccalidadparam(request):
    llave_recepcion = request.GET.get('category_id')
    datos = detallerec.objects.filter(criterio=llave_recepcion).values('recepcion').distinct('recepcion')
    valor = Ccalidad.objects.filter(llave=llave_recepcion).aggregate(suma=Sum('porcentaje'))['suma']
    if valor != None:
        valor = 1-float(Ccalidad.objects.filter(llave=llave_recepcion).aggregate(suma=Sum('porcentaje'))['suma'])
        
    else:
        valor=1
    
    return JsonResponse({'datos': list(datos),'valor':valor})

def inventarioProd_list(request):
    today = timezone.localtime(timezone.now()).date()
    #salidas = Recepciones.objects.filter(fecha=today)
    salidas = inventarioProdTerm.objects.filter(fecha=today,categoria="Exportación").exclude(status='Anulado')
    return render(request, 'plantaE/inventarioProd_list.html', {'registros': salidas})

def inventarioProd_detail(request, pk):
    salidas = get_object_or_404(inventarioProdTerm, pk=pk)
    return render(request, 'plantaE/inventarioProd_detail.html', {'registros': salidas})


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

def validaroventa(request):
    # Recibe los datos desde el body de la solicitud
    data = json.loads(request.body)
    contenedores_array = data.get('array')  # Contenedores recibidos en el array

    # Filtra los contenedores que no tienen el status "Cerrado" y que están en el array de contenedores
    contenedores_a_cerrar = salidacontenedores.objects.filter(
        contenedor=contenedores_array
    ).exclude(Q(status='Cerrado') | Q(status='Anulado'))

    if contenedores_a_cerrar.exists():
        # Actualiza el status a "Cerrado" para los contenedores encontrados
        contenedores_a_cerrar.update(status='Cerrado')
        return JsonResponse({'msm': "Listo, se cerro el contenedor"}, safe=False)
    else:
    # Si no se encontraron contenedores
        return JsonResponse({'msm': "No se encontraron contenedores para cerrar"}, safe=False)

def generate_packing_list_pdf(request):
    # Obtén el parámetro 'contenedor' de la URL (GET)
    contenedor = request.GET.get('contenedor')
    if not contenedor:
        return JsonResponse({'error': 'Contenedor no especificado'}, status=400)
    
    hoy = timezone.now().date()
    semana_actual = hoy.isocalendar()[1]  # Semana actual

    # Obtiene el primer contenedor que coincida con los datos
    infoconten = contenedores.objects.exclude(status="Anulado").exclude(status="Cerrado").order_by("registro").filter(contenedor=contenedor).first()
    if not infoconten:
        return JsonResponse({'error': 'Contenedor no encontrado'}, status=404)

    # Filtra los contenedores que no tienen el status "Cerrado" y que están en el array de contenedores
    contenedores_a_imprimir = salidacontenedores.objects.filter(contenedor=contenedor).exclude(status='Anulado').order_by("registro").values('proveedor','itemsapcode','itemsapname','contenedor','fechasalcontenedor','fecha','cajas','importe','cultivo','palet')
    if not contenedores_a_imprimir:
        return JsonResponse({'error': 'No hay contenedor con status pendiente'}, status=404)
    # Convierte el QuerySet a un DataFrame de pandas
    df = pd.DataFrame(list(contenedores_a_imprimir))
    df['fechasalcontenedor'] = pd.to_datetime(df['fechasalcontenedor'], errors='coerce')
    df['semana_contenedor'] = df['fechasalcontenedor'].dt.isocalendar().week
    df['semana_actual'] = semana_actual

    # Filtra el DataFrame para que solo contenga los registros de la semana actual
    df_filtrado = df[df['semana_contenedor'] == semana_actual]

    if not df_filtrado.empty:
        # Agrupar por 'itemsapcode', 'palet', 'proveedor' y calcular la suma de las cajas
        df_agrupado = df_filtrado.groupby(['itemsapcode', 'palet', 'proveedor','fecha'], as_index=False).agg(
            fecha=('fecha', 'first'),
            palet=('palet', 'first'),
            itemsapname=('itemsapname', 'first'),
            proveedor=('proveedor', 'first'),
            total_cajas=('cajas', 'sum')
        )
        # Ordena el DataFrame por la columna 'palet'
        df_agrupado = df_agrupado.sort_values(by='palet')

        # Prepara el contexto para la plantilla
        context = {
            'planta': 'SDC',
            'destino': infoconten.destino,
            'contenedor': infoconten.contenedor,
            'fecha': infoconten.fecha,
            'viaje': infoconten.viaje,
            'marchamo': infoconten.marchamo,
            'placacamion': infoconten.placacamion,
            'temperatura': infoconten.temperatura,
            'ventilacion': infoconten.ventilacion,
            'hora': infoconten.horasalida,
            'piloto': infoconten.piloto,
            'transportista': infoconten.transportista,
            'datos': df_agrupado.to_dict(orient='records')
        }
        semana_contenedor = infoconten.fecha.isocalendar()[1]
         # Si la semana del contenedor es la misma que la semana actual
        if semana_contenedor == semana_actual:
            infoconten.status = "Cerrado"
            infoconten.save()
        # Renderiza la plantilla HTML con los datos
        return render(request, 'plantaE/packinglist_template.html', context)
   
    else:
        # Si no hay datos, devuelve una respuesta vacía o de error
        return JsonResponse({'error': 'No hay datos disponibles para esta semana'}, status=400)
       
def inventarioProd_create(request):
    if request.method == 'POST':
        opcion1 = request.POST.get('opcion1')
        opcion2 = request.POST.get('opcion2')
        # Filtra tus datos según la opción seleccionada
        datos = productoTerm.objects.filter(cultivo=opcion1,categoria=opcion2).values('itemsapcode','itemsapname')  # Ajusta los campos
        return JsonResponse({'datos': list(datos),'opcion1':opcion1,'opcion2':opcion2}, safe=False)
    return render(request, 'plantaE/inventarioProd_formPlantilla.html')
'''
def inventarioProd_create(request):
    if request.method == 'POST':
        form = inventarioFrutaForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                # Manejar excepciones específicas (por ejemplo, UniqueConstraintError)
                return JsonResponse({'error': str(e)}, status=400)
            return redirect('inventarioProd_list')
        else:
             # Imprimir errores para depuración
            return JsonResponse({'errores': form.errors}, status=400)
    else:
        form = inventarioFrutaForm()
    return render(request, 'plantaE/inventarioProd_form.html', {'form': form})
'''

def inventarioProd_delete(request, pk):
    salidas = get_object_or_404(inventarioProdTerm, pk=pk)
    salidasaux = inventarioProdTermAux.objects.filter(inventarioreg=salidas.registro)

    # Si tiene movimientos asociados, no se puede anular
    if salidasaux.exists():
        return render(request, 'plantaE/inventarioProd_confirm_delete.html', {
            'registros': salidas,
            'alert_message': "No se puede anular el registro porque tiene movimientos asociados.",
            'redirect_url': reverse('inventarioProd_list')
        })

    if request.method == 'POST':
        salidas.status = 'Anulado'
        salidas.status3 = 'Anulado'
        salidas.save()

        return render(request, 'plantaE/inventarioProd_confirm_delete.html', {
            'registros': salidas,
            'alert_message': "Registro anulado correctamente.",
            'redirect_url': reverse('inventarioProd_list')
        })

    return render(request, 'plantaE/inventarioProd_confirm_delete.html', {'registros': salidas})

def inventarioProd_update(request, pk):
    salidas = get_object_or_404(inventarioProdTerm, pk=pk)
    if request.method == 'POST':
        form = inventarioFrutaForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('inventarioProd_list')
    else:
        form = inventarioFrutaForm(instance=salidas)
        
    return render(request, 'plantaE/inventarioProd_form_edit.html', {'form': form})

def load_inventarioProdparam(request):
    cultivo_ = request.GET.get('campo1')
    categoria_ = request.GET.get('campo2')

    if cultivo_ != None and categoria_ != None:
        datos = productoTerm.objects.filter(cultivo=cultivo_,categoria=categoria_).values('itemsapcode','itemsapname')
    
    return JsonResponse({'datos': list(datos),'cultivo':cultivo_,'categoria':categoria_})

def plantaEhomepage(request):
    return render(request,'plantaE/plantaE_home.html')

def reporteInventario(request):
    opcion1 = timezone.now().date()

    # Filtra tus datos según la opción seleccionada
    datos_empaque = inventarioProdTerm.objects.filter(fecha=opcion1,categoria="Exportación").exclude(status='Anulado').values(
        "fecha", "proveedor", "cultivo", "itemsapcode", "itemsapname", "categoria", "cajas", "lbsintara", "merma"
    )

    # Crea un DataFrame a partir de los datos
    df = pd.DataFrame(list(datos_empaque))
    registros_finales = []

    if not df.empty:
        # Agrupa los datos
        df_agrupado = df.groupby(['proveedor', 'itemsapcode','categoria'], as_index=False).agg(
            fecha=('fecha', 'first'),
            proveedor=('proveedor', 'first'),
            cultivo=('cultivo', 'first'),
            itemsapcode=('itemsapcode', 'first'),
            itemsapname=('itemsapname', 'first'),
            total_tarimas=('itemsapcode', 'count'),
            categoria=('categoria', 'first'),
            total_cajas=('cajas', 'sum'),
            total_libras=('lbsintara', 'sum'),
            total_merma=('merma', 'sum'),
        )
        
        df_agrupado["porcen_merma"] = df_agrupado["total_merma"]*100/df_agrupado["total_libras"]
        df_agrupado["pesoxcajaprom"] = df_agrupado["total_libras"]/df_agrupado["total_cajas"]
        
        registros_finales = df_agrupado.to_dict(orient='records')

    # Al hacer la solicitud GET (cuando se carga la página inicialmente), se envían datos para el día actual
    context = {'datos': registros_finales, 'opcion1': opcion1}

    if request.method == 'POST':
        opcion1 = request.POST.get('opcion2')

        # Filtra los datos nuevamente
        datos_empaque = inventarioProdTerm.objects.filter(fecha=opcion1,categoria="Exportación").exclude(status = 'Anulado').values(
            "fecha", "proveedor", "cultivo", "itemsapcode", "itemsapname", "categoria", "cajas", "lbsintara", "merma"
        )

        # Crea el DataFrame y agrupa
        df = pd.DataFrame(list(datos_empaque))
        if not df.empty:
            df_agrupado = df.groupby(['proveedor', 'itemsapcode','categoria'], as_index=False).agg(
                fecha=('fecha', 'first'),
                proveedor=('proveedor', 'first'),
                cultivo=('cultivo', 'first'),
                itemsapcode=('itemsapcode', 'first'),
                itemsapname=('itemsapname', 'first'),
                total_tarimas=('itemsapcode', 'count'),
                categoria=('categoria', 'first'),
                total_cajas=('cajas', 'sum'),
                total_libras=('lbsintara', 'sum'),
                total_merma=('merma', 'sum'),
            )
            df_agrupado["porcen_merma"] = df_agrupado["total_merma"]*100/df_agrupado["total_libras"]
            df_agrupado["pesoxcajaprom"] = df_agrupado["total_libras"]/df_agrupado["total_cajas"]
            registros_finales = df_agrupado.to_dict(orient='records')
            return JsonResponse({'datos': registros_finales, 'opcion1': opcion1}, safe=False)

    return render(request, 'plantaE/inventarioProd_reporteInv.html', context)

def contenedorpacking_list(request):
    opcion1 = timezone.now().date()

    # Filtra tus datos según la opción seleccionada
    contenedores = salidacontenedores.objects.exclude(Q(status='Cerrado') | Q(status='Anulado'))
    contenedores = contenedores.order_by("registro").values('proveedor', 'itemsapcode', 'itemsapname', 'contenedor','fechasalcontenedor', 'cajas', 'importe', 'cultivo')
    # Crea un DataFrame a partir de los datos
    df = pd.DataFrame(list(contenedores))
    registros_finales = []

    if not df.empty:
        # Agrupa los datos
        df_agrupado = df.groupby(['itemsapcode','contenedor','fechasalcontenedor'], as_index=False).agg(
            fecha=('fechasalcontenedor', 'first'),
            cultivo=('cultivo', 'first'),
            contenedor=('contenedor', 'first'),
            itemsapcode=('itemsapcode', 'first'),
            itemsapname=('itemsapname', 'first'),
            total_cajas=('cajas', 'sum'),
            total_importe=('importe', 'sum')
        )
        
        
        registros_finales = df_agrupado.to_dict(orient='records')

    # Al hacer la solicitud GET (cuando se carga la página inicialmente), se envían datos para el día actual
    context = {'datos': registros_finales, 'opcion1': opcion1}

    if request.method == 'POST':

        opcion1 = request.POST.get('opcion1')

        # Filtra los datos nuevamente
        contenedor = salidacontenedores.objects.filter(contenedor=opcion1).exclude(Q(status='Cerrado') | Q(status='Anulado')).order_by("registro").values('proveedor','itemsapcode','itemsapname','contenedor','fechasalcontenedor','cajas','importe','cultivo')


        # Crea el DataFrame y agrupa
        df = pd.DataFrame(list(contenedor))
        if not df.empty:
            df_agrupado = df.groupby([ 'itemsapcode','fechasalcontenedor','contenedor'], as_index=False).agg(
                fecha=('fechasalcontenedor', 'first'),
                cultivo=('cultivo', 'first'),
                itemsapcode=('itemsapcode', 'first'),
                itemsapname=('itemsapname', 'first'),
                total_cajas=('cajas', 'sum'),
                total_importe=('importe', 'sum')
            )
            registros_finales = df_agrupado.to_dict(orient='records')
            return JsonResponse({'datos': registros_finales, 'opcion1': opcion1}, safe=False)
        else:
        # Si el DataFrame está vacío después de agrupar, retorna un mensaje indicando que no hay datos
            return JsonResponse({'mensaje': 'No se encontraron datos para el contenedor seleccionado'})

    return render(request, 'plantaE/inventarioProd_packinglist.html', context)

def contenedorpacking_list_detail(request):

    # Filtra tus datos según la opción seleccionada
    contenedores = salidacontenedores.objects.order_by("-registro").exclude(Q(status='Cerrado') | Q(status='Anulado'))

    return render(request, 'plantaE/inventarioProd_packinglist_detail.html', {'data':contenedores})

def packinglist_update(request, pk):
    salidas = get_object_or_404(salidacontenedores, pk=pk)
    if request.method == 'POST':
        form = salidacontenedoresForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('inventarioProd_packinglist_detail')
    else:
        form = salidacontenedoresForm(instance=salidas)
    return render(request, 'plantaE/inventarioProd_packinglist_form.html', {'form': form})


def packinglist_delete(request, pk):
    
    salidas = get_object_or_404(salidacontenedores, pk=pk)

   # Buscar registros auxiliares vinculados al contenedor
    relacionados = inventarioProdTermAux.objects.filter(salidacontenedores=salidas.registro)

    # Buscar en inventarioProdTerm los registros asociados
    relacionados2 = inventarioProdTerm.objects.filter(
        registro__in=relacionados.values_list('inventarioreg', flat=True)
    )

    # Verificar si alguno tiene boleta asignada
    tiene_boletas = relacionados2.filter(boleta__isnull=False).exclude(boleta=0).exists()

    if tiene_boletas:
        return render(request, 'plantaE/inventarioProd_packinglist_confirm_delete.html', {
            'registros': salidas,
            'alert_message': "No se puede anular esta paleta porque tiene boletas asignadas.",
            'redirect_url': reverse('inventarioProd_packinglist_detail')
        })

    if request.method == 'POST':
        # Paso 1: Anular el contenedor
        salidas.status = 'Anulado'
        salidas.save()

        # Paso 2: Anular los registros auxiliares
        relacionados.update(status='Anulado')

        # Paso 3: Obtener los inventarioreg únicos
        inventario_codigos = relacionados.values_list('inventarioreg', flat=True).distinct()

        # Paso 4: Actualizar inventario principal
        inventarioProdTerm.objects.filter(registro__in=inventario_codigos).exclude(status='Anulado').update(status=None)

        return render(request, 'plantaE/inventarioProd_packinglist_confirm_delete.html', {
            'registros': salidas,
            'alert_message': "Paleta anulada correctamente.",
            'redirect_url': reverse('inventarioProd_packinglist_detail')
        })

    return render(request, 'plantaE/inventarioProd_packinglist_confirm_delete.html', {
        'registros': salidas
    })

def packinglist_delete(request, pk):
    salidas = get_object_or_404(salidacontenedores, pk=pk)

    # Buscar registros auxiliares vinculados al contenedor
    relacionados = inventarioProdTermAux.objects.filter(salidacontenedores=salidas.registro)

    # Verificar si alguno tiene boleta asignada (no permitir anular)
    if relacionados.filter(boleta__isnull=False).exists():
        messages.error(request, "No se puede anular esta paleta porque tiene boletas asignadas.")
        return redirect('inventarioProd_packinglist_detail')

    if request.method == 'POST':
        # Paso 1: Anular el contenedor
        salidas.status = 'Anulado'
        salidas.save()

        # Paso 2: Anular los registros en inventarioProdTermAux
        relacionados.update(status='Anulado')

        # Paso 3: Obtener todos los códigos únicos de inventarioreg
        inventario_codigos = relacionados.values_list('inventarioreg', flat=True).distinct()

        # Paso 4: Actualizar los registros en inventarioProdTerm a status=None
        inventarioProdTerm.objects.filter(registro__in=inventario_codigos).update(status=None)

        messages.success(request, "Registro anulado correctamente.")
        return redirect('inventarioProd_packinglist_detail')

    return render(request, 'plantaE/inventarioProd_packinglist_confirm_delete.html', {'registros': salidas})

def procesarinvprodconten(request):

    data = json.loads(request.body)
    mensaje = data['array']
    contenedor_=data['contenedor']
    today = timezone.now().date()
    semana_actual = today.isocalendar()[1]  # semana actual
    #mensaje = request.POST.get('array')
        
    registros =  []
    
    for i in mensaje:
        ref=inventarioProdTerm.objects.get(registro = i[0])
        ref2=productoTerm.objects.get(itemsapcode = i[4])
        precio = float(ref2.precio) if ref2.precio is not None else 0.0
        lbsintara = float(ref.lbsintara) if ref.lbsintara is not None else 0.0

        importe=float(precio)*float(i[6])
        salidacontenedores.objects.create(fecha=str(ref.fecha),palet=i[12],importe=importe,fechasalcontenedor=today,key=ref.registro,contenedor=contenedor_,categoria=str(ref.categoria),cultivo=ref.cultivo,proveedor=ref.proveedor,itemsapcode = ref.itemsapcode,itemsapname = ref.itemsapname,orden=ref.orden,cajas=float(i[6]),lbsintara=(float(i[6])*lbsintara/ref.cajas),pesostdxcaja=ref.pesostdxcaja,pesostd=(float(i[6])*ref.pesostd/ref.cajas),merma=(float(i[6])*ref.merma/ref.cajas),pesorxcaja=ref.pesorxcaja,pesosinmerma=ref.pesosinmerma,calidad1=ref.calidad1)
        # Crea un diccionario con los datos
    
    for i in mensaje:

        salidas = inventarioProdTerm.objects.get(registro=i[0])
        
        salidas2= salidacontenedores.objects.all().filter(key=i[0]).aggregate(sumacajas=Sum('cajas'))['sumacajas']
        
        if str(salidas2) == str(salidas.cajas):
            salidas.status = "En proceso"
            salidas.save()
    
    return JsonResponse({'mensaje':mensaje,'registros':registros})   


def reporte_tabla_pivote(request):
    filtros_get = {
        'finca': request.GET.get('finca'),
        'orden': request.GET.get('orden'),
        'estructura': request.GET.get('estructura'),
        'variedad': request.GET.get('variedad'),
        'cultivo': request.GET.get('cultivo'),
    }

    qs = AcumFruta.objects.exclude(finca="CIP").exclude(libras__isnull=True)

    for campo, valor in filtros_get.items():
        if valor:
            qs = qs.filter(**{campo: valor})

    data = qs.values('fecha', 'finca', 'orden', 'estructura').annotate(
        total_libras=Sum('libras')
    )

    if data:
        df = pd.DataFrame(data)
        df['fecha'] = pd.to_datetime(df['fecha'])
        df['semana'] = df['fecha'].dt.strftime('%Y-W%V')
        df['kg'] = df['total_libras'] / 2.20462  # convertir a kilogramos

        # Crear tabla pivote: kilos por semana
        pivot = pd.pivot_table(
            df,
            values='kg',
            index=['finca', 'orden', 'estructura'],
            columns='semana',
            aggfunc='sum',
            fill_value=0
        ).round(2)

        # Obtener áreas por finca-orden-estructura
        areas_qs = detallesEstructuras.objects.values('finca', 'orden', 'estructura').annotate(
            area_total=Sum('area')
        )
        df_areas = pd.DataFrame(list(areas_qs))

        # Unir pivot con áreas
        pivot = pivot.reset_index()
        df_merge = pd.merge(pivot, df_areas, on=['finca', 'orden', 'estructura'], how='left')

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
        ('Finca', 'finca', AcumFruta.objects.exclude(finca__isnull=True).exclude(finca='').values_list('finca', flat=True).distinct()),
        ('Orden', 'orden', AcumFruta.objects.exclude(orden__isnull=True).exclude(orden='').values_list('orden', flat=True).distinct()),
        ('Variedad', 'variedad', AcumFruta.objects.exclude(variedad__isnull=True).exclude(variedad='').values_list('variedad', flat=True).distinct()),
        ('Cultivo', 'cultivo', AcumFruta.objects.exclude(cultivo__isnull=True).exclude(cultivo='').values_list('cultivo', flat=True).distinct()),
        ('Estructura', 'estructura', AcumFruta.objects.exclude(estructura__isnull=True).exclude(estructura='').values_list('estructura', flat=True).distinct()),
    ]

    return render(request, 'plantaE/reporte_tabla_pivote.html', {
        'tabla_html': tabla_html,
        'filtros_completos': filtros_completos,
        'request': request
    })

def reporte_tabla_pivote2(request):

    filtros_get = {
        'finca': request.GET.get('finca'),
        'orden': request.GET.get('orden'),
        'estructura': request.GET.get('estructura'),
        'variedad': request.GET.get('variedad'),
        'cultivo': request.GET.get('cultivo'),
    }

    nombre_usuario = request.user.username

    qs = AcumFruta.objects.filter(correo=nombre_usuario).exclude(finca="CIP").exclude(libras__isnull=True)

    for campo, valor in filtros_get.items():
        if valor:
            qs = qs.filter(**{campo: valor})

    data = qs.values('fecha', 'finca', 'orden', 'estructura').annotate(
        total_libras=Sum('libras')
    )

    if data:
        df = pd.DataFrame(data)
        df['fecha'] = pd.to_datetime(df['fecha'])
        df['semana'] = df['fecha'].dt.strftime('%Y-W%V')
        df['kg'] = df['total_libras'] / 2.20462  # convertir a kilogramos

        # Crear tabla pivote: kilos por semana
        pivot = pd.pivot_table(
            df,
            values='kg',
            index=['finca', 'orden', 'estructura'],
            columns='semana',
            aggfunc='sum',
            fill_value=0
        ).round(2)

        # Obtener áreas por finca-orden-estructura
        areas_qs = detallesEstructuras.objects.values('finca', 'orden', 'estructura').annotate(
            area_total=Sum('area')
        )
        df_areas = pd.DataFrame(list(areas_qs))

        # Unir pivot con áreas
        pivot = pivot.reset_index()
        df_merge = pd.merge(pivot, df_areas, on=['finca', 'orden', 'estructura'], how='left')

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
        ('Finca', 'finca', AcumFruta.objects.filter(correo=nombre_usuario).exclude(finca__isnull=True).exclude(finca='').values_list('finca', flat=True).distinct()),
        ('Orden', 'orden', AcumFruta.objects.filter(correo=nombre_usuario).exclude(orden__isnull=True).exclude(orden='').values_list('orden', flat=True).distinct()),
        ('Variedad', 'variedad', AcumFruta.objects.filter(correo=nombre_usuario).exclude(variedad__isnull=True).exclude(variedad='').values_list('variedad', flat=True).distinct()),
        ('Cultivo', 'cultivo', AcumFruta.objects.filter(correo=nombre_usuario).exclude(cultivo__isnull=True).exclude(cultivo='').values_list('cultivo', flat=True).distinct()),
        ('Estructura', 'estructura', AcumFruta.objects.filter(correo=nombre_usuario).exclude(estructura__isnull=True).exclude(estructura='').values_list('estructura', flat=True).distinct()),
    ]

    return render(request, 'plantaE/reporte_tabla_pivote2.html', {
        'tabla_html': tabla_html,
        'filtros_completos': filtros_completos,
        'request': request
    })

def procesarinvprodcontenv2(request):
    data = json.loads(request.body)
    mensaje = data['array']
    contenedor_ = data['contenedor']
    today = timezone.now().date()

    # Obtener siguiente palet disponible
    consulta = salidacontenedores.objects.exclude(Q(status='Cerrado') | Q(status='Anulado')).filter(contenedor=contenedor_).order_by('-registro').first()
    palet = 1 if consulta is None else (consulta.palet or 0) + 1

    registros = []

    for i in mensaje:
        proveedor = i[0]
        cultivo = i[1]
        itemsapcode = i[2]
        itemsapname = i[3]
        cajas_a_enviar = int(i[4])
        fecha_salida = i[9]

        producto = productoTerm.objects.filter(itemsapcode=itemsapcode).first()
        precio = float(producto.precio) if producto and producto.precio else 0.0

        disponibles = inventarioProdTerm.objects.filter(
            proveedor=proveedor,
            itemsapcode=itemsapcode,
            categoria="Exportación",
            status__isnull=True
        ).exclude(status='Anulado').order_by('fecha', 'registro')

        usados = inventarioProdTermAux.objects.filter(
            proveedor=proveedor,
            itemsapcode=itemsapcode,
            categoria="Exportación",
            status__isnull=True
        ).exclude(status='Anulado').values('inventarioreg').annotate(
            cajas_usadas=Sum('cajas'),
            lbs_usadas=Sum('lbsintara')
        )
        usados_map = {r['inventarioreg']: {'cajas': r['cajas_usadas'], 'lbs': r['lbs_usadas']} for r in usados}
        # Formatear disponibles en una lista de diccionarios
        disponibles_data = [{
            'registro': r.registro,
            'fecha': r.fecha,
            'cajas': r.cajas,
            'lbsintara': r.lbsintara,
            'orden': r.orden,
            'categoria': r.categoria,
            'status': r.status
        } for r in disponibles]

        # Convertir los usados directamente desde la query
        usados_data = list(usados)
        cajas_acumuladas = 0

        for registro in disponibles:
            orden = registro.orden
            total_cajas = registro.cajas or 0
            total_libras = registro.lbsintara or 0

            usadas = usados_map.get(registro.registro, {'cajas': 0, 'lbs': 0})
            cajas_disponibles = total_cajas - (usadas['cajas'] or 0)
            libras_disponibles = total_libras - (usadas['lbs'] or 0)

            if cajas_disponibles <= 0 or libras_disponibles <= 0:
                continue  # nada que usar, siguiente registro

            faltan_cajas = cajas_a_enviar - cajas_acumuladas
            cajas_usadas = min(cajas_disponibles, faltan_cajas)
            if cajas_usadas <= 0:
                continue

            proporcion = cajas_usadas / cajas_disponibles
            libras_a_usar = libras_disponibles * proporcion

            importe = precio * cajas_usadas
            pesostd = (cajas_usadas * registro.pesostd / total_cajas) if registro.pesostd else 0
            merma = max(libras_a_usar - pesostd, 0)
            pesorxcaja = libras_a_usar / cajas_usadas if cajas_usadas else 0
            pesosinmerma = libras_a_usar - merma

            # Crear en salidacontenedores
            salidacontenedores.objects.create(
                fecha=fecha_salida,
                palet=palet,
                importe=importe,
                fechasalcontenedor=today,
                contenedor=contenedor_,
                categoria=registro.categoria,
                cultivo=cultivo,
                proveedor=proveedor,
                itemsapcode=itemsapcode,
                itemsapname=itemsapname,
                orden=orden,
                cajas=cajas_usadas,
                lbsintara=libras_a_usar,
                pesostdxcaja=registro.pesostdxcaja,
                pesostd=pesostd,
                merma=merma,
                pesorxcaja=pesorxcaja,
                pesosinmerma=pesosinmerma,
                calidad1=registro.calidad1
            )
            conexion = salidacontenedores.objects.last()

            # Crear en inventarioProdTermAux
            inventarioProdTermAux.objects.create(
                fecha=registro.fecha,
                inventarioreg=registro.registro,
                categoria=registro.categoria,
                cultivo=cultivo,
                proveedor=proveedor,
                itemsapcode=itemsapcode,
                itemsapname=itemsapname,
                calidad1=registro.calidad1,
                cajas=cajas_usadas,
                lbsintara=libras_a_usar,
                pesostdxcaja=registro.pesostdxcaja,
                pesostd=pesostd,
                merma=merma,
                pesorxcaja=pesorxcaja,
                pesosinmerma=pesosinmerma,
                orden=registro.orden,
                salidacontenedores=str(conexion.registro)
            )

            # Verificar si se agotó todo el stock del registro
            aux_sum = inventarioProdTermAux.objects.filter(inventarioreg=registro.registro).aggregate(
                sumacajas=Sum('cajas'),
                sumalbs=Sum('lbsintara')
            )
            if (aux_sum['sumacajas'] or 0) >= total_cajas and (aux_sum['sumalbs'] or 0) >= total_libras:
                registro.status = 'En proceso'
                registro.save()
                inventarioProdTermAux.objects.filter(orden=orden).update(status='En proceso')

            # Solo aquí se suma una vez
            cajas_acumuladas += cajas_usadas

            if cajas_acumuladas >= cajas_a_enviar:
                break

    return JsonResponse({
        'mensaje': 'Procesado correctamente',
        'palet': palet,
        'total_registros_procesados': len(mensaje),
        'disponibles':disponibles_data,
        'usados' : usados_data
    })

def cargacontenedores_listv2(request):

    today = timezone.now().date()

    # Obtener todas las salidas de inventario y salidas de contenedores
    salidas = inventarioProdTerm.objects.filter(
        fecha__lte=today,
        categoria="Exportación"
    ).filter(
        Q(status='') | Q(status__isnull=True)
    ).order_by('registro')
    salidas2 = inventarioProdTermAux.objects.filter(
        fecha__lte=today,
        categoria="Exportación").exclude(Q(status='En proceso') | Q(status='Anulado'))

    # Filtrar las salidas de inventario para las que tienen categoría 'Exportación' y sin 'status'

    # Excluir los registros de salidas2 donde el contenedor esté vacío
    #salidas2 = salidas2.filter(registro__gte=2799)

    # Crear un diccionario para almacenar los resultados agrupados por 'itemsapcode' y 'proveedor'
    agrupaciones = {}

    # Agrupar las salidas de inventario (salidas) por 'itemsapcode' y 'proveedor'
    for salida in salidas:
        # Crear la clave de agrupación concatenando 'itemsapcode' y 'proveedor'
        clave_agrupacion = (salida.itemsapcode, salida.proveedor)

        if clave_agrupacion not in agrupaciones:
            agrupaciones[clave_agrupacion] = {
                'itemsapcode': salida.itemsapcode,
                'itemsapname': salida.itemsapname,
                'proveedor': salida.proveedor,
                'cultivo': salida.cultivo,
                'total_cajas_salidas': 0,  # Cajas de salidas
                'total_cajas_salidas2': 0,  # Cajas de salidas2
                'total_libras_salidas': 0,  # Cajas de salidas
                'total_libras_salidas2': 0,  # Cajas de salidas2
                'salidas': []
            }

        # Acumular las cajas de las salidas
        agrupaciones[clave_agrupacion]['total_cajas_salidas'] += salida.cajas
        agrupaciones[clave_agrupacion]['salidas'].append(salida)
        agrupaciones[clave_agrupacion]['total_libras_salidas'] += salida.lbsintara

    # Agrupar las salidas de contenedores (salidas2) por 'itemsapcode' y 'proveedor'
    for salida2 in salidas2:
        # Verificar si el contenedor no está vacío antes de acumular las cajas
        #if salida2.contenedor is not None:
            # Crear la clave de agrupación concatenando 'itemsapcode' y 'proveedor'
        clave_agrupacion = (salida2.itemsapcode, salida2.proveedor)

        if clave_agrupacion in agrupaciones:
            # Acumular las cajas de las salidas2
            agrupaciones[clave_agrupacion]['total_cajas_salidas2'] += salida2.cajas
            
            agrupaciones[clave_agrupacion]['total_libras_salidas2'] += salida2.lbsintara

    # Ahora, restamos las cajas de 'salidas2' de las de 'salidas' para cada agrupación
    for agrupacion in agrupaciones.values():
        # Restar las cajas de las salidas2 de las de las salidas
        agrupacion['cajas_restantes'] = agrupacion['total_cajas_salidas'] - agrupacion['total_cajas_salidas2']
        agrupacion['libras_restantes'] = agrupacion['total_libras_salidas'] - agrupacion['total_libras_salidas2']
    
    # Filtrar las agrupaciones donde las cajas restantes son mayores que 0
    registros_agrupados = [
        agrupacion for agrupacion in agrupaciones.values() if agrupacion['cajas_restantes'] > 0
    ]

    # Ordenar la lista de registros por el campo 'proveedor'
    registros_agrupados = sorted(registros_agrupados, key=lambda x: x['proveedor'])
    registros_json = json.dumps(registros_agrupados, default=str)  # Usar default=str para evitar errores con objetos no serializables

    return render(request, 'plantaE/inventarioProd_ccontenedor.html', {'registros': registros_agrupados, 'registros_json':registros_json})

def cargacontenedores_list(request):
    today = timezone.now().date()
    
    # Obtener todos los registros de inventario y salidas
    salidas = inventarioProdTerm.objects.all()
    salidas2 = salidacontenedores.objects.all()
    
    # Filtrar salidas de exportación y con status=None
    salidas = salidas.order_by('registro').filter(status=None, categoria="Exportación")
    
    for i in salidas:
        # Obtener la cantidad total de cajas asociadas a la salida
        cajasacum = salidas2.order_by('-created_at').filter(key=i.registro).aggregate(sumacajas=Sum('cajas'))['sumacajas']
        
        # Si hay cajas acumuladas, restarlas de las cajas de inventario
        if cajasacum is not None:
            i.cajas = i.cajas - int(cajasacum)
            
            # Cambiar el status si las cajas quedan en 0
            if i.cajas == 0:
                i.status = 'Cerrado'
    
    # Filtrar las salidas para que solo contengan aquellas con cajas > 0
    salidas = [i for i in salidas if i.cajas > 0]

    # Retornar las salidas que cumplen con la condición (cajas > 0)
    return render(request, 'plantaE/inventarioProd_contenedores.html', {'registros': salidas})

def inventariogeneral_list(request):
    today = timezone.now().date()

    # Obtener todas las salidas de inventario y salidas de contenedores
    salidas = inventarioProdTerm.objects.filter(
        fecha__lte=today,
        categoria="Exportación"
    ).filter(
        Q(status='') | Q(status__isnull=True)
    ).order_by('registro')
    salidas2 = inventarioProdTermAux.objects.filter(
        fecha__lte=today,
        categoria="Exportación").exclude(Q(status='En proceso') | Q(status='Anulado'))

    # Filtrar las salidas de inventario para las que tienen categoría 'Exportación' y sin 'status'

    # Excluir los registros de salidas2 donde el contenedor esté vacío
    #salidas2 = salidas2.filter(registro__gte=2799)

    # Crear un diccionario para almacenar los resultados agrupados por 'itemsapcode' y 'proveedor'
    agrupaciones = {}

    # Agrupar las salidas de inventario (salidas) por 'itemsapcode' y 'proveedor'
    for salida in salidas:
        # Crear la clave de agrupación concatenando 'itemsapcode' y 'proveedor'
        clave_agrupacion = (salida.itemsapcode, salida.proveedor)

        if clave_agrupacion not in agrupaciones:
            agrupaciones[clave_agrupacion] = {
                'itemsapcode': salida.itemsapcode,
                'itemsapname': salida.itemsapname,
                'proveedor': salida.proveedor,
                'cultivo': salida.cultivo,
                'total_cajas_salidas': 0,  # Cajas de salidas
                'total_cajas_salidas2': 0,  # Cajas de salidas2
                'salidas': []
            }

        # Acumular las cajas de las salidas
        agrupaciones[clave_agrupacion]['total_cajas_salidas'] += salida.cajas
        agrupaciones[clave_agrupacion]['salidas'].append(salida)

    # Agrupar las salidas de contenedores (salidas2) por 'itemsapcode' y 'proveedor'
    for salida2 in salidas2:
        # Verificar si el contenedor no está vacío antes de acumular las cajas

        # Crear la clave de agrupación concatenando 'itemsapcode' y 'proveedor'
        clave_agrupacion = (salida2.itemsapcode, salida2.proveedor)

        if clave_agrupacion in agrupaciones:
            # Acumular las cajas de las salidas2
            agrupaciones[clave_agrupacion]['total_cajas_salidas2'] += salida2.cajas

    # Ahora, restamos las cajas de 'salidas2' de las de 'salidas' para cada agrupación
    for agrupacion in agrupaciones.values():
        # Restar las cajas de las salidas2 de las de las salidas
        agrupacion['cajas_restantes'] = agrupacion['total_cajas_salidas'] - agrupacion['total_cajas_salidas2']
    
    # Filtrar las agrupaciones donde las cajas restantes son mayores que 0
    registros_agrupados = [
        agrupacion for agrupacion in agrupaciones.values() if agrupacion['cajas_restantes'] > 0
    ]

    # Ordenar la lista de registros por el campo 'proveedor'
    registros_agrupados = sorted(registros_agrupados, key=lambda x: x['proveedor'])
    registros_json = json.dumps(registros_agrupados, default=str)  # Usar default=str para evitar errores con objetos no serializables

    # Pasar los registros agrupados al renderizado de la plantilla
    return render(request, 'plantaE/inventarioProd_inventariogeneral.html', {'registros': registros_agrupados,'registros_json':registros_json})


def dashboard_acumfruta(request):

    # Filtros desde GET
    filtros_get = {
        'finca': request.GET.get('finca'),
        'orden': request.GET.get('orden'),
        'variedad': request.GET.get('variedad'),
        'cultivo': request.GET.get('cultivo'),
        'estructura': request.GET.get('estructura'),
    }
    
    # Query base
    qs = AcumFruta.objects.exclude(finca="CIP").exclude(libras__isnull=True)

    # Aplicar filtros
    for campo, valor in filtros_get.items():
        if valor:
            qs = qs.filter(**{campo: valor})

    # Agrupación por fecha
    datos = qs.values('fecha').annotate(libras_totales=Sum('libras')).order_by('fecha')
    fechas = [d['fecha'].strftime('%Y-%m-%d') for d in datos]
    libras = [d['libras_totales'] for d in datos]
    derivadas = [0] + [libras[i] - libras[i - 1] for i in range(1, len(libras))]

    # Filtros disponibles
    filtros_completos = [
        ('Finca', 'finca', AcumFruta.objects.exclude(finca__isnull=True).exclude(finca='').values_list('finca', flat=True).distinct()),
        ('Orden', 'orden', AcumFruta.objects.exclude(orden__isnull=True).exclude(orden='').values_list('orden', flat=True).distinct()),
        ('Variedad', 'variedad', AcumFruta.objects.exclude(variedad__isnull=True).exclude(variedad='').values_list('variedad', flat=True).distinct()),
        ('Cultivo', 'cultivo', AcumFruta.objects.exclude(cultivo__isnull=True).exclude(cultivo='').values_list('cultivo', flat=True).distinct()),
        ('Estructura', 'estructura', AcumFruta.objects.exclude(estructura__isnull=True).exclude(estructura='').values_list('estructura', flat=True).distinct()),
    ]

    context = {
        'filtros_completos': filtros_completos,
        'fechas_json': json.dumps(fechas),
        'libras_json': json.dumps(libras),
        'derivadas_json': json.dumps(derivadas),
        'request': request,
    }

    return render(request, 'plantaE/dashboard_acumfruta.html', context)

def get_date_from_week(anio, semana):
    first_day = datetime.datetime(anio, 1, 4)  # El 4 de enero siempre está en la semana 1
    start_of_week = first_day - datetime.timedelta(days=first_day.weekday())
    return (start_of_week + datetime.timedelta(weeks=semana - 1)).date()

def dashboard_tecnicos(request):
    # Filtros desde GET
    filtros_get = {
        'finca': request.GET.get('finca'),
        'orden': request.GET.get('orden'),
        'variedad': request.GET.get('variedad'),
        'cultivo': request.GET.get('cultivo'),
        'estructura': request.GET.get('estructura'),
    }
    nombre_usuario = request.user.username
    # Query base
    qs = AcumFruta.objects.filter(correo=nombre_usuario).exclude(finca="CIP").exclude(libras__isnull=True)

    # Aplicar filtros
    for campo, valor in filtros_get.items():
        if valor:
            qs = qs.filter(**{campo: valor})

    # Agrupación por semana
    datos = qs.annotate(
        semana=ExtractWeek('fecha'),
        anio=ExtractYear('fecha')
    ).values('anio', 'semana').annotate(
        libras_totales=Sum('libras')
    ).order_by('anio', 'semana')

    # Ejes para la gráfica
    fechas = [get_date_from_week(d['anio'], d['semana']).isoformat() for d in datos]
    kilos = [round(d['libras_totales'] / 2.20462, 2) for d in datos]
    derivadas = [0] + [kilos[i] - kilos[i - 1] for i in range(1, len(kilos))]


    # Filtros disponibles
    filtros_completos = [
        ('Finca', 'finca', AcumFruta.objects.filter(correo=nombre_usuario).exclude(finca__isnull=True).exclude(finca='').values_list('finca', flat=True).distinct()),
        ('Orden', 'orden', AcumFruta.objects.filter(correo=nombre_usuario).exclude(orden__isnull=True).exclude(orden='').values_list('orden', flat=True).distinct()),
        ('Variedad', 'variedad', AcumFruta.objects.filter(correo=nombre_usuario).exclude(variedad__isnull=True).exclude(variedad='').values_list('variedad', flat=True).distinct()),
        ('Cultivo', 'cultivo', AcumFruta.objects.filter(correo=nombre_usuario).exclude(cultivo__isnull=True).exclude(cultivo='').values_list('cultivo', flat=True).distinct()),
        ('Estructura', 'estructura', AcumFruta.objects.filter(correo=nombre_usuario).exclude(estructura__isnull=True).exclude(estructura='').values_list('estructura', flat=True).distinct()),
    ]

    context = {
        'filtros_completos': filtros_completos,
        'fechas_json': json.dumps(fechas),
        'libras_json': json.dumps(kilos),
        'derivadas_json': json.dumps(derivadas),
        'request': request,
    }

    return render(request, 'plantaE/dashboard_acumfruta2.html', context)

def get_ordenes_por_finca(request):
    finca = request.POST.get('finca')
    if finca:
        ordenes = AcumFruta.objects.filter(finca=finca)\
            .exclude(orden__isnull=True)\
            .exclude(orden='')\
            .values_list('orden', flat=True)\
            .distinct()
        return JsonResponse({'ordenes': list(ordenes)})
    return JsonResponse({'ordenes': []})

def get_ordenes_por_finca2(request):
    finca = request.POST.get('finca')
    nombre_usuario = request.user.username
    if finca:
        ordenes = AcumFruta.objects.filter(finca=finca,correo=nombre_usuario)\
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

def obtener_proveedor_desde_finca_llave(finca, llave):
    if finca.strip().lower() == "productor":
        return llave.strip()
    return finca.strip()

def obtener_proveedor_detalle(finca, llave):
    if (finca or "").strip().lower() == "productor":
        return (llave or "").strip()
    return (finca or "").strip()

def aprovechamientos(request):
    hoy = timezone.now().date()
    semana_actual = hoy.isocalendar()[1]
    anio_actual = hoy.year

    # 1. Obtener fecha máxima en detallerecaux
    fecha_max = detallerecaux.objects.aggregate(max_fecha=Max('fechasalidafruta'))['max_fecha']
    if not fecha_max:
        fecha_max = hoy  # fallback si no hay registros

    # 2. Filtrar recepciones hasta esa fecha, semana actual
    recepciones = detallerec.objects.filter(
        fecha__lte=fecha_max
    ).annotate(
        semana=ExtractWeek('fecha'),
        anio=ExtractYear('fecha')
    ).filter(
        semana=semana_actual,
        anio=anio_actual
    ).values('finca', 'cultivo').annotate(total_libras=Sum('libras')).order_by()

    # Crear dict con claves consistentes
    recepciones_dict = {
        formar_clave(r['finca'], r['cultivo']): r['total_libras'] for r in recepciones
    }

    # 3. Filtrar distribuciones por semana actual
    detalles = detallerecaux.objects.annotate(
        semana=ExtractWeek('fechasalidafruta'),
        anio=ExtractYear('fechasalidafruta')
    ).filter(
        semana=semana_actual,
        anio=anio_actual
    )

    boleta_ids = detalles.values_list('boleta', flat=True)
    boletas = Boletas.objects.filter(boleta__in=boleta_ids)
    boletas_dict = {b.boleta: b for b in boletas}

    agrupados = defaultdict(lambda: {'aprovechamiento': 0, 'devolución': 0, 'mediano': 0, 'total': 0})
    detalle_debug = []

    for detalle in detalles:
        boleta = boletas_dict.get(detalle.boleta)
        if not boleta:
            continue
        if detalle.finca == "Productor":
            clave = formar_clave(detalle.llave, detalle.cultivo)
        else:
            clave = formar_clave(detalle.finca, detalle.cultivo)
        calidad = (boleta.calidad or '').strip().lower()
        libras = detalle.libras or 0

        if 'aprovechamiento' in calidad:
            agrupados[clave]['aprovechamiento'] += libras
        elif 'devolución' in calidad:
            agrupados[clave]['devolución'] += libras
        elif 'mediano' in calidad:
            agrupados[clave]['mediano'] += libras

        agrupados[clave]['total'] += libras

        # Solo para depuración: ejemplo con finca VALLE y cultivo GRAPE
        if clave == formar_clave("VALLE", "GRAPE"):
            detalle_debug.append({
                'boleta_id': detalle.boleta,
                'finca': detalle.finca,
                'cultivo': detalle.cultivo,
                'calidad': boleta.calidad,
                'libras': detalle.libras,
                'fecha_salida': detalle.fechasalidafruta,
            })

    # 4. Calcular resultados finales
    resultado = []
    for (finca, cultivo), datos in agrupados.items():
        total_distribuido = datos['total'] or 0
        recepcion_libras = recepciones_dict.get((finca, cultivo), 0)
        pendiente = recepcion_libras - total_distribuido
        if pendiente < 0:
            pendiente = 0
        porcentaje_pendiente = round(pendiente * 100 / recepcion_libras, 2) if recepcion_libras else 0

        resultado.append({
            'proveedor': finca,
            'cultivo': cultivo,
            'porcentaje_aprovechamiento': round(datos['aprovechamiento'] * 100 / total_distribuido, 2) if total_distribuido else 0,
            'porcentaje_devolucion': round(datos['devolución'] * 100 / total_distribuido, 2) if total_distribuido else 0,
            'porcentaje_mediano': round(datos['mediano'] * 100 / total_distribuido, 2) if total_distribuido else 0,
            'porcentaje_pendiente': porcentaje_pendiente,
            'libras_recibidas': round(recepcion_libras, 2),
            'libras_cargadas': round(total_distribuido, 2),
        })

    registros_json = json.dumps(resultado, default=str)
    detalle_debug_json = json.dumps(detalle_debug, default=str)

    return render(request, 'plantaE/inventarioProd_aprovechamientos.html', {
        'registros': resultado,
        'registros_json': registros_json,
        'detalle_debug': detalle_debug_json
    })

def boletas_reporterecepcion(request):
    if request.method == 'POST':
        try:
            opcion1 = request.POST.get('opcion1')  # cultivo
            opcion2 = request.POST.get('opcion2')  # proveedor

            # Obtener recepciones en proceso que coincidan con cultivo
            recepciones_raw = (
                detallerec.objects
                .filter(status="En proceso", cultivo=opcion1)
                .values('recepcion', 'llave', 'finca', 'cultivo', 'fecha')
                .annotate(total_libras=Sum('libras'))
                .order_by('-recepcion')
            )

            # Filtrar por proveedor después de obtener los datos
            recepciones_filtradas = []
            for r in recepciones_raw:
                proveedor = obtener_proveedor_desde_finca_llave(r['finca'], r['llave'])
                if proveedor == opcion2:
                    r['proveedor'] = proveedor
                    recepciones_filtradas.append(r)

            # Limitar a 10
            recepciones_filtradas = recepciones_filtradas[:10]

            # Crear diccionario para búsqueda rápida
            recepciones_dict = {
                r['recepcion']: {
                    'total_libras': r['total_libras'],
                    'proveedor': r['proveedor'],
                    'cultivo': r['cultivo'],
                    'fecha': r['fecha'],
                }
                for r in recepciones_filtradas
            }

            # Paso 1: Obtener detalles de esas recepciones
            detalles = (
                detallerecaux.objects
                .filter(status="En proceso", recepcion__in=recepciones_dict.keys())
            )

            # Paso 2: Obtener boletas únicas y cargarlas
            boleta_ids = detalles.values_list('boleta', flat=True).distinct()
            boletas = Boletas.objects.filter(boleta__in=boleta_ids)
            boletas_dict = {b.boleta: b for b in boletas}

            # Paso 3: Agrupar libras por calidad
            agrupados = defaultdict(lambda: {'aprovechamiento': 0, 'mediano': 0, 'devolución': 0, 'total': 0})

            for detalle in detalles:
                boleta = boletas_dict.get(detalle.boleta)
                if not boleta:
                    continue

                calidad = (boleta.calidad or '').strip().lower()
                libras = detalle.libras or 0
                clave = detalle.recepcion  # Usamos recepcion como clave única

                if 'aprovechamiento' in calidad:
                    agrupados[clave]['aprovechamiento'] += libras
                elif 'mediano' in calidad:
                    agrupados[clave]['mediano'] += libras
                elif 'devolución' in calidad:
                    agrupados[clave]['devolución'] += libras

                agrupados[clave]['total'] += libras
            
            resultado = []

            for recepcion_id, datos in agrupados.items():
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

            return JsonResponse({'datos': resultado}, safe=False)




        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    # GET
    return render(request, 'plantaE/boletasFruta_reporterecepciones.html')

def poraprovechamientos(request):
    hoy = timezone.now().date()
    nombre_usuario=request.user.username
    # Obtener fecha máxima en detallerecaux
    fecha_max = AcumFruta.objects.filter(correo=nombre_usuario).aggregate(max_fecha=Max('fecha'))['max_fecha']
    if not fecha_max:
        fecha_max = hoy  # fallback si no hay registros

    # Filtrar las libras totales por variedad desde AcumFruta
    acumfrutadatos = AcumFruta.objects.filter(correo=nombre_usuario).filter(
        fecha__lte=fecha_max
    ).annotate(
        semana=ExtractWeek('fecha'),
        anio=ExtractYear('fecha')
    ).values('finca', 'cultivo', 'orden', 'estructura', 'variedad').annotate(total_libras=Sum('libras')).order_by()

    recepciones_dict = {
        formar_clave(r['finca'], r['cultivo'], r['orden'], r['estructura'], r['variedad']): r['total_libras'] for r in acumfrutadatos
    }

    # Filtrar distribuciones desde AcumFrutaaux
    detalles = AcumFrutaaux.objects.annotate(
        semana=ExtractWeek('fecha'),
        anio=ExtractYear('fecha')
    ).filter(correo=nombre_usuario)

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
        porcentaje_devolucion = round(datos['devolución'] * 100 / recepcion_libras, 2) if recepcion_libras else 0

        resultado.append({
            'proveedor': finca,
            'cultivo': cultivo,
            'orden': orden,
            'estructura': estructura,
            'variedad': variedad,
            'libras': round(recepcion_libras, 2),
            'aprovechamiento': round(datos['aprovechamiento'] * 100 / total_distribuido, 2) if total_distribuido else 0,
            'mediano': round(datos['mediano'] * 100 / total_distribuido, 2) if total_distribuido else 0,
            'devolucion': porcentaje_devolucion,
            'porcentaje_pendiente': porcentaje_pendiente,
        })

    registros_json = json.dumps(resultado, default=str)

    # Convertir los resultados en una tabla HTML
    df = pd.DataFrame(resultado)
    tabla_html = df.to_html(classes="table table-striped", index=False)

    return render(request, 'plantaE/salidasFruta_aprovechamientos.html', {
        'registros': resultado,
        'tabla_html': tabla_html,
        'registros_json': registros_json,
    })


def inventariogeneralfruta_list(request):
    today = timezone.now().date()

    # Obtener todas las salidas de inventario y salidas de contenedores
    salidas = detallerec.objects.all()
    salidas2 = detallerecaux.objects.all()
    
    # Filtrar las salidas de inventario para las que tienen categoría 'Exportación' y sin 'status'
    salidas = salidas.order_by('registro').exclude(status='Cerrado').exclude(status = 'En proceso')
    
    # Excluir los registros de salidas2 donde el contenedor esté vacío
    salidas2 = salidas2.exclude(status='Cerrado')


    # Crear un diccionario para almacenar los resultados agrupados por 'itemsapcode' y 'proveedor'
    agrupaciones = {}

    # Agrupar las salidas de inventario (salidas) por 'itemsapcode' y 'proveedor'
    for salida in salidas:
        # Revisar si la finca es 'RIO', 'VALLE', o 'CIP' y asignar 'SDC' si es cierto
        finca = salida.finca
        # Crear la clave de agrupación
        if finca == "Productor":
            clave_agrupacion = (salida.llave, salida.cultivo)
            if clave_agrupacion not in agrupaciones:
                agrupaciones[clave_agrupacion] = {
                    'proveedor': salida.llave,
                    'cultivo': salida.cultivo,
                    'total_libras_salidas': 0,  # Cajas de salidas
                    'total_libras_salidas2': 0,  # Cajas de salidas2
                    'salidas': []
                }
        else:
            clave_agrupacion = (finca, salida.cultivo)  # Usar 'SDC' o el valor de finca
            if clave_agrupacion not in agrupaciones:
                agrupaciones[clave_agrupacion] = {
                    'proveedor': finca,  # Usar 'SDC' o el valor de finca
                    'cultivo': salida.cultivo,
                    'total_libras_salidas': 0,  # Cajas de salidas
                    'total_libras_salidas2': 0,  # Cajas de salidas2
                    'salidas': []
                }

        # Acumular las cajas de las salidas
        agrupaciones[clave_agrupacion]['total_libras_salidas'] += salida.libras
        agrupaciones[clave_agrupacion]['salidas'].append(salida)
    
    # Agrupar las salidas de contenedores (salidas2) por 'itemsapcode' y 'proveedor'
    for salida2 in salidas2:
        # Verificar si el contenedor no está vacío antes de acumular las cajas
        
        # Crear la clave de agrupación concatenando 'itemsapcode' y 'proveedor'
        clave_agrupacion = (salida2.finca, salida2.cultivo)
        
        if clave_agrupacion in agrupaciones:
            # Acumular las cajas de las salidas2
            agrupaciones[clave_agrupacion]['total_libras_salidas2'] += salida2.libras
    
    # Ahora, restamos las cajas de 'salidas2' de las de 'salidas' para cada agrupación
    for agrupacion in agrupaciones.values():
        # Restar las cajas de las salidas2 de las de las salidas
        agrupacion['libras_restantes'] = agrupacion['total_libras_salidas'] - agrupacion['total_libras_salidas2']
    
    # Convertir el diccionario en una lista para pasarlo al contexto de la plantilla
    registros_agrupados = list(agrupaciones.values())
    
    # Ordenar la lista de registros por el campo 'proveedor'
    registros_agrupados = sorted(registros_agrupados, key=lambda x: x['proveedor'])
    
    # Pasar los registros agrupados al renderizado de la plantilla
    return render(request, 'plantaE/inventarioProd_inventariogeneralfruta.html', {'registros': registros_agrupados})

def load_contenedores(request):
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
    adicionales = contenedores.objects.exclude(status='Cerrado').values('contenedor')

    return JsonResponse({'adicionales':list(adicionales), 'fecha': fecha_})

def escanearbarras(request):
    
    context = {'msm': 'Listo.'}
    return render(request, 'plantaE/escanearbarras.html',context)

def contenedores_list(request):
    salidas = contenedores.objects.exclude(status='Cerrado')  # Excluye los que tienen status 'Cerrado'
    salidas = salidas.order_by('-created_at')
    
    return render(request, 'plantaE/contenedores_list.html', {'registros': salidas})

def contenedores_delete(request, pk):
    salidas = get_object_or_404(contenedores, pk=pk)
    if request.method == 'POST':
        salidas.delete()
        return redirect('contenedores_list')
    return render(request, 'plantaE/contenedores_confirm_delete.html', {'registros': salidas})

def contenedores_create(request):
    if request.method == 'POST':
        form = contenedoresForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                # Manejar excepciones específicas (por ejemplo, UniqueConstraintError)
                return JsonResponse({'error': str(e)}, status=400)
            return redirect('contenedores_list')
        else:
            # Imprimir errores para depuración
            return JsonResponse({'errores': form.errors}, status=400)
    else:
        form = contenedoresForm()

    # Obtener el último registro del contenedor
    ultimo_contenedor = contenedores.objects.last()

    # Si existe un último contenedor, pre-llenar el campo 'nombre' con el valor del último contenedor
    initial_data = {}
    if ultimo_contenedor:
        initial_data['viaje'] = ultimo_contenedor.viaje + 1 # Cambia 'nombre' por el nombre del campo relevante

    # Crear el formulario con los valores iniciales
    form = contenedoresForm(initial=initial_data)

    return render(request, 'plantaE/contenedores_form.html', {
        'form': form,
        'ultimo_contenedor': ultimo_contenedor,
    })

def contenedores_update(request, pk):
    salidas = get_object_or_404(contenedores, pk=pk)
    if request.method == 'POST':
        form = contenedoresForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('contenedores_list')
    else:
        form = contenedoresForm(instance=salidas)
    return render(request, 'plantaE/contenedores_form.html', {'form': form})

def items_list(request):
    salidas = productoTerm.objects.all() # Excluye los que tienen status 'Cerrado'
    salidas = salidas.order_by('-registro')
    
    return render(request, 'plantaE/items_list.html', {'registros': salidas})

def items_delete(request, pk):
    salidas = get_object_or_404(productoTerm, pk=pk)
    if request.method == 'POST':
        salidas.delete()
        return redirect('items_list')
    return render(request, 'plantaE/items_confirm_delete.html', {'registros': salidas})

def items_create(request):
    if request.method == 'POST':
        form = itemsForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                # Manejar excepciones específicas (por ejemplo, UniqueConstraintError)
                return JsonResponse({'error': str(e)}, status=400)
            return redirect('items_list')
        else:
             # Imprimir errores para depuración
            return JsonResponse({'errores': form.errors}, status=400)
    else:
        form = itemsForm()
    return render(request, 'plantaE/items_form.html', {'form': form,'modo':'crear'})

def items_update(request, pk):
    salidas = get_object_or_404(productoTerm, pk=pk)
    if request.method == 'POST':
        form = itemsForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('items_list')
    else:
        form = itemsForm(instance=salidas)
    return render(request, 'plantaE/items_form.html', {'form': form,'modo':'actualizar'})

def itemsenvios_list(request):
    salidas = paramenvlocales.objects.all() # Excluye los que tienen status 'Cerrado'
    salidas = salidas.order_by('-registro')
    
    return render(request, 'plantaE/itemsenvios_list.html', {'registros': salidas})

def itemsenvios_delete(request, pk):
    salidas = get_object_or_404(paramenvlocales, pk=pk)
    if request.method == 'POST':
        salidas.delete()
        return redirect('itemsenvios_list')
    return render(request, 'plantaE/itemsenvios_confirm_delete.html', {'registros': salidas})

def itemsenvios_create(request):
    if request.method == 'POST':
        form = itemsenviosForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                # Manejar excepciones específicas (por ejemplo, UniqueConstraintError)
                return JsonResponse({'error': str(e)}, status=400)
            return redirect('itemsenvios_list')
        else:
             # Imprimir errores para depuración
            return JsonResponse({'errores': form.errors}, status=400)
    else:
        form = itemsenviosForm()
    return render(request, 'plantaE/itemsenvios_form.html', {'form': form,'modo':'crear'})

def itemsenvios_update(request, pk):
    salidas = get_object_or_404(paramenvlocales, pk=pk)
    if request.method == 'POST':
        form = itemsenviosForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('itemsenvios_list')
    else:
        form = itemsenviosForm(instance=salidas)
    return render(request, 'plantaE/itemsenvios_form.html', {'form': form,'modo':'actualizar'})