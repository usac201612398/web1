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

def inventarioProd_list(request):
    today = timezone.localtime(timezone.now()).date()
    #salidas = Recepciones.objects.filter(fecha=today)
    salidas = inventarioProdTerm.objects.filter(fecha=today,categoria="Exportación").exclude(status='Anulado')
    return render(request, 'plantaE/inventarioprodterm/inventarioProd_list.html', {'registros': salidas})

def inventarioProd_detail(request, pk):
    salidas = get_object_or_404(inventarioProdTerm, pk=pk)
    return render(request, 'plantaE/inventarioprodterm/inventarioProd_detail.html', {'registros': salidas})

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
    return render(request, 'plantaE/inventarioprodterm/inventarioProd_formPlantilla.html')

def inventarioProd_delete(request, pk):
    salidas = get_object_or_404(inventarioProdTerm, pk=pk)
    salidasaux = inventarioProdTermAux.objects.filter(inventarioreg=salidas.registro)

    # Si tiene movimientos asociados, no se puede anular
    if salidasaux.exists():
        return render(request, 'plantaE/inventarioprodterm/inventarioProd_confirm_delete.html', {
            'registros': salidas,
            'alert_message': "No se puede anular el registro porque tiene movimientos asociados.",
            'redirect_url': reverse('inventarioProd_list')
        })

    if request.method == 'POST':
        salidas.status = 'Anulado'
        salidas.status3 = 'Anulado'
        salidas.save()

        return render(request, 'plantaE/inventarioprodterm/inventarioProd_confirm_delete.html', {
            'registros': salidas,
            'alert_message': "Registro anulado correctamente.",
            'redirect_url': reverse('inventarioProd_list')
        })

    return render(request, 'plantaE/inventarioprodterm/inventarioProd_confirm_delete.html', {'registros': salidas})

def inventarioProd_update(request, pk):
    salidas = get_object_or_404(inventarioProdTerm, pk=pk)
    if request.method == 'POST':
        form = inventarioFrutaForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('inventarioProd_list')
    else:
        form = inventarioFrutaForm(instance=salidas)
        
    return render(request, 'plantaE/inventarioprodterm/inventarioProd_form_edit.html', {'form': form})

def load_inventarioProdparam(request):
    cultivo_ = request.GET.get('campo1')
    categoria_ = request.GET.get('campo2')

    if cultivo_ != None and categoria_ != None:
        datos = productoTerm.objects.filter(cultivo=cultivo_,categoria=categoria_).values('itemsapcode','itemsapname')
    
    return JsonResponse({'datos': list(datos),'cultivo':cultivo_,'categoria':categoria_})
