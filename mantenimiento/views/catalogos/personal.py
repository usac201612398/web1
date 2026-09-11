from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib import messages

from ...models import Usuarios
from ...forms import personalForm


# ==========================================================
# LISTADO DE USUARIOS
# ==========================================================

def personal_list(request):

    registros = Usuarios.objects.all()

    return render(
        request,
        'mantenimiento/crud/gestor/personal/personal_list.html',
        {
            'registros': registros
        }
    )

# ==========================================================
# CREAR USUARIOS
# ==========================================================

def personal_create(request):

    if request.method == 'POST':

        form = personalForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Personal registrado correctamente."
            )

            return redirect('personal_list')

    else:

        form = personalForm()

    return render(
        request,
        'mantenimiento/crud/gestor/personal/personal_form.html',
        {
            'form': form,
            'modo': 'crear'
        }
    )

# ==========================================================
# ACTUALIZAR USUARIOS
# ==========================================================

def personal_update(request, pk):

    registro = get_object_or_404(
        Usuarios,
        pk=pk
    )

    if request.method == 'POST':

        form = personalForm(
            request.POST,
            instance=registro
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Personal actualizado correctamente."
            )

            return redirect('personal_list')

    else:

        form = personalForm(
            instance=registro
        )

    return render(
        request,
        'mantenimiento/crud/gestor/personal/personal_form.html',
        {
            'form': form,
            'modo': 'actualizar'
        }
    )

# ==========================================================
# ANULAR USUARIOS
# ==========================================================

def personal_delete(request, pk):

    registro = get_object_or_404(
        Usuarios,
        pk=pk
    )

    if request.method == 'POST':

        registro.status = 'Anulado'

        registro.save()

        messages.success(
            request,
            "Personal anulado correctamente."
        )

        return redirect('personal_list')

    return render(
        request,
        'mantenimiento/crud/gestor/personal/personal_confirm_delete.html',
        {
            'registros': registro
        }
    )