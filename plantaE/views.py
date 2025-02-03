from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import logging
from openpyxl import Workbook
# Create your views here.
from django.shortcuts import get_object_or_404, redirect
from .models import Actpeso,Boletas, detallerecaux,detallerec,salidasFruta, usuariosAppFruta, datosProduccion, detallesProduccion, detallesEstructuras, Recepciones, Ccalidad,causasRechazo,inventarioProdTerm,productoTerm,cultivoxFinca,AcumFruta
from .forms import pesosForm,salidasFrutaForm, recepcionesForm, ccalidadForm, inventarioFrutaForm, acumFrutaForm
from django.db.models import Sum, Q
from django.utils import timezone
import matplotlib.pyplot as plt
import datetime
from io import BytesIO
import base64
import json
import pandas as pd
import pytz

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
        datos_rio = AcumFruta.objects.filter(fecha=opcion1, finca="RIO").values(
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
        datos_valle = AcumFruta.objects.filter(fecha=opcion1, finca="VALLE").values(
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
        datos_provalle = AcumFruta.objects.filter(fecha=opcion1, finca="PRODUCTOS DEL VALLE, S.A.").values(
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
    return JsonResponse({'username': nombre_usuario,'fecha':fecha_,'adicionales':list(adicionales),'finca':list(datos)[0]['finca'] })

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


def pesos_list(request):
    today = timezone.now().date()
    salidas = Actpeso.objects.filter(fecha=today)
    salidas = salidas.order_by('created')
    
    return render(request, 'plantaE/pesos_list.html', {'registros': salidas})

def pesos_detail(request, pk):
    salidas = get_object_or_404(Actpeso, pk=pk)
    return render(request, 'plantaE/pesos_detail.html', {'registros': salidas})

def article_list(request):
    today = timezone.now().date()
    nombre_usuario = request.user.username
    salidas = salidasFruta.objects.filter(fecha=today,correo=nombre_usuario)
    salidas = salidas.order_by('-created_at')
    
    return render(request, 'plantaE/salidasFruta_list.html', {'registros': salidas})

def pesos_delete(request, pk):
    salidas = get_object_or_404(Actpeso, pk=pk)
    if request.method == 'POST':
        salidas.delete()
        return redirect('pesos_list')
    return render(request, 'plantaE/pesos_confirm_delete.html', {'registros': salidas})

def article_listValle(request):
    today = timezone.now().date()
    nombre_usuario = request.user.username
    salidas = salidasFruta.objects.filter(fecha=today,correo=nombre_usuario)
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
        datos = salidasFruta.objects.filter(fecha=i[8],finca=i[7],cultivo=i[2])
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
    
    #mensaje = request.POST.get('array')
    
    for i in mensaje:
        pesostd = productoTerm.objects.filter(itemsapcode=i[0]).first()
        pesotarima = 54
        pesosintara = int(i[3]) - float(pesostd.taraxcaja)*int(i[2]) -pesotarima
        pesoestandar = float(pesostd.pesostdxcaja)*int(i[2])
        pesostdxcaja = pesostd.pesostdxcaja
        merma = pesosintara-pesoestandar
        
        pesoporcaja = pesosintara/int(i[2])
        ordenemp=pesostd.orden
        if i[2] == '':
            i[2] == None
        inventarioProdTerm.objects.create(fecha=i[8],proveedor=i[5],cultivo=i[6],itemsapcode=i[0],itemsapname=i[1],cajas=i[2],categoria=i[7],libras=i[3],lbsintara=pesosintara,pesostd=pesoestandar,merma=merma,pesorxcaja=pesoporcaja,orden=ordenemp,pesostdxcaja=pesostdxcaja)
        if merma > 0:
            inventarioProdTerm.objects.create(fecha=i[8],proveedor=i[5],cultivo=i[6],itemsapcode=i[0],itemsapname=i[1],cajas=0,categoria="Merma",libras=0,lbsintara=merma,pesostd=0,merma=merma,pesorxcaja=0,orden="SM",pesostdxcaja=0)
            
    return JsonResponse({'mensaje':mensaje})

def cuadrar_RioDia(request):
    today = timezone.now().date()
    nombre_usuario = request.user.username
     # Obtener todos los registros para el usuario y la fecha
    registros = salidasFruta.objects.filter(fecha=today, correo=nombre_usuario, libras__isnull=False)

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
        registros = salidasFruta.objects.filter(fecha=opcion2,cultivo=opcion1,correo=nombre_usuario,libras__isnull=False)

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
    registros = salidasFruta.objects.filter(fecha=today, correo=nombre_usuario,libras__isnull=False)

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
        registros = salidasFruta.objects.filter(fecha=opcion2,cultivo=opcion1,correo=nombre_usuario,libras__isnull=False)

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
        'Cultivo': 'first',
        'Finca': 'first',
        'Viaje': 'first',
        'Fecha': 'first',
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
            return redirect('salidasFruta_list')
        else:
             # Imprimir errores para depuración
            return JsonResponse({'errores': form.errors}, status=400)
    else:
        form = salidasFrutaForm()
    return render(request, 'plantaE/salidasFruta_form.html', {'form': form})

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
            return redirect('salidasFruta_list')
    else:
        form = salidasFrutaForm(instance=salidas)
    return render(request, 'plantaE/salidasFruta_form.html', {'form': form})

def article_delete(request, pk):
    salidas = get_object_or_404(salidasFruta, pk=pk)
    if request.method == 'POST':
        salidas.delete()
        return redirect('salidasFruta_list')
    return render(request, 'plantaE/salidasFruta_confirm_delete.html', {'registros': salidas})

def article_deleteValle(request, pk):
    salidas = get_object_or_404(salidasFruta, pk=pk)
    if request.method == 'POST':
        salidas.delete()
        return redirect('salidasFruta_listValle')
    return render(request, 'plantaE/salidasFruta_confirm_deleteValle.html', {'registros': salidas})

def acumFruta_list(request):
    today = timezone.now().date()
    nombre_usuario = request.user.username
    salidas = AcumFruta.objects.filter(fecha=today,correo=nombre_usuario)
    
    salidas = salidas.order_by('-created_at')
    
    
    return render(request, 'plantaE/AcumFrutaDia_list.html', {'registros': salidas})

def acumFruta_detail(request, pk):
    salidas = get_object_or_404(AcumFruta, pk=pk)
    return render(request, 'plantaE/AcumFrutaDia_detail.html', {'registros': salidas})

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
        form = acumFrutaForm()
    return render(request, 'plantaE/AcumFrutaDia_form.html', {'form': form})

def acumFruta_update(request, pk):
    salidas = get_object_or_404(AcumFruta, pk=pk)
    if request.method == 'POST':
        form = acumFrutaForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('acumFruta_list')
    else:
        form = acumFrutaForm(instance=salidas)
    return render(request, 'plantaE/AcumFrutaDia_form.html', {'form': form})

def acumFruta_delete(request, pk):
    salidas = get_object_or_404(AcumFruta, pk=pk)
    if request.method == 'POST':
        salidas.delete()
        return redirect('acumFruta_list')
    return render(request, 'plantaE/acumFruta_confirm_delete.html', {'registros': salidas})

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
    today = timezone.now().date()
    #salidas = Recepciones.objects.filter(fecha=today)
    salidas= detallerec.objects.all()
    salidas2= detallerecaux.objects.all()
    salidas = salidas.order_by('recepcion').filter(status=None)
    
    for i in salidas:
        cajasacum = salidas2.order_by('-created').filter(Q(status="En proceso") | Q(status="Cerrado"),recepcion=i.recepcion).aggregate(sumacajas=Sum('cajas'))['sumacajas']
        librasacum = salidas2.order_by('-created').filter(Q(status="En proceso") | Q(status="Cerrado"),recepcion=i.recepcion).aggregate(sumalibras=Sum('libras'))['sumalibras']    
        if librasacum != None and cajasacum != None:
            i.cajas = i.cajas - int(cajasacum)
            i.libras = i.libras - float(librasacum)
        

    #existenciaCajas = finca=list(salidas)[0]['cajas']
    #existenciaLibras = finca=list(salidas)[0]['libras']
    #rebajaCajas = finca=list(salidas2)[0]['cajas']
    #rebajaLibras = finca=list(salidas2)[0]['libras']
    #for i in len(salidas):
    #    existenciaCajas 
    return render(request, 'plantaE/recepciones_list.html', {'registros': salidas})

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
    registros = AcumFruta.objects.filter(**filtros)
    

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
    salidas = salidas.order_by('boleta')
     
    return render(request, 'plantaE/boletas_list.html', {'registros': salidas})

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
    salidas = Ccalidad.objects.all()

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
    return render(request, 'plantaE/ccalidad_form.html', {'form': form})

def ccalidad_update(request, pk):
    salidas = get_object_or_404(Ccalidad, pk=pk)
    if request.method == 'POST':
        form = ccalidadForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('ccalidad_list')
    else:
        form = ccalidadForm(instance=salidas)
        
    return render(request, 'plantaE/ccalidad_form_edit.html', {'form': form})

def ccalidad_update_aux(request):
    pk = request.GET.get('pk')
    salidas = get_object_or_404(Ccalidad, pk=pk)
    causa_rechazo = causasRechazo.objects.all().values('causa')
    return JsonResponse({'llave': salidas.llave,'recepcion':salidas.recepcion,'causa_select':salidas.causarechazo,'causas':list(causa_rechazo)})
    

def ccalidad_delete(request, pk):
    salidas = get_object_or_404(Ccalidad, pk=pk)
    if request.method == 'POST':
        salidas.delete()
        return redirect('ccalidad_list')
    return render(request, 'plantaE/ccalidad_confirm_delete.html', {'registros': salidas})

def obtener_llave_recepcion(request):
    # Obtén la fecha límite

    # Obtén los criterios únicos filtrando por fecha
    llave_recepcion = detallerec.objects.filter(recepcion__gte=304).values('criterio').distinct()
    llave_recepcion2 = detallerec.objects.filter(recepcion__gte=304).values('recepcion').distinct()
    #valor = Ccalidad.objects.filter(llave=llave_recepcion).aggregate(suma=Sum('porcentaje'))['suma']
    # Crea un diccionario para almacenar las sumas de porcentaje por llave
    suma_por_llave = Ccalidad.objects.values('llave').annotate(suma=Sum('porcentaje'))

    # Convierte el resultado a un diccionario para facilitar el acceso
    suma_dict = {item['llave']: item['suma'] for item in suma_por_llave}

    # Filtra las llaves_recepcion si su suma es igual a 1
    llaves_recepcion_filtradas = [
        llave for llave in llave_recepcion 
        if suma_dict.get(llave['criterio'], 0) != 1
    ]

    causa_rechazo = causasRechazo.objects.all().values('causa')
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
    return JsonResponse({'llaves': list(llaves_recepcion_filtradas),'causa':list(causa_rechazo),'fecha':fecha_,'llave':list(llave_recepcion2)})

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
    today = timezone.now().date()
    #salidas = Recepciones.objects.filter(fecha=today)
    salidas = inventarioProdTerm.objects.filter(fecha=today)
    return render(request, 'plantaE/inventarioProd_list.html', {'registros': salidas})

def inventarioProd_detail(request, pk):
    salidas = get_object_or_404(inventarioProdTerm, pk=pk)
    return render(request, 'plantaE/inventarioProd_detail.html', {'registros': salidas})

def acumFruta_consulta(request):

    if request.method == 'POST':
        opcion1 = request.POST.get('opcion1')
        opcion2 = request.POST.get('opcion2')
        nombre_usuario = request.user.username
        # Filtra tus datos según la opción seleccionada
        datos = AcumFruta.objects.filter(cultivo=opcion1,fecha=opcion2,correo=nombre_usuario,libras__isnull=False) 
        # Obtener todos los registros para el usuario y la fecha
        registros = AcumFruta.objects.filter(cultivo=opcion1,fecha=opcion2,correo=nombre_usuario,libras__isnull=False)
        df = pd.DataFrame(list(datos.values()),columns=['id','fecha','finca','orden','cultivo','variedad','cajas','libras','estructura'])

        df_agrupado = df.groupby(['orden','estructura','variedad'], as_index=False).agg(
            total_cajas=('cajas', 'sum'),
            cultivo=('cultivo', 'first'),  # Conservar el primer correo asociado
            total_libras=('libras', 'sum'),
            id=('id', 'first'),
            fecha =('fecha', 'first'),
            finca =('finca', 'first'),
            orden =('orden', 'first'),
            variedad =('variedad', 'first'),
            estructura =('estructura', 'first')
        )
        df_agrupado = df_agrupado.sort_values(by='orden')
        registros_finales = df_agrupado.to_dict(orient='records')
        # Crear un DataFrame a partir de los registros, incluyendo todas las columnas
        df = pd.DataFrame(list(registros.values()),columns=['fecha','finca','cultivo','cajas','libras'])

        # Agrupar por 'variedad' y sumar las 'cajas'
        df_agrupado = df.groupby('cultivo', as_index=False).agg(
            total_cajas=('cajas', 'sum'),
            total_libras=('libras', 'sum'),
            cultivo=('cultivo', 'first'),  # Conservar el primer correo asociado
            fecha=('fecha', 'first'),
            finca =('finca', 'first')
        )

        registros_finales2 = df_agrupado.to_dict(orient='records')
        return JsonResponse({'datos': registros_finales,'opcion1':opcion1,'opcion2':opcion2,'resumen':registros_finales2}, safe=False)
    return render(request, 'plantaE/AcumFrutaDia_list.html')


def acumFruta_consultaValle(request):
    
    if request.method == 'POST':
        opcion1 = request.POST.get('opcion1')
        opcion2 = request.POST.get('opcion2')
        nombre_usuario = request.user.username
        # Filtra tus datos según la opción seleccionada
        datos = AcumFruta.objects.filter(cultivo=opcion1,fecha=opcion2,correo=nombre_usuario,libras__isnull=False) 
        # Obtener todos los registros para el usuario y la fecha
        registros = AcumFruta.objects.filter(cultivo=opcion1,fecha=opcion2,correo=nombre_usuario,libras__isnull=False)
        df = pd.DataFrame(list(datos.values()),columns=['id','fecha','finca','orden','cultivo','variedad','cajas','libras','estructura'])

        df_agrupado = df.groupby(['orden','estructura','variedad'], as_index=False).agg(
            total_cajas=('cajas', 'sum'),
            total_libras=('libras', 'sum'),
            cultivo=('cultivo', 'first'),  # Conservar el primer correo asociado
            id=('id', 'first'),
            fecha =('fecha', 'first'),
            finca =('finca', 'first'),
            orden =('orden', 'first'),
            variedad =('variedad', 'first'),
            estructura =('estructura', 'first')
        )
        df_agrupado = df_agrupado.sort_values(by='orden')
        registros_finales = df_agrupado.to_dict(orient='records')
        # Crear un DataFrame a partir de los registros, incluyendo todas las columnas
        df = pd.DataFrame(list(registros.values()),columns=['fecha','finca','cultivo','cajas','libras'])

        # Agrupar por 'variedad' y sumar las 'cajas'
        df_agrupado = df.groupby('cultivo', as_index=False).agg(
            total_cajas=('cajas', 'sum'),
            total_libras=('libras', 'sum'),
            cultivo=('cultivo', 'first'),  # Conservar el primer correo asociado
            fecha=('fecha', 'first'),
            finca =('finca', 'first')
        )

        registros_finales2 = df_agrupado.to_dict(orient='records')
        return JsonResponse({'datos': registros_finales,'opcion1':opcion1,'opcion2':opcion2,'resumen':registros_finales2}, safe=False)
    return render(request, 'plantaE/AcumFrutaDia_listValle.html')

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
    if request.method == 'POST':
        salidas.delete()
        return redirect('inventarioProd_list')
    return render(request, 'plantaE/inventarioProd_confirm_delete.html', {'registros': salidas})

def load_inventarioProdparam(request):
    cultivo_ = request.GET.get('campo1')
    categoria_ = request.GET.get('campo2')

    if cultivo_ != None and categoria_ != None:
        datos = productoTerm.objects.filter(cultivo=cultivo_,categoria=categoria_).values('itemsapcode','itemsapname')
    
    return JsonResponse({'datos': list(datos),'cultivo':cultivo_,'categoria':categoria_})

def plantaEhomepage(request):
    return render(request,'plantaE/plantaE_home.html')