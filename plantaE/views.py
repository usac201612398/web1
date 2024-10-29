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
import datetime
import json
import pandas as pd
import pytz

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
    return JsonResponse({'username': nombre_usuario,'fecha':fecha_})

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

def load_dataUsuario2(request):
    ordenSelect = request.GET.get('category_id')

    cultivo= datosProduccion.objects.filter(orden=ordenSelect,status="Abierta").values('cultivo')
    variedad = detallesProduccion.objects.filter(cultivo=list(cultivo)[0]['cultivo']).values('variedad')
    estructura = detallesEstructuras.objects.filter(orden=ordenSelect).values('estructura')
    return JsonResponse({'datos': list(cultivo),'variedad':list(variedad),'estructura':list(estructura),'orden':ordenSelect})

def load_dataUsuario3(request):
    cultivo_ = request.GET.get('category_id')
    finca_ = request.GET.get('finca')
    variedad= cultivoxFinca.objects.filter(finca=finca_,cultivo=cultivo_).values('variedad').distinct('variedad')
    #variedad = cultivoxFinca.objects.filter(cultivo=list(cultivo)[0]['cultivo']).values('variedad')
    return JsonResponse({'datos': list(variedad)})

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
    
    for i in mensaje:
        datos = salidasFruta.objects.filter(fecha=i[8],finca=i[7],orden=i[1],cultivo=i[2])
        # Calcular las sumas
        suma_cajas = datos.aggregate(Sum('cajas'))['cajas__sum'] or 0
        suma_libras = datos.aggregate(Sum('libras'))['libras__sum'] or 0

        pesoxcaja = suma_libras/suma_cajas
        librasestructura = i[5]*pesoxcaja
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
    context = {

        'usuario': nombre_usuario,
        'registros': list(estructura),
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

def recepciones_reportecurva(request):

    finca_id = request.GET.get('finca')
    orden_id = request.GET.get('orden')

    registros_filtrados = AcumFruta.objects.filter(finca=finca_id, orden=orden_id)
    df = pd.DataFrame(list(registros_filtrados.values()), columns=['fecha', 'finca', 'cultivo', 'variedad', 'cajas', 'libras', 'orden'])
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    df['semana'] = df['fecha'].dt.isocalendar().week

    # Agrupamos los datos por semana
    df_agrupado = df.groupby(['semana'], as_index=False).agg(
        total_libras=('libras', 'sum')
    )
    df_agrupado['total_kilos'] = df_agrupado['total_libras'] * 0.453592

    # Obtener el área para el orden seleccionado
    area = datosProduccion.objects.filter(orden=orden_id).first()
    area_valor = area.area if area else 0  # Obtener el área, asegurándonos de que no sea nula

    # Calcular kilos por área
    df_agrupado['kilos_por_area'] = df_agrupado['total_kilos'] / area_valor if area_valor else 0

    result = df_agrupado[['semana', 'kilos_por_area']].to_dict(orient='records')
    return JsonResponse(result, safe=False)

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
    # Obtén el nombre de usuario del usuario autenticado
    llave_recepcion = detallerec.objects.values('criterio').distinct('criterio')
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
    return JsonResponse({'llaves': list(llaves_recepcion_filtradas),'causa':list(causa_rechazo),'fecha':fecha_})

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
        datos = productoTerm.objects.filter(cultivo=opcion1,categoria=opcion2).values('calidad1')  # Ajusta los campos
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
        datos = productoTerm.objects.filter(cultivo=cultivo_,categoria=categoria_).values('calidad1')
    
    return JsonResponse({'datos': list(datos),'cultivo':cultivo_,'categoria':categoria_})

def plantaEhomepage(request):
    return render(request,'plantaE/plantaE_home.html')