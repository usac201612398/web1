from django.shortcuts import render
from django.http import JsonResponse
import logging
# Create your views here.
from django.shortcuts import get_object_or_404, redirect
from .models import salidasFruta, usuariosAppFruta, datosProduccion, detallesProduccion, detallesEstructuras, Recepciones, Ccalidad,causasRechazo
from .forms import salidasFrutaForm, recepcionesForm, ccalidadForm
from django.db.models import Sum

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
    salidas = Recepciones.objects.all()
    return render(request, 'plantaE/recepciones_list.html', {'registros': salidas})

def recepciones_detail(request, pk):
    salidas = get_object_or_404(Recepciones, pk=pk)
    return render(request, 'plantaE/recepciones_detail.html', {'registros': salidas})

def recepciones_update(request, pk):
    salidas = get_object_or_404(Recepciones, pk=pk)
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
        return JsonResponse({'datos': salidas})
    return render(request, 'plantaE/ccalidad_form_edit.html', {'form': form})

def ccalidad_delete(request, pk):
    salidas = get_object_or_404(Ccalidad, pk=pk)
    if request.method == 'POST':
        salidas.delete()
        return redirect('ccalidad_list')
    return render(request, 'plantaE/ccalidad_confirm_delete.html', {'registros': salidas})

def obtener_llave_recepcion(request):
    # Obtén el nombre de usuario del usuario autenticado
    llave_recepcion = Recepciones.objects.values('criterio').distinct('criterio')
    causa_rechazo = causasRechazo.objects.all().values('causa')
    return JsonResponse({'llaves': list(llave_recepcion),'causa':list(causa_rechazo)})

def load_ccalidadparam(request):
    llave_recepcion = request.GET.get('category_id')
    datos = Recepciones.objects.filter(criterio=llave_recepcion).values('recepcion').distinct('recepcion')
    valor = Ccalidad.objects.filter(llave=llave_recepcion).aggregate(suma=Sum('porcentaje'))['suma']
    if valor != None:
        valor = 1-float(Ccalidad.objects.filter(llave=llave_recepcion).aggregate(suma=Sum('porcentaje'))['suma'])
    else:
        valor=1
    return JsonResponse({'datos': list(datos),'valor':valor})