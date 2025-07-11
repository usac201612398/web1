from django.shortcuts import render
from .models import *
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from.forms import *
from django.contrib import messages

def sdcsemillashomepage(request):
    return render(request,'sdcsemillas/sdcsemillas_home.html')

# Create your views here.
def lotes_list(request):
    #today = timezone.localtime(timezone.now()).date()
    salidas = lotes.objects.filter( status__isnull=True)
    return render(request, 'sdcsemillas/lotes_list.html', {'registros': salidas})

def lotes_detail(request, pk):
    salidas = get_object_or_404(lotes, pk=pk)
    return render(request, 'sdcsemillas/lotes_detail.html', {'registros': salidas})

def  lotes_create(request):
    if request.method == 'POST':
        form = lotesForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                # Manejar excepciones específicas (por ejemplo, UniqueConstraintError)
                return JsonResponse({'error': str(e)}, status=400)
            return redirect('lotes_list')
        else:
             # Imprimir errores para depuración
            return JsonResponse({'errores': form.errors}, status=400)
    else:
        form = lotesForm()
    return render(request, 'sdcsemillas/lotes_form.html', {'form': form})

def lotes_update(request, pk):
    salidas = get_object_or_404(lotes, pk=pk)
    if request.method == 'POST':
        form = lotesForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('lotes_list')
    else:
        form = lotesForm(instance=salidas)
    return render(request, 'sdcsemillas/lotes_form.html', {'form': form})

def lotes_delete(request, pk):

    salidas = get_object_or_404(lotes, pk=pk)

    if request.method == 'POST':
        salidas.status = 'Anulado'
        salidas.save()
        messages.success(request, "Lote anulado correctamente.")
        return redirect('lotes_list')
    
    return render(request, 'sdcsemillas/lotes_confirm_delete.html', {'registros': salidas})

def lotes_detail(request, pk):
    salidas = get_object_or_404(lotes, pk=pk)
    return render(request, 'sdcsemillas/lotes_detail.html', {'registros': salidas})

def variedades_list(request):
    #today = timezone.localtime(timezone.now()).date()
    salidas = variedades.objects.filter( status__isnull=True)
    return render(request, 'sdcsemillas/variedades_list.html', {'registros': salidas})

def  variedades_create(request):
    if request.method == 'POST':
        form = variedadesForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                # Manejar excepciones específicas (por ejemplo, UniqueConstraintError)
                return JsonResponse({'error': str(e)}, status=400)
            return redirect('variedades_list')
        else:
             # Imprimir errores para depuración
            return JsonResponse({'errores': form.errors}, status=400)
    else:
        form = variedadesForm()
    return render(request, 'sdcsemillas/variedades_form.html', {'form': form})

def variedades_update(request, pk):
    salidas = get_object_or_404(variedades, pk=pk)
    if request.method == 'POST':
        form = variedadesForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('lotes_list')
    else:
        form = variedadesForm(instance=salidas)
    return render(request, 'sdcsemillas/variedades_form.html', {'form': form})

def variedades_delete(request, pk):

    salidas = get_object_or_404(variedades, pk=pk)

    if request.method == 'POST':
        salidas.status = 'Anulado'
        salidas.save()
        messages.success(request, "Variedad anulado correctamente.")
        return redirect('variedades_list')
    
    return render(request, 'sdcsemillas/variedades_confirm_delete.html', {'registros': salidas})

def variedades_detail(request, pk):
    salidas = get_object_or_404(variedades, pk=pk)
    return render(request, 'sdcsemillas/variedades_detail.html', {'registros': salidas})

def conteoplantas_list(request):
    #today = timezone.localtime(timezone.now()).date()
    salidas = conteoplantas.objects.filter( status__isnull=True)
    return render(request, 'sdcsemillas/conteoplantas_list.html', {'registros': salidas})

def  conteoplantas_create(request):
    if request.method == 'POST':
        form = conteoplantasForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                # Manejar excepciones específicas (por ejemplo, UniqueConstraintError)
                return JsonResponse({'error': str(e)}, status=400)
            return redirect('conteoplantas_list')
        else:
             # Imprimir errores para depuración
            return JsonResponse({'errores': form.errors}, status=400)
    else:
        form = conteoplantasForm()
    return render(request, 'sdcsemillas/conteoplantas_form.html', {'form': form})

