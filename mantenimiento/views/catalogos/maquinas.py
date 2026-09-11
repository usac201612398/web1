from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib import messages

from ...models import Maquina
from ...forms import MaquinaForm


# ==========================================================
# LISTADO DE MAQUINAS
# ==========================================================

def maquinas_list(request):

    registros = Maquina.objects.all().order_by('registro')

    return render(
        request,
        'mantenimiento/crud/gestor/maquinas/maquinas_list.html',
        {
            'registros': registros
        }
    )


# ==========================================================
# CREAR MAQUINA
# ==========================================================

def maquinas_create(request):

    if request.method == 'POST':

        form = MaquinaForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Máquina creada correctamente."
            )

            return redirect('maquinas_list')

    else:

        form = MaquinaForm()


    return render(
        request,
        'mantenimiento/crud/gestor/maquinas/maquinas_form.html',
        {
            'form': form,
            'modo': 'crear'
        }
    )


# ==========================================================
# ACTUALIZAR MAQUINA
# ==========================================================

def maquinas_update(request, pk):

    registro = get_object_or_404(
        Maquina,
        pk=pk
    )


    if request.method == 'POST':

        form = MaquinaForm(
            request.POST,
            instance=registro
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Máquina actualizada correctamente."
            )

            return redirect('maquinas_list')

    else:

        form = MaquinaForm(
            instance=registro
        )


    return render(
        request,
        'mantenimiento/crud/gestor/maquinas/maquinas_form.html',
        {
            'form': form,
            'modo': 'actualizar',
            'registro': registro
        }
    )


# ==========================================================
# ANULAR MAQUINA
# ==========================================================

def maquinas_delete(request, pk):

    registro = get_object_or_404(
        Maquina,
        pk=pk
    )


    if request.method == 'POST':

        registro.status = 'Anulada'

        registro.save(
            update_fields=[
                'status',
                'updated_at'
            ]
        )

        messages.success(
            request,
            "Máquina anulada correctamente."
        )

        return redirect('maquinas_list')


    return render(
        request,
        'mantenimiento/crud/gestor/maquinas/maquinas_confirm_delete.html',
        {
            'registro': registro
        }
    )