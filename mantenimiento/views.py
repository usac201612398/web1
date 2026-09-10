from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView,
)
from .models import *
from .forms import *
def index(request):
    return render(request, 'mantenimiento/home.html')

def ubicaciones_list(request):
    #today = timezone.localtime(timezone.now()).date()
    salidas = Ubicacion.objects.all()
    return render(request, 'mantenimiento/crud/gestor/ubicaciones/ubicaciones_list.html', {'registros': salidas})

def  ubicaciones_create(request):
    if request.method == 'POST':
        form = ubicacionesForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                # Manejar excepciones específicas (por ejemplo, UniqueConstraintError)
                return JsonResponse({'error': str(e)}, status=400)
            return redirect('ubicaciones_list')
        else:
             # Imprimir errores para depuración
            return JsonResponse({'errores': form.errors}, status=400)
    else:
        form = ubicacionesForm()
    return render(request, 'mantenimiento/crud/gestor/ubicaciones/ubicaciones_form.html', {'form': form,'modo':'crear'})

def ubicaciones_update(request, pk):
    salidas = get_object_or_404(Ubicacion, pk=pk)
    if request.method == 'POST':
        form = ubicacionesForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('ubicaciones_list')
    else:
        form = ubicacionesForm(instance=salidas)
    return render(request, 'mantenimiento/crud/gestor/ubicaciones/ubicaciones_form.html', {'form': form,'modo':'actualizar'})

def ubicaciones_delete(request, pk):

    salidas = get_object_or_404(Ubicacion, pk=pk)

    if request.method == 'POST':
        salidas.status = 'Anulada'
        salidas.save()
        messages.success(request, "Ubicación anulado correctamente.")
        return redirect('ubicaciones_list')
    
    return render(request, 'mantenimiento/crud/gestor/ubicaciones/ubicaciones_confirm_delete.html', {'registros': salidas})