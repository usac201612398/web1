from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib import messages

from ...models import ListaMantenimientos
from ...forms import listaMantenimientosForm

# ==========================================================
# LISTADO DE MANTENIMIENTOS
# ==========================================================

def listamantenimientos_list(request):
    registros = ListaMantenimientos.objects.select_related(
        'maquina'
    ).all()

    return render(
        request,
        'mantenimiento/crud/gestor/listamantenimientos/listamantenimientos_list.html',
        {
            'registros': registros
        }
    )

# ==========================================================
# CREAR ELEMENTO PARA LISTA DE MANTENIMIENTO
# ==========================================================

def listamantenimientos_create(request):
    if request.method == 'POST':

        form = listaMantenimientosForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Mantenimiento creado correctamente."
            )

            return redirect('listamantenimientos_list')

    else:

        form = listaMantenimientosForm()


    return render(
        request,
        'mantenimiento/crud/gestor/listamantenimientos/listamantenimientos_form.html',
        {
            'form': form,
            'modo': 'crear'
        }
    )

# ==========================================================
# ACTUALIZAR ELEMENTO PARA LISTA DE MANTENIMIENTO
# ==========================================================

def listamantenimientos_update(request, pk):
    registro = get_object_or_404(
        ListaMantenimientos,
        pk=pk
    )


    if request.method == 'POST':

        form = listaMantenimientosForm(
            request.POST,
            instance=registro
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Mantenimiento actualizado correctamente."
            )

            return redirect('listamantenimientos_list')

    else:

        form = listaMantenimientosForm(
            instance=registro
        )


    return render(
        request,
        'mantenimiento/crud/gestor/listamantenimientos/listamantenimientos_form.html',
        {
            'form': form,
            'modo': 'actualizar'
        }
    )

# ==========================================================
# ANULAR ELEMENTO PARA LISTA DE MANTENIMIENTO
# ==========================================================

def listamantenimientos_delete(request, pk):
    registro = get_object_or_404(
        ListaMantenimientos,
        pk=pk
    )

    if request.method == 'POST':

        registro.status = 'Anulada'

        registro.save(
            update_fields=['status', 'updated_at']
        )

        messages.success(
            request,
            "Mantenimiento anulado correctamente."
        )

        return redirect('listamantenimientos_list')


    return render(
        request,
        'mantenimiento/crud/gestor/listamantenimientos/listamantenimientos_confirm_delete.html',
        {
            'registros': registro
        }
    )