def conteoplantas_update(request, pk):
    salidas = get_object_or_404(conteoplantas, pk=pk)
    if request.method == 'POST':
        form = conteoplantasForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('conteoplantas_list')
    else:
        form = conteoplantasForm(instance=salidas)
    return render(request, 'sdcsemillas/conteoplantas_form.html', {'form': form})

def conteoplantas_delete(request, pk):

    salidas = get_object_or_404(conteoplantas, pk=pk)

    if request.method == 'POST':
        salidas.status = 'Anulado'
        salidas.save()
        messages.success(request, "Variedad anulado correctamente.")
        return redirect('conteoplantas_list')
    
    return render(request, 'sdcsemillas/conteoplantas_confirm_delete.html', {'registros': salidas})

def conteoplantas_detail(request, pk):
    salidas = get_object_or_404(conteoplantas, pk=pk)
    return render(request, 'sdcsemillas/conteoplantas_detail.html', {'registros': salidas})


def conteosemillas_list(request):
    #today = timezone.localtime(timezone.now()).date()
    salidas = conteosemillas.objects.filter( status__isnull=True)
    return render(request, 'sdcsemillas/conteosemillas_list.html', {'registros': salidas})

def conteosemillas_create(request):
    if request.method == 'POST':
        form = conteosemillasForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                # Manejar excepciones específicas (por ejemplo, UniqueConstraintError)
                return JsonResponse({'error': str(e)}, status=400)
            return redirect('conteosemillas_list')
        else:
             # Imprimir errores para depuración
            return JsonResponse({'errores': form.errors}, status=400)
    else:
        form = conteosemillasForm()
    return render(request, 'sdcsemillas/conteosemillas_form.html', {'form': form})

def conteosemillas_update(request, pk):
    salidas = get_object_or_404(conteosemillas, pk=pk)
    if request.method == 'POST':
        form = conteosemillasForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('conteosemillas_list')
    else:
        form = conteosemillasForm(instance=salidas)
    return render(request, 'sdcsemillas/conteosemillas_form.html', {'form': form})

def conteosemillas_delete(request, pk):

    salidas = get_object_or_404(conteosemillas, pk=pk)

    if request.method == 'POST':
        salidas.status = 'Anulado'
        salidas.save()
        messages.success(request, "Conteo anulado correctamente.")
        return redirect('conteosemillas_list')
    
    return render(request, 'sdcsemillas/conteosemillas_confirm_delete.html', {'registros': salidas})

def conteosemillas_detail(request, pk):
    salidas = get_object_or_404(conteosemillas, pk=pk)
    return render(request, 'sdcsemillas/conteosemillas_detail.html', {'registros': salidas})

def conteofrutos_list(request):
    #today = timezone.localtime(timezone.now()).date()
    salidas = conteofrutos.objects.filter( status__isnull=True)
    return render(request, 'sdcsemillas/conteofrutos_list.html', {'registros': salidas})

def conteofrutos_create(request):
    if request.method == 'POST':
        form = conteofrutosForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                # Manejar excepciones específicas (por ejemplo, UniqueConstraintError)
                return JsonResponse({'error': str(e)}, status=400)
            return redirect('conteofrutos_list')
        else:
             # Imprimir errores para depuración
            return JsonResponse({'errores': form.errors}, status=400)
    else:
        form = conteofrutosForm()
    return render(request, 'sdcsemillas/conteofrutos_form.html', {'form': form})

def conteofrutos_update(request, pk):
    salidas = get_object_or_404(conteofrutos, pk=pk)
    if request.method == 'POST':
        form = conteofrutosForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('conteofrutos_list')
    else:
        form = conteofrutosForm(instance=salidas)
    return render(request, 'sdcsemillas/conteofrutos_form.html', {'form': form})

def conteofrutos_delete(request, pk):

    salidas = get_object_or_404(conteofrutos, pk=pk)

    if request.method == 'POST':
        salidas.status = 'Anulado'
        salidas.save()
        messages.success(request, "Conteo anulado correctamente.")
        return redirect('conteofrutos_list')
    
    return render(request, 'sdcsemillas/conteofrutos_confirm_delete.html', {'registros': salidas})

def conteofrutos_detail(request, pk):
    salidas = get_object_or_404(conteofrutos, pk=pk)
    return render(request, 'sdcsemillas/conteofrutos_detail.html', {'registros': salidas})

def etapasdelote_list(request):
    #today = timezone.localtime(timezone.now()).date()
    salidas = etapasdelote.objects.filter( status__isnull=True)
    return render(request, 'sdcsemillas/etapasdelote_list.html', {'registros': salidas})

def etapasdelote_create(request):
    if request.method == 'POST':
        form = etapasdeloteForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                # Manejar excepciones específicas (por ejemplo, UniqueConstraintError)
                return JsonResponse({'error': str(e)}, status=400)
            return redirect('etapasdelote_list')
        else:
             # Imprimir errores para depuración
            return JsonResponse({'errores': form.errors}, status=400)
    else:
        form = etapasdeloteForm()
    return render(request, 'sdcsemillas/etapasdelote_form.html', {'form': form})

def etapasdelote_update(request, pk):
    salidas = get_object_or_404(etapasdelote, pk=pk)
    if request.method == 'POST':
        form = etapasdeloteForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('etapasdelote_list')
    else:
        form = etapasdeloteForm(instance=salidas)
    return render(request, 'sdcsemillas/etapasdelote_form.html', {'form': form})

def etapasdelote_delete(request, pk):

    salidas = get_object_or_404(etapasdelote, pk=pk)

    if request.method == 'POST':
        salidas.status = 'Anulado'
        salidas.save()
        messages.success(request, "Etapa anulada correctamente.")
        return redirect('etapasdelote_list')
    
    return render(request, 'sdcsemillas/etapasdelote_confirm_delete.html', {'registros': salidas})

def etapasdelote_detail(request, pk):
    salidas = get_object_or_404(etapasdelote, pk=pk)
    return render(request, 'sdcsemillas/etapasdelote_detail.html', {'registros': salidas})


def ccalidadpolen_list(request):
    #today = timezone.localtime(timezone.now()).date()
    salidas = ccalidadpolen.objects.filter( status__isnull=True)
    return render(request, 'sdcsemillas/ccalidadpolen_list.html', {'registros': salidas})

def ccalidadpolen_create(request):
    if request.method == 'POST':
        form = ccalidadpolenForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                # Manejar excepciones específicas (por ejemplo, UniqueConstraintError)
                return JsonResponse({'error': str(e)}, status=400)
            return redirect('ccalidadpolen_list')
        else:
             # Imprimir errores para depuración
            return JsonResponse({'errores': form.errors}, status=400)
    else:
        form = ccalidadpolenForm()
    return render(request, 'sdcsemillas/ccalidadpolen_form.html', {'form': form})

def ccalidadpolen_update(request, pk):
    salidas = get_object_or_404(ccalidadpolen, pk=pk)
    if request.method == 'POST':
        form = ccalidadpolenForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('ccalidadpolen_list')
    else:
        form = ccalidadpolenForm(instance=salidas)
    return render(request, 'sdcsemillas/ccalidadpolen_form.html', {'form': form})

def ccalidadpolen_delete(request, pk):

    salidas = get_object_or_404(ccalidadpolen, pk=pk)

    if request.method == 'POST':
        salidas.status = 'Anulado'
        salidas.save()
        messages.success(request, "Control anulado correctamente.")
        return redirect('ccalidadpolen_list')
    
    return render(request, 'sdcsemillas/ccalidadpolen_confirm_delete.html', {'registros': salidas})

def ccalidadpolen_detail(request, pk):
    salidas = get_object_or_404(ccalidadpolen, pk=pk)
    return render(request, 'sdcsemillas/ccalidadpolen_detail.html', {'registros': salidas})

def indexpolinizacion_list(request):
    #today = timezone.localtime(timezone.now()).date()
    salidas = indexpolinizacion.objects.filter( status__isnull=True)
    return render(request, 'sdcsemillas/indexpolinizacion_list.html', {'registros': salidas})

def indexpolinizacion_create(request):
    if request.method == 'POST':
        form = indexpolinizacionForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                # Manejar excepciones específicas (por ejemplo, UniqueConstraintError)
                return JsonResponse({'error': str(e)}, status=400)
            return redirect('indexpolinizacion_list')
        else:
             # Imprimir errores para depuración
            return JsonResponse({'errores': form.errors}, status=400)
    else:
        form = indexpolinizacionForm()
    return render(request, 'sdcsemillas/indexpolinizacion_form.html', {'form': form})

def indexpolinizacion_update(request, pk):
    salidas = get_object_or_404(indexpolinizacion, pk=pk)
    if request.method == 'POST':
        form = indexpolinizacionForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('indexpolinizacion_list')
    else:
        form = indexpolinizacionForm(instance=salidas)
    return render(request, 'sdcsemillas/indexpolinizacion_form.html', {'form': form})

def indexpolinizacion_delete(request, pk):

    salidas = get_object_or_404(indexpolinizacion, pk=pk)

    if request.method == 'POST':
        salidas.status = 'Anulado'
        salidas.save()
        messages.success(request, "Index anulado correctamente.")
        return redirect('indexpolinizacion_list')
    
    return render(request, 'sdcsemillas/indexpolinizacion_confirm_delete.html', {'registros': salidas})

def indexpolinizacion_detail(request, pk):
    salidas = get_object_or_404(indexpolinizacion, pk=pk)
    return render(request, 'sdcsemillas/indexpolinizacion_detail.html', {'registros': salidas})


def conteoflores_list(request):
    #today = timezone.localtime(timezone.now()).date()
    salidas = floresabiertas.objects.filter( status__isnull=True)
    return render(request, 'sdcsemillas/conteoflores_list.html', {'registros': salidas})

def conteoflores_create(request):
    if request.method == 'POST':
        form = conteofloresForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                # Manejar excepciones específicas (por ejemplo, UniqueConstraintError)
                return JsonResponse({'error': str(e)}, status=400)
            return redirect('conteoflores_list')
        else:
             # Imprimir errores para depuración
            return JsonResponse({'errores': form.errors}, status=400)
    else:
        form = indexpolinizacionForm()
    return render(request, 'sdcsemillas/conteoflores_form.html', {'form': form})

def conteoflores_update(request, pk):
    salidas = get_object_or_404(floresabiertas, pk=pk)
    if request.method == 'POST':
        form = conteofloresForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('conteoflores_list')
    else:
        form = conteofloresForm(instance=salidas)
    return render(request, 'sdcsemillas/conteoflores_form.html', {'form': form})

def conteoflores_delete(request, pk):

    salidas = get_object_or_404(floresabiertas, pk=pk)

    if request.method == 'POST':
        salidas.status = 'Anulado'
        salidas.save()
        messages.success(request, "Conteo anulada correctamente.")
        return redirect('conteoflores_list')
    
    return render(request, 'sdcsemillas/conteoflores_confirm_delete.html', {'registros': salidas})

def conteoflores_detail(request, pk):
    salidas = get_object_or_404(floresabiertas, pk=pk)
    return render(request, 'sdcsemillas/conteoflores_detail.html', {'registros': salidas})

def controlcosecha_list(request):
    #today = timezone.localtime(timezone.now()).date()
    salidas = controlcosecha.objects.filter( status__isnull=True)
    return render(request, 'sdcsemillas/controlcosecha_list.html', {'registros': salidas})

def controlcosecha_create(request):
    if request.method == 'POST':
        form = controlcosechaForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                # Manejar excepciones específicas (por ejemplo, UniqueConstraintError)
                return JsonResponse({'error': str(e)}, status=400)
            return redirect('controlcosecha_list')
        else:
             # Imprimir errores para depuración
            return JsonResponse({'errores': form.errors}, status=400)
    else:
        form = controlcosechaForm()
    return render(request, 'sdcsemillas/conteocosecha_form.html', {'form': form})

def controlcosecha_update(request, pk):
    salidas = get_object_or_404(controlcosecha, pk=pk)
    if request.method == 'POST':
        form = controlcosechaForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('controlcosecHa_list')
    else:
        form = controlcosechaForm(instance=salidas)
    return render(request, 'sdcsemillas/controlcosecha_list.html', {'form': form})

def controlcosecha_delete(request, pk):

    salidas = get_object_or_404(controlcosecha, pk=pk)

    if request.method == 'POST':
        salidas.status = 'Anulado'
        salidas.save()
        messages.success(request, "Control anulado correctamente.")
        return redirect('controlcosecha_list')
    
    return render(request, 'sdcsemillas/controlcosecha_confirm_delete.html', {'registros': salidas})

def controlcosecha_detail(request, pk):
    salidas = get_object_or_404(controlcosecha, pk=pk)
    return render(request, 'sdcsemillas/controlcosecha_detail.html', {'registros': salidas})