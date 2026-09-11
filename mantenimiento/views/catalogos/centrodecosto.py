from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib import messages

from ...models import centrodecosto
from ...forms import centrodecostoForm

# ==========================================================
# LISTADO DE CENTROS DE COSTO
# ==========================================================

def centrodecosto_list(request):

    registros = centrodecosto.objects.all()

    return render(
        request,
        'mantenimiento/crud/gestor/centrodecosto/centrodecosto_list.html',
        {
            'registros': registros
        }
    )

# ==========================================================
# CREAR CENTROS DE COSTO
# ==========================================================

def centrodecosto_create(request):

    if request.method == 'POST':

        form = centrodecostoForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('centrodecosto_list')

    else:

        form = centrodecostoForm()

    return render(
        request,
        'mantenimiento/crud/gestor/centrodecosto/centrodecosto_form.html',
        {
            'form': form,
            'modo': 'crear'
        }
    )

# ==========================================================
# ACTUALIZAR CENTROS DE COSTO
# ==========================================================

def centrodecosto_update(request, pk):

    registro = get_object_or_404(
        centrodecosto,
        pk=pk
    )

    if request.method == 'POST':

        form = centrodecostoForm(
            request.POST,
            instance=registro
        )

        if form.is_valid():

            form.save()

            return redirect('centrodecosto_list')

    else:

        form = centrodecostoForm(
            instance=registro
        )

    return render(
        request,
        'mantenimiento/crud/gestor/centrodecosto/centrodecosto_form.html',
        {
            'form': form,
            'modo': 'actualizar'
        }
    )

# ==========================================================
# ANULAR CENTROS DE COSTO
# ==========================================================

def centrodecosto_delete(request, pk):

    registro = get_object_or_404(
        centrodecosto,
        pk=pk
    )

    if request.method == 'POST':

        registro.status = 'Anulado'

        registro.save()

        messages.success(
            request,
            "Centro de costo anulado correctamente."
        )

        return redirect('centrodecosto_list')

    return render(
        request,
        'mantenimiento/crud/gestor/centrodecosto/centrodecosto_confirm_delete.html',
        {
            'registros': registro
        }
    )