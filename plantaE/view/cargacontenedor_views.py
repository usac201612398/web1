import json
import pandas as pd

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.utils import timezone
from django.urls import reverse
from django.contrib import messages

from django.db.models import Q, Sum

from plantaE.models import (
    inventarioProdTerm,
    inventarioProdTermAux,
    salidacontenedores,
    productoTerm
)

from plantaE.forms import salidacontenedoresForm
from .auxiliares import *

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
        producto = productoTerm.objects.filter(itemsapcode=itemsapcode).first()
        precio = float(producto.precio) if producto and producto.precio else 0.0
        
        itemsapname = producto.itemsapname
        cajas_a_enviar = int(i[4])
        fecha_salida = i[9]


        disponibles = inventarioProdTerm.objects.filter(
            proveedor=proveedor,
            itemsapcode=itemsapcode,
            categoria="Exportación"
        ).filter(
            Q(status__isnull=True) | Q(status='')
        ).exclude(status='Anulado').order_by('fecha', 'registro')

        usados = inventarioProdTermAux.objects.filter(
            proveedor=proveedor,
            itemsapcode=itemsapcode,
            categoria="Exportación"
        ).filter(
            Q(status__isnull=True) | Q(status='')
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
            aux_sum = inventarioProdTermAux.objects.filter(inventarioreg=registro.registro).exclude(status="Anulado").aggregate(
                sumacajas=Sum('cajas'),
                sumalbs=Sum('lbsintara')
            )
            if (aux_sum['sumacajas'] or 0) >= total_cajas and (aux_sum['sumalbs'] or 0) >= total_libras:
                registro.status = 'En proceso'
                registro.save()
                inventarioProdTermAux.objects.filter(inventarioreg=registro.registro).update(status='En proceso')

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
                'calidad1': salida.calidad1,
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

    return render(request, 'plantaE/cargacontenedor/inventarioProd_ccontenedor.html', {'registros': registros_agrupados, 'registros_json':registros_json})

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
    return render(request, 'plantaE/cargacontenedor/inventarioProd_contenedores.html', {'registros': salidas})

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

    return render(request, 'plantaE/cargacontenedor/inventarioProd_packinglist.html', context)

def contenedorpacking_list_detail(request):

    # Filtra tus datos según la opción seleccionada
    contenedores = salidacontenedores.objects.order_by("-registro").exclude(Q(status='Cerrado') | Q(status='Anulado'))

    return render(request, 'plantaE/cargacontenedor/inventarioProd_packinglist_detail.html', {'data':contenedores})

def packinglist_update(request, pk):
    salidas = get_object_or_404(salidacontenedores, pk=pk)
    if request.method == 'POST':
        form = salidacontenedoresForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('inventarioProd_packinglist_detail')
    else:
        form = salidacontenedoresForm(instance=salidas)
    return render(request, 'plantaE/cargacontenedor/inventarioProd_packinglist_form.html', {'form': form})

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
        return render(request, 'plantaE/cargacontenedor/inventarioProd_packinglist_confirm_delete.html', {
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

        return render(request, 'plantaE/cargacontenedor/inventarioProd_packinglist_confirm_delete.html', {
            'registros': salidas,
            'alert_message': "Paleta anulada correctamente.",
            'redirect_url': reverse('inventarioProd_packinglist_detail')
        })

    return render(request, 'plantaE/cargacontenedor/inventarioProd_packinglist_confirm_delete.html', {
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

    return render(request, 'plantaE/cargacontenedor/inventarioProd_packinglist_confirm_delete.html', {'registros': salidas})

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

    # semana basada en el contenedor
    semana_contenedor = infoconten.fecha.isocalendar()[1]

    # filtrar por la semana del contenedor
    df_filtrado = df[df['semana_contenedor'] == semana_contenedor]

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
        return render(request, 'plantaE/cargacontenedor/packinglist_template.html', context)
   
    else:
        # Si no hay datos, devuelve una respuesta vacía o de error
        return JsonResponse({'error': 'No hay datos disponibles para esta semana'}, status=400)
    
def generate_packing_list_pdf2(request):

    # Recibir parámetros por GET
    fecha = request.GET.get('fecha')
    contenedor = request.GET.get('contenedor')

    if not fecha or not contenedor:
        return JsonResponse({'error': 'Faltan parámetros: fecha y contenedor'}, status=400)

    # Convertir fecha
    try:
        fecha_obj = datetime.datetime.strptime(fecha, "%Y-%m-%d").date()
    except:
        return JsonResponse({'error': 'Formato de fecha inválido'}, status=400)

    # Información del contenedor
    infoconten = contenedores.objects.filter(
        contenedor=contenedor
    ).exclude(status="Anulado").first()

    if not infoconten:
        return JsonResponse({'error': 'Contenedor no encontrado'}, status=404)

    # Obtener toda la fruta del contenedor en esa fecha
    qs = salidacontenedores.objects.filter(
        contenedor=contenedor,
        fechasalcontenedor=fecha_obj
    ).exclude(status="Anulado")

    if not qs.exists():
        return JsonResponse({'error': 'No hay registros para este contenedor y fecha'}, status=404)

    # Agrupado igual al template
    datos = qs.values(
        "palet",
        "proveedor",
        "itemsapname",
        "fechasalcontenedor"
    ).annotate(
        total_cajas=Sum("cajas")
    ).order_by("palet")

    # Contexto para el template
    context = {
        'planta': 'SDC',
        'destino': infoconten.destino,
        'contenedor': infoconten.contenedor,
        'fecha': fecha_obj,
        'viaje': infoconten.viaje,
        'marchamo': infoconten.marchamo,
        'placacamion': infoconten.placacamion,
        'temperatura': infoconten.temperatura,
        'ventilacion': infoconten.ventilacion,
        'hora': infoconten.horasalida,
        'piloto': infoconten.piloto,
        'transportista': infoconten.transportista,
        'datos': datos
    }

    return render(request, "plantaE/cargacontenedor/packinglist_template.html", context)

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

def procesarinvprodconten(request):

    data = json.loads(request.body)
    mensaje = data['array']
    contenedor_=data['contenedor']
    today = timezone.localtime(timezone.now()).date()
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