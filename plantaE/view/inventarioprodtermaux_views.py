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

def inventarioProdAux_list(request):
    #salidas = Recepciones.objects.filter(fecha=today)
    today = timezone.localtime(timezone.now()).date()
        
    salidas = inventarioProdTerm.objects.exclude(status='Anulado').filter(
            fecha__year=today.year,
            fecha__month=today.month
        )
    return render(request, 'plantaE/inventarioProdTermAux/inventarioProdAux_list.html', {'registros': salidas})


def inventarioProdAux_delete(request, pk):
    salidas = get_object_or_404(inventarioProdTermAux, pk=pk)
    salidasaux = inventarioProdTerm.objects.filter(registro=salidas.inventarioreg)

    # Si tiene movimientos asociados, no se puede anular

    if request.method == 'POST':
        salidas.status = 'Anulado'
        salidas.status3 = 'Anulado'
        salidas.save()

        return render(request, 'plantaE/inventarioProdTermAux/inventarioProdAux_confirm_delete.html', {
            'registros': salidas,
            'alert_message': "Registro anulado correctamente.",
            'redirect_url': reverse('inventarioProdAux_list')
        })

    return render(request, 'plantaE/inventarioProdTermAux/inventarioProdAux_confirm_delete.html', {'registros': salidas})

def inventarioProdAux_update(request, pk):
    salidas = get_object_or_404(inventarioProdTerm, pk=pk)
    if request.method == 'POST':
        form = inventarioFrutaForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('inventarioProdAux_list')
    else:
        form = inventarioFrutaForm(instance=salidas)
        
    return render(request, 'plantaE/inventarioProdTermAux/inventarioProdAux_form_edit.html', {'form': form})
