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

from plantaE.forms import inventarioFrutaAuxForm
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
    
    salidasaux = get_object_or_404(inventarioProdTermAux, pk=pk)

    # Registros relacionados en inventarioProdTerm
    salidas = inventarioProdTerm.objects.filter(registro=salidasaux.inventarioreg).exclude(status='Anulado')

    if request.method == 'POST':

        # 1. Anular el registro principal
        salidasaux.status = 'Anulado'
        salidasaux.status3 = 'Anulado'
        salidasaux.save()

        # 2. Verificar si alguno está en proceso
        if salidas.filter(status='En proceso').exists():

            # 3. Poner en NULL los que están en proceso
            salidas.filter(status='En proceso').update(status=None)

            # 4. También actualizar los auxiliares relacionados (excepto anulados)
            inventarioProdTermAux.objects.filter(
                inventarioreg=salidas.registro
            ).exclude(status='Anulado').update(status=None)

        return render(request, 'plantaE/inventarioProdTermAux/inventarioProdAux_confirm_delete.html', {
            'registros': salidas,
            'alert_message': "Registro anulado correctamente.",
            'redirect_url': reverse('inventarioProdAux_list')
        })

    return render(request, 'plantaE/inventarioProdTermAux/inventarioProdAux_confirm_delete.html', {
        'registros': salidas
    })

def inventarioProdAux_update(request, pk):
    salidas = get_object_or_404(inventarioProdTermAux, pk=pk)
    if request.method == 'POST':
        form = inventarioFrutaAuxForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('inventarioProdAux_list')
    else:
        form = inventarioFrutaAuxForm(instance=salidas)
        
    return render(request, 'plantaE/inventarioProdTermAux/inventarioProdAux_form_edit.html', {'form': form})
