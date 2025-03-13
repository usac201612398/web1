from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import logging
from openpyxl import Workbook
# Create your views here.
from django.shortcuts import get_object_or_404, redirect
from .models import Actpeso,salidacontenedores, productores,contenedores,Boletas, detallerecaux,detallerec,salidasFruta, usuariosAppFruta, datosProduccion, detallesProduccion, detallesEstructuras, Recepciones, Ccalidad,causasRechazo,inventarioProdTerm,productoTerm,cultivoxFinca,AcumFruta
from .forms import pesosForm,salidasFrutaForm, contenedoresForm,recepcionesForm, ccalidadForm, inventarioFrutaForm, acumFrutaForm
from django.db.models import Sum, Q
from django.utils import timezone
import matplotlib.pyplot as plt
import datetime
from io import BytesIO
import base64
import json
import pandas as pd
import pytz
from openpyxl.utils.dataframe import dataframe_to_rows
import pdfkit
from django.template.loader import render_to_string

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
        productor_ = productores.objects.filter(productor=i[5]).first()
        pesotarima = 54    
        tara  = float(pesostd.taraxcaja)*int(i[2]) + pesotarima
        pesosintara = int(i[3]) - tara 
        pesoestandar = float(pesostd.pesostdxcaja)*int(i[2])
        pesostdxcaja = pesostd.pesostdxcaja
        if pesosintara < pesoestandar:
            merma = 0
        else:
            merma = pesosintara-pesoestandar
        pesosinmerma = pesosintara-merma
        pesoporcaja = pesosintara/int(i[2])
        ordenemp=pesostd.orden
        if i[2] == '':
            i[2] == None
        if productor_.tipo=="EM":
            inventarioProdTerm.objects.create(fecha=i[8],proveedor=i[5],cultivo=i[6],itemsapcode=i[0],itemsapname=i[1],cajas=i[2],categoria=i[7],libras=i[3],lbsintara=pesosintara,pesostd=pesoestandar,merma=merma,pesorxcaja=pesoporcaja,orden="EM",pesostdxcaja=pesostdxcaja,tara=tara,pesosinmerma=pesosinmerma,calidad1=pesostd.calidad1)
            #if merma > 0:
            #    inventarioProdTerm.objects.create(fecha=i[8],proveedor=i[5],cultivo=i[6],itemsapcode=i[0],itemsapname=i[1],cajas=0,categoria="Merma",libras=0,lbsintara=merma,pesostd=0,merma=merma,pesorxcaja=0,orden="SM",pesostdxcaja=0,tara=tara,pesosinmerma=pesosinmerma,calidad1=pesostd.calidad1)       
        else:
            inventarioProdTerm.objects.create(fecha=i[8],proveedor=i[5],cultivo=i[6],itemsapcode=i[0],itemsapname=i[1],cajas=i[2],categoria=i[7],libras=i[3],lbsintara=pesosintara,pesostd=pesoestandar,merma=merma,pesorxcaja=pesoporcaja,orden=ordenemp,pesostdxcaja=pesostdxcaja,tara=tara,pesosinmerma=pesosinmerma,calidad1=pesostd.calidad1)
            #if merma > 0:
            #    inventarioProdTerm.objects.create(fecha=i[8],proveedor=i[5],cultivo=i[6],itemsapcode=i[0],itemsapname=i[1],cajas=0,categoria="Merma",libras=0,lbsintara=merma,pesostd=0,merma=merma,pesorxcaja=0,orden="SM",pesostdxcaja=0,tara=tara,pesosinmerma=pesosinmerma,calidad1=pesostd.calidad1)
        confirmacion = inventarioProdTerm.objects.filter(categoria="Exportación").order_by('-registro').first()

    return JsonResponse({'mensaje':mensaje,'msm': " Listo, en número de pesada es: " + str(confirmacion.registro)})

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
    
    resultado = df.groupby(['Variedad','Cultivo'] ).agg({
        'Encargado': 'first',  # O 'last', 'min', 'max', etc.
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
    salidas = inventarioProdTerm.objects.filter(fecha=today,categoria="Exportación")
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
        df = pd.DataFrame(list(datos.values()),columns=['id','fecha','finca','viaje','orden','cultivo','variedad','cajas','libras','estructura'])

        df_agrupado = df.groupby(['orden','estructura','variedad'], as_index=False).agg(
            total_cajas=('cajas', 'sum'),
            cultivo=('cultivo', 'first'),  # Conservar el primer correo asociado
            total_libras=('libras', 'sum'),
            id=('id', 'first'),
            fecha =('fecha', 'first'),
            finca =('finca', 'first'),
            viaje =('viaje', 'first'),
            orden =('orden', 'first'),
            variedad =('variedad', 'first'),
            estructura =('estructura', 'first')
        )
        df_agrupado = df_agrupado.sort_values(by=['viaje', 'orden'])

        registros_finales = df_agrupado.to_dict(orient='records')
        # Crear un DataFrame a partir de los registros, incluyendo todas las columnas
        df = pd.DataFrame(list(registros.values()),columns=['fecha','finca','viaje','cultivo','cajas','libras'])

        # Agrupar por 'variedad' y sumar las 'cajas'
        df_agrupado = df.groupby('cultivo', as_index=False).agg(
            total_cajas=('cajas', 'sum'),
            total_libras=('libras', 'sum'),
            viaje=('viaje', 'first'),
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
        df = pd.DataFrame(list(datos.values()),columns=['id','fecha','finca','viaj','orden','cultivo','variedad','cajas','libras','estructura'])

        df_agrupado = df.groupby(['orden','estructura','variedad'], as_index=False).agg(
            total_cajas=('cajas', 'sum'),
            total_libras=('libras', 'sum'),
            cultivo=('cultivo', 'first'),  # Conservar el primer correo asociado
            id=('id', 'first'),
            fecha =('fecha', 'first'),
            finca =('finca', 'first'),
            viaje =('viaje', 'first'),
            orden =('orden', 'first'),
            variedad =('variedad', 'first'),
            estructura =('estructura', 'first')
        )
        df_agrupado = df_agrupado.sort_values(by=['viaje', 'orden'])
        registros_finales = df_agrupado.to_dict(orient='records')
        # Crear un DataFrame a partir de los registros, incluyendo todas las columnas
        df = pd.DataFrame(list(registros.values()),columns=['fecha','finca','cultivo','viaje','cajas','libras'])

        # Agrupar por 'variedad' y sumar las 'cajas'
        df_agrupado = df.groupby('cultivo', as_index=False).agg(
            total_cajas=('cajas', 'sum'),
            total_libras=('libras', 'sum'),
            viaje=('viaje', 'first'),
            cultivo=('cultivo', 'first'),  # Conservar el primer correo asociado
            fecha=('fecha', 'first'),
            finca =('finca', 'first')
        )

        registros_finales2 = df_agrupado.to_dict(orient='records')
        return JsonResponse({'datos': registros_finales,'opcion1':opcion1,'opcion2':opcion2,'resumen':registros_finales2}, safe=False)
    return render(request, 'plantaE/AcumFrutaDia_listValle.html')



def validaroventa(request):
    # Recibe los datos desde el body de la solicitud
    data = json.loads(request.body)
    contenedores_array = data.get('array')  # Contenedores recibidos en el array

    # Filtra los contenedores que no tienen el status "Cerrado" y que están en el array de contenedores
    contenedores_a_cerrar = salidacontenedores.objects.filter(
        contenedor=contenedores_array
    ).exclude(status='Cerrado')

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
    infoconten = contenedores.objects.exclude(status="Cerrado").filter(contenedor=contenedor).first()
    if not infoconten:
        return JsonResponse({'error': 'Contenedor no encontrado'}, status=404)

    # Filtra los contenedores que no tienen el status "Cerrado" y que están en el array de contenedores
    contenedores_a_imprimir = salidacontenedores.objects.filter(contenedor=contenedor).order_by("registro").values('proveedor','itemsapcode','itemsapname','contenedor','fechasalcontenedor','cajas','importe','cultivo','palet')

    # Convierte el QuerySet a un DataFrame de pandas
    df = pd.DataFrame(list(contenedores_a_imprimir))
    df['fechasalcontenedor'] = pd.to_datetime(df['fechasalcontenedor'], errors='coerce')
    df['semana_contenedor'] = df['fechasalcontenedor'].dt.isocalendar().week
    df['semana_actual'] = semana_actual

    # Filtra el DataFrame para que solo contenga los registros de la semana actual
    df_filtrado = df[df['semana_contenedor'] == semana_actual]

    if not df_filtrado.empty:
        # Agrupar por 'itemsapcode', 'palet', 'proveedor' y calcular la suma de las cajas
        df_agrupado = df_filtrado.groupby(['itemsapcode', 'palet', 'proveedor'], as_index=False).agg(
            fechasalcontenedor=('fechasalcontenedor', 'first'),
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

def reporteInventario(request):
    opcion1 = timezone.now().date()

    # Filtra tus datos según la opción seleccionada
    datos_empaque = inventarioProdTerm.objects.filter(fecha=opcion1,categoria="Exportación").values(
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
        datos_empaque = inventarioProdTerm.objects.filter(fecha=opcion1,categoria="Exportación").values(
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
    contenedores = salidacontenedores.objects.exclude(status="Cerrado").order_by("registro").values('proveedor','itemsapcode','itemsapname','contenedor','fechasalcontenedor','cajas','importe','cultivo')

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
        contenedor = salidacontenedores.objects.filter(contenedor=opcion1).order_by("registro").values('proveedor','itemsapcode','itemsapname','contenedor','fechasalcontenedor','cajas','importe','cultivo')


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
                i.status = 'En proceso'
    
    # Filtrar las salidas para que solo contengan aquellas con cajas > 0
    salidas = [i for i in salidas if i.cajas > 0]

    # Retornar las salidas que cumplen con la condición (cajas > 0)
    return render(request, 'plantaE/inventarioProd_contenedores.html', {'registros': salidas})


def inventariogeneral_list(request):
    today = timezone.now().date()

    # Obtener todas las salidas de inventario y salidas de contenedores
    salidas = inventarioProdTerm.objects.all()
    salidas2 = salidacontenedores.objects.all()

    # Filtrar las salidas de inventario para las que tienen categoría 'Exportación' y sin 'status'
    salidas = salidas.filter(categoria="Exportación").order_by('registro').exclude(status='Cerrado')

    # Excluir los registros de salidas2 donde el contenedor esté vacío
    salidas2 = salidas2.exclude(contenedor='0')

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
        if salida2.contenedor is not None:
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

def inventariogeneralfruta_list(request):
    today = timezone.now().date()

    # Obtener todas las salidas de inventario y salidas de contenedores
    salidas = detallerec.objects.all()
    salidas2 = inventarioProdTerm.objects.all()
    
    # Filtrar las salidas de inventario para las que tienen categoría 'Exportación' y sin 'status'
    salidas = salidas.order_by('registro').exclude(status='Cerrado')
    
    # Excluir los registros de salidas2 donde el contenedor esté vacío
    salidas2 = salidas2.exclude(status='Cerrado').exclude(categoria='Merma')


    # Crear un diccionario para almacenar los resultados agrupados por 'itemsapcode' y 'proveedor'
    agrupaciones = {}

    # Agrupar las salidas de inventario (salidas) por 'itemsapcode' y 'proveedor'
    for salida in salidas:
        # Revisar si la finca es 'RIO', 'VALLE', o 'CIP' y asignar 'SDC' si es cierto
        finca = salida.finca
        if finca in ['RIO', 'VALLE', 'CIP']:
            finca = 'SDC'  # Asignar 'SDC' si la finca es uno de los valores específicos
        
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
        clave_agrupacion = (salida2.proveedor, salida2.cultivo)
        
        if clave_agrupacion in agrupaciones:
            # Acumular las cajas de las salidas2
            agrupaciones[clave_agrupacion]['total_libras_salidas2'] += salida2.lbsintara
    
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
    
    adicionales = contenedores.objects.exclude(status='Cerrado').values('contenedor')
    return JsonResponse({'adicionales':list(adicionales)})

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
    return render(request, 'plantaE/contenedores_form.html', {'form': form})

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