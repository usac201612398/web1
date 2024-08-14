from django.shortcuts import render
from django.http import JsonResponse
import logging
# Create your views here.
from django.shortcuts import get_object_or_404, redirect
from .models import salidasFruta, usuariosAppFruta, datosProduccion, detallesProduccion, detallesEstructuras
from .forms import salidasFrutaForm

def obtener_nombre_usuario(request):
    # Obtén el nombre de usuario del usuario autenticado
    nombre_usuario = request.user.username
    return JsonResponse({'username': nombre_usuario})

def load_dataUsuario(request):
    correo_id = request.GET.get('category_id')
    datos = usuariosAppFruta.objects.filter(correo=correo_id).values('finca', 'encargado')
    adicionales = datosProduccion.objects.filter(finca=list(datos)[0]['finca'],status="Abierta").values('orden')
    return JsonResponse({'datos': list(datos),'correo':correo_id,'adicionales':list(adicionales)})

def load_dataUsuario2(request):
    ordenSelect = request.GET.get('category_id')
    cultivo= datosProduccion.objects.filter(orden=ordenSelect,status="Abierta").values('cultivo')
    variedad = detallesProduccion.objects.filter(cultivo=list(cultivo)[0]['cultivo']).values('variedad')
    estructura = detallesEstructuras.objects.filter(orden=ordenSelect).values('estructura')
    return JsonResponse({'datos': list(cultivo),'variedad':list(variedad),'estructura':list(estructura),'orden':ordenSelect})

def article_list(request):
    salidas = salidasFruta.objects.all()
    return render(request, 'plantaE/salidasFruta_list.html', {'registros': salidas})

def article_detail(request, pk):
    salidas = get_object_or_404(salidasFruta, pk=pk)
    return render(request, 'plantaE/salidasFruta_detail.html', {'registros': salidas})

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

def recepciones_list(request):
    salidas = salidasFruta.objects.all()
    return render(request, 'plantaE/recepcionesFruta_list.html', {'registros': salidas})

def recepciones_detail(request, pk):
    salidas = get_object_or_404(salidasFruta, pk=pk)
    return render(request, 'plantaE/recepcionesFruta_detail.html', {'registros': salidas})

def  recepciones_update(request, pk):
    salidas = get_object_or_404(salidasFruta, pk=pk)
    if request.method == 'POST':
        form = salidasFrutaForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('recepcionesFruta_list')
    else:
        form = salidasFrutaForm(instance=salidas)
    return render(request, 'plantaE/recepcionesFruta_form.html', {'form': form})