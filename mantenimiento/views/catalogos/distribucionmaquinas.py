from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib import messages

from ...models import DistribucionMaquinas
from ...forms import distribucionMaquinasForm

# ==========================================================
# LISTA DE DISTRIBUCION DE MAQUINAS
# ==========================================================

def distribucionmaquinas_list(request):
    registros = DistribucionMaquinas.objects.select_related(
        'ubicacion',
        'maquina',
        'centrodecosto'
    ).all()

    return render(
        request,
        'mantenimiento/crud/gestor/distribuciones/distribuciones_list.html',
        {
            'registros': registros
        }
    )

# ==========================================================
# CREAR DISTRIBUCION DE MAQUINAS
# ==========================================================

def distribucionmaquinas_create(request):
    if request.method == 'POST':

        form = distribucionMaquinasForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Distribución de máquina creada correctamente."
            )

            return redirect('distribucionmaquinas_list')

    else:

        form = distribucionMaquinasForm()


    return render(
        request,
        'mantenimiento/crud/gestor/distribuciones/distribuciones_form.html',
        {
            'form': form,
            'modo': 'crear'
        }
    )

# ==========================================================
# ACTUALIZAR DISTRIBUCION DE MAQUINAS
# ==========================================================

def distribucionmaquinas_update(request, pk):
    registro = get_object_or_404(
        DistribucionMaquinas,
        pk=pk
    )


    if request.method == 'POST':

        form = distribucionMaquinasForm(
            request.POST,
            instance=registro
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Distribución de máquina actualizada correctamente."
            )

            return redirect('distribucionmaquinas_list')

    else:

        form = distribucionMaquinasForm(
            instance=registro
        )


    return render(
        request,
        'mantenimiento/crud/gestor/distribuciones/distribuciones_form.html',
        {
            'form': form,
            'modo': 'actualizar'
        }
    )

# ==========================================================
# ANULAR DISTRIBUCION DE MAQUINAS
# ==========================================================

def distribucionmaquinas_delete(request, pk):
    registro = get_object_or_404(
        DistribucionMaquinas,
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
            "Distribución de máquina anulada correctamente."
        )

        return redirect('distribucionmaquinas_list')


    return render(
        request,
        'mantenimiento/crud/gestor/distribuciones/distribuciones_confirm_delete.html',
        {
            'registros': registro
        }
    )