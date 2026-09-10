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

def centrodecosto_list(request):

    registros = centrodecosto.objects.all()

    return render(
        request,
        'mantenimiento/crud/gestor/centrodecosto/centrodecosto_list.html',
        {
            'registros': registros
        }
    )


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


def personal_list(request):

    registros = Usuarios.objects.all()

    return render(
        request,
        'mantenimiento/crud/gestor/personal/personal_list.html',
        {
            'registros': registros
        }
    )


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

def distribucionmaquinas_list(request):
    registros = DistribucionMaquinas.objects.select_related(
        'ubicacion',
        'maquina',
        'centrodecosto'
    ).all()

    return render(
        request,
        'mantenimiento/crud/gestor/distribucionmaquinas/distribucionmaquinas_list.html',
        {
            'registros': registros
        }
    )

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
        'mantenimiento/crud/gestor/distribucionmaquinas/distribucionmaquinas_form.html',
        {
            'form': form,
            'modo': 'crear'
        }
    )

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
        'mantenimiento/crud/gestor/distribucionmaquinas/distribucionmaquinas_form.html',
        {
            'form': form,
            'modo': 'actualizar'
        }
    )

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
        'mantenimiento/crud/gestor/distribucionmaquinas/distribucionmaquinas_confirm_delete.html',
        {
            'registros': registro
        }
    )
