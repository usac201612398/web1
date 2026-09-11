from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib import messages

from ...models import Ubicacion
from ...forms import ubicacionesForm

# ==========================================================
# LISTADO DE UBICACIONES
# ==========================================================

def ubicaciones_list(request):

    registros = Ubicacion.objects.all()

    return render(
        request,
        'mantenimiento/crud/gestor/ubicaciones/ubicaciones_list.html',
        {'registros': registros}
    )

# ==========================================================
# CREAR UBICACIÓN
# ==========================================================

def ubicaciones_create(request):

    if request.method == 'POST':

        form = ubicacionesForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Ubicación creada correctamente.'
            )

            return redirect(
                'ubicaciones_list'
            )

    else:

        form = ubicacionesForm()

    return render(
        request,
        'mantenimiento/crud/gestor/ubicaciones/ubicaciones_form.html',
        {
            'form': form,
            'modo': 'crear'
        }
    )

# ==========================================================
# ACTUALIZAR UBICACIÓN
# ==========================================================

def ubicaciones_update(request, pk):

    registro = get_object_or_404(
        Ubicacion,
        pk=pk
    )

    if request.method == 'POST':

        form = ubicacionesForm(
            request.POST,
            instance=registro
        )

        if form.is_valid():

            form.save()

            return redirect(
                'ubicaciones_list'
            )

    else:

        form = ubicacionesForm(
            instance=registro
        )

    return render(
        request,
        'mantenimiento/crud/gestor/ubicaciones/ubicaciones_form.html',
        {
            'form': form,
            'modo': 'actualizar'
        }
    )

# ==========================================================
# ANULAR UBICACIÓN
# ==========================================================

def ubicaciones_delete(request, pk):

    registro = get_object_or_404(
        Ubicacion,
        pk=pk
    )

    if request.method == 'POST':

        registro.status = 'Anulada'
        registro.save()

        return redirect(
            'ubicaciones_list'
        )

    return render(
        request,
        'mantenimiento/crud/gestor/ubicaciones/ubicaciones_confirm_delete.html',
        {
            'registros': registro
        }
    )