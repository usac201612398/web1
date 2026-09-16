from django.http import JsonResponse
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from ...forms import SolicitarOperacionForm
from ...models import (
    SolicitarOperacion,
    DistribucionMaquinas,
    ListaMantenimientos,
)

from django.contrib import messages
from django.utils import timezone

# ==========================================================
# CREAR SOLICITUD DE MANTENIMIENTO
# ==========================================================

def solicitar_mantenimiento_create(request):

    if request.method == 'POST':

        form = SolicitarOperacionForm(request.POST)

        if form.is_valid():

            solicitud = form.save(commit=False)

            solicitud.solicita = request.user
            solicitud.status = 'Activa'
            solicitud.solicitud = True

            solicitud.save()

            return redirect('solicitar_mantenimiento_list')

    else:

        form = SolicitarOperacionForm(
            initial={
                'fecha_solicitud': timezone.localdate()
            }
        )

    return render(
        request,
        'mantenimiento/crud/solicitud/solicitar_mantenimiento_form.html',
        {
            'form': form,
            'modo': 'crear',
        }
    )

# ==========================================================
# LISTADO DE SOLICITUDES DE MANTENIMINETO
# ==========================================================

def solicitar_mantenimiento_list(request):

    registros = SolicitarOperacion.objects.all()

    return render(
        request,
        'mantenimiento/crud/solicitud/solicitar_mantenimiento_list.html',
        {
            'registros': registros
        }
    )

# ==========================================================
# ACTUALIZAR SOLICITUD DE MANTENIMIENTO
# ==========================================================

def solicitar_mantenimiento_update(request, pk):

    registro = get_object_or_404(
        SolicitarOperacion,
        pk=pk
    )

    if request.method == 'POST':

        form = SolicitarOperacionForm(
            request.POST,
            instance=registro
        )

        if form.is_valid():

            form.save()

            return redirect('solicitar_mantenimiento_list')

    else:

        form = SolicitarOperacionForm(
            instance=registro
        )

    return render(
        request,
        'mantenimiento/crud/solicitud/solicitar_mantenimiento_form.html',
        {
            'form': form,
            'modo': 'actualizar'
        }
    )

# ==========================================================
# ANULAR SOLICITUD DE MANTENIMIENTO
# ==========================================================

def solicitar_mantenimiento_delete(request, pk):

    registro = get_object_or_404(
        SolicitarOperacion,
        pk=pk
    )

    if request.method == 'POST':

        registro.status = 'Anulada'

        registro.save()

        messages.success(
            request,
            "Solicitud anulada correctamente."
        )

        return redirect('solicitar_mantenimiento_list')

    return render(
        request,
        'mantenimiento/crud/solicitud/solicitar_mantenimiento_confirm_delete.html',
        {
            'registros': registro
        }
    )

def maquinas_por_ubicacion(request):

    ubicacion_id = request.GET.get('ubicacion')

    if not ubicacion_id:
        return JsonResponse(
            {
                'maquinas': []
            }
        )

    distribuciones = (
        DistribucionMaquinas.objects
        .filter(
            ubicacion_id=ubicacion_id,
            status='Activa'
        )
        .select_related('maquina')
        .order_by('maquina__nombre')
    )

    maquinas = []

    for distribucion in distribuciones:

        maquinas.append({
            'id': distribucion.maquina_id,
            'nombre': distribucion.maquina.nombre,
            'serie': distribucion.serie or '',
            'registro': distribucion.registro,
        })

    return JsonResponse({
        'maquinas': maquinas
    })

def mantenimientos_por_maquina(request):

    maquina_id = request.GET.get('maquina')

    if not maquina_id:
        return JsonResponse({
            'mantenimientos': []
        })

    mantenimientos = (
        ListaMantenimientos.objects
        .filter(
            maquina_id=maquina_id
        )
        .order_by('descripcion')
    )

    data = []

    for mantenimiento in mantenimientos:

        data.append({
            'id': mantenimiento.pk,
            'descripcion': mantenimiento.descripcion,
        })

    return JsonResponse({
        'mantenimientos': data
    })
