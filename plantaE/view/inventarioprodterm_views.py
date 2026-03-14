import json

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.utils import timezone
from django.urls import reverse

from plantaE.models import (
    inventarioProdTerm,
    inventarioProdTermAux,
    productoTerm,
    productores
)

from plantaE.forms import inventarioFrutaForm
from .auxiliares import *
def inventarioProd_list(request):
    today = timezone.localtime(timezone.now()).date()
    #salidas = Recepciones.objects.filter(fecha=today)
    salidas = inventarioProdTerm.objects.filter(fecha=today,categoria="Exportación").exclude(status='Anulado')
    return render(request, 'plantaE/inventarioProdTerm/inventarioProd_list.html', {'registros': salidas})

def inventarioProd_detail(request, pk):
    salidas = get_object_or_404(inventarioProdTerm, pk=pk)
    return render(request, 'plantaE/inventarioProdTerm/inventarioProd_detail.html', {'registros': salidas})

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
            pesotarima = 56
            tara = float(pesostd.taraxcaja) * int(i[2]) + pesotarima
            pesosintara = int(i[3]) - tara
            pesoestandar = float(pesostd.pesostdxcaja) * int(i[2])
            pesostdxcaja = pesostd.pesostdxcaja

            merma = max(0, pesosintara - pesoestandar)
            pesosinmerma = pesosintara - merma
            pesoporcaja = pesosintara / int(i[2]) if int(i[2]) != 0 else 0
            ordenemp = pesostd.orden
            ordenproductor = pesostd.orden2
            pormerma = (merma / pesoestandar) * 100 if pesoestandar > 0 else 0

            if productor_.tipo == "EM":
                if not ordenproductor:  # Esto cubre tanto None como ''
                    orden = "EM"
                else:
                    orden = ordenproductor
            else:
                orden = ordenemp
            inventarioProdTerm.objects.create(
                fecha=i[7],
                proveedor=i[4],
                cultivo=i[5],
                itemsapcode=i[0],
                itemsapname=pesostd.itemsapname,
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

def inventarioProd_create(request):
    if request.method == 'POST':
        opcion1 = request.POST.get('opcion1')
        opcion2 = request.POST.get('opcion2')
        # Filtra tus datos según la opción seleccionada
        datos = productoTerm.objects.filter(cultivo=opcion1,categoria=opcion2).values('itemsapcode','itemsapname','calidad1')  # Ajusta los campos
        return JsonResponse({'datos': list(datos),'opcion1':opcion1,'opcion2':opcion2}, safe=False)
    return render(request, 'plantaE/inventarioProdTerm/inventarioProd_formPlantilla.html')

def inventarioProd_delete(request, pk):
    salidas = get_object_or_404(inventarioProdTerm, pk=pk)
    salidasaux = inventarioProdTermAux.objects.filter(inventarioreg=salidas.registro)

    # Si tiene movimientos asociados, no se puede anular
    if salidasaux.exists():
        return render(request, 'plantaE/inventarioProdTerm/inventarioProd_confirm_delete.html', {
            'registros': salidas,
            'alert_message': "No se puede anular el registro porque tiene movimientos asociados.",
            'redirect_url': reverse('inventarioProd_list')
        })

    if request.method == 'POST':
        salidas.status = 'Anulado'
        salidas.status3 = 'Anulado'
        salidas.save()

        return render(request, 'plantaE/inventarioProdTerm/inventarioProd_confirm_delete.html', {
            'registros': salidas,
            'alert_message': "Registro anulado correctamente.",
            'redirect_url': reverse('inventarioProd_list')
        })

    return render(request, 'plantaE/inventarioProdTerm/inventarioProd_confirm_delete.html', {'registros': salidas})

def inventarioProd_update(request, pk):
    salidas = get_object_or_404(inventarioProdTerm, pk=pk)
    if request.method == 'POST':
        form = inventarioFrutaForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('inventarioProd_list')
    else:
        form = inventarioFrutaForm(instance=salidas)
        
    return render(request, 'plantaE/inventarioProdTerm/inventarioProd_form_edit.html', {'form': form})

def load_inventarioProdparam(request):
    cultivo_ = request.GET.get('campo1')
    categoria_ = request.GET.get('campo2')

    if cultivo_ != None and categoria_ != None:
        datos = productoTerm.objects.filter(cultivo=cultivo_,categoria=categoria_).values('itemsapcode','itemsapname')
    
    return JsonResponse({'datos': list(datos),'cultivo':cultivo_,'categoria':categoria_})

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

    return render(request, 'plantaE/inventarioProdTerm/inventarioProd_reporteInv.html', context)

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
    return render(request, 'plantaE/inventarioProdTerm/inventarioProd_inventariogeneralfruta.html', {'registros': registros_agrupados})

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
                'calidad1': salida.calidad1,
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
    for registro in registros_agrupados:
        try:
            producto = productoTerm.objects.get(itemsapcode=registro['itemsapcode'])
            cajasxtarima = producto.cajasxtarima
        except productoTerm.DoesNotExist:
            cajasxtarima = 0

        registro['cajasxtarima'] = cajasxtarima

        # (Opcional) calcular tarimas restantes
        if cajasxtarima > 0:
            registro['total_tarimas'] = registro['cajas_restantes'] / cajasxtarima
        else:
            registro['tarimas_restantes'] = 0
    registros_json = json.dumps(registros_agrupados, default=str)  # Usar default=str para evitar errores con objetos no serializables

    # Pasar los registros agrupados al renderizado de la plantilla
    return render(request, 'plantaE/inventarioProdTerm/inventarioProd_inventariogeneral.html', {'registros': registros_agrupados,'registros_json':registros_json})

