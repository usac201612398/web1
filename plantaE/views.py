from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, redirect
from .models import salidasFruta
from .forms import salidasFrutaForm

def article_list(request):
    salidas = salidasFruta.objects.all()
    return render(request, 'salidasFruta/salidasFruta_list.html', {'registros': salidas})

def article_detail(request, pk):
    salidas = get_object_or_404(salidasFruta, pk=pk)
    return render(request, 'salidasFruta/salidasFruta_detail.html', {'registros': salidas})

def article_create(request):
    if request.method == 'POST':
        form = salidasFrutaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('salidasFruta_list')
    else:
        form =salidasFrutaForm()
    return render(request, 'salidasFruta/salidasFruta_form.html', {'form': form})

def article_update(request, pk):
    salidas = get_object_or_404(salidasFruta, pk=pk)
    if request.method == 'POST':
        form = salidasFrutaForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('salidasFruta_list')
    else:
        form = salidasFrutaForm(instance=salidas)
    return render(request, 'salidasFruta/salidasFruta_form.html', {'form': form})

def article_delete(request, pk):
    salidas = get_object_or_404(salidasFruta, pk=pk)
    if request.method == 'POST':
        salidas.delete()
        return redirect('salidasFruta_list')
    return render(request, 'salidasFruta/salidasFruta_confirm_delete.html', {'article': salidas})