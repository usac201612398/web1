from django.shortcuts import render
from .models import *
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from.forms import *
from django.contrib import messages

# Create your views here.
def lotes_list(request):
    today = timezone.localtime(timezone.now()).date()
    salidas = lotes.objects.filter(fecha=today, status__isnull=True)
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
