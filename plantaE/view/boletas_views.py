
import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from plantaE.models import (
    Boletas,
    inventarioProdTerm,
    detallerec,
    detallerecaux,
    AcumFruta,
    AcumFrutaaux,
    usuariosAppFruta
)

from plantaE.forms import boletasForm
'''
def boletas_list(request):
    #today = timezone.now().date()
    #salidas = Recepciones.objects.filter(fecha=today)
    salidas = Boletas.objects.filter(
    Q(status='') | Q(status__isnull=True),
    fecha__gte=datetime.date(2026, 1, 1)
    ).order_by('-boleta')
    #salidas = salidas.order_by('-boleta')
     
    return render(request, 'plantaE/boletas/boletas_list.html', {'registros': salidas})

def boletas_listproductor(request):

    salidas = Boletas.objects.exclude(status="Anulado")
    nombre_usuario = request.user.username
    datos = usuariosAppFruta.objects.filter(correo=nombre_usuario).values('finca', 'encargado')

    # Definir fecha límite: 31 de octubre de 2025
    fecha_limite = datetime.date(2025, 9, 30)

    if datos.exists():
        finca_usuario = datos[0]['finca']
        salidas = salidas.filter(
            finca=finca_usuario,
            fecha__gt=fecha_limite  # Filtra fechas posteriores a octubre
        ).order_by('-boleta')
    else:
        salidas = Boletas.objects.none()  # No hay datos del usuario

    return render(request, 'plantaE/boletas/boletas_list_productor.html', {'registros': salidas})

def boletas_update(request, pk):
    salidas = get_object_or_404(Boletas, pk=pk)
    if request.method == 'POST':
        form = boletasForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('boletasFruta_list')
        else:
            return JsonResponse({'errores': form.errors}, status=400)
    else:
        form = boletasForm(instance=salidas)
    return render(request, 'plantaE/boletas/boletas_form.html', {'form': form})

def boletas_detail(request, pk):
    salidas = get_object_or_404(Boletas, pk=pk)
    return render(request, 'plantaE/boletas/boletas_detail.html', {'registros': salidas})

def boletas_delete(request, pk):

    salidas = get_object_or_404(Boletas, pk=pk)

    if request.method == 'POST':

        with transaction.atomic():

            #  Anular boletas
            Boletas.objects.filter(
                boleta=salidas.boleta
            ).update(status='Anulado')

            # Liberar inventario
            inventarioProdTerm.objects.filter(
                boleta=salidas.boleta
            ).exclude(status='Anulado').update(
                status3=None,
                boleta=None
            )

            # Obtener recepciones relacionadas
            recepciones_ids = list(
                detallerecaux.objects.filter(
                    boleta=salidas.boleta
                ).exclude(status='Anulado')
                .values_list('recepcion', flat=True)
                .distinct()
            )

            # Reabrir recepciones
            if recepciones_ids:

                detallerec.objects.filter(
                    recepcion__in=recepciones_ids
                ).exclude(status='Anulado').update(status=None)

                detallerecaux.objects.filter(
                    recepcion__in=recepciones_ids
                ).exclude(status='Anulado').update(status='En proceso')

            # Anular detalle auxiliar
            detallerecaux.objects.filter(
                boleta=salidas.boleta
            ).exclude(status='Anulado').update(status='Anulado')

            # Obtener AcumFruta relacionados
            acumfruta_ids = list(
                AcumFrutaaux.objects.filter(
                    boleta=salidas.boleta
                ).exclude(status='Anulado')
                .values_list('acumfrutaid', flat=True)
                .distinct()
            )

            # Liberar fruta
            if acumfruta_ids:

                AcumFruta.objects.filter(
                    id__in=acumfruta_ids
                ).exclude(status='Anulado').update(status=None)

                AcumFrutaaux.objects.filter(
                    acumfrutaid__in=acumfruta_ids
                ).exclude(status='Anulado').update(status=None)

            # Anular auxiliar
            AcumFrutaaux.objects.filter(
                boleta=salidas.boleta
            ).exclude(status='Anulado').update(status='Anulado')

        messages.success(request, "Registro anulado correctamente.")
        return redirect('boletasFruta_list')

    return render(request, 'plantaE/boletas/boletas_confirm_delete.html', {'registros': salidas})

def boletas_devolver(request, pk):

    salidas = get_object_or_404(Boletas, pk=pk)

    if request.method == 'POST':

        with transaction.atomic():

            # Anular boletas relacionadas
            Boletas.objects.filter(
                boleta=salidas.boleta
            ).update(status='Anulado')

            # Marcar inventario como devuelto
            inventarioProdTerm.objects.filter(
                boleta=salidas.boleta
            ).exclude(status='Anulado').update(
                status3="Devuelto"
            )

            # Obtener recepciones relacionadas
            recepciones_ids = list(
                detallerecaux.objects.filter(
                    boleta=salidas.boleta
                ).exclude(status='Anulado')
                .values_list('recepcion', flat=True)
                .distinct()
            )

            # Reabrir recepciones
            if recepciones_ids:

                detallerec.objects.filter(
                    recepcion__in=recepciones_ids
                ).exclude(status='Anulado').update(status=None)

                detallerecaux.objects.filter(
                    recepcion__in=recepciones_ids
                ).exclude(status='Anulado').update(status='En proceso')

            # Anular detalle auxiliar
            detallerecaux.objects.filter(
                boleta=salidas.boleta
            ).exclude(status='Anulado').update(status='Anulado')

            # Obtener AcumFruta relacionados
            acumfruta_ids = list(
                AcumFrutaaux.objects.filter(
                    boleta=salidas.boleta
                ).exclude(status='Anulado')
                .values_list('acumfrutaid', flat=True)
                .distinct()
            )

            # Liberar fruta
            if acumfruta_ids:

                AcumFruta.objects.filter(
                    id__in=acumfruta_ids
                ).exclude(status='Anulado').update(status=None)

                AcumFrutaaux.objects.filter(
                    acumfrutaid__in=acumfruta_ids
                ).exclude(status='Anulado').update(status=None)

            # Anular auxiliares
            AcumFrutaaux.objects.filter(
                boleta=salidas.boleta
            ).exclude(status='Anulado').update(status='Anulado')

        messages.success(request, "Boleta devuelta correctamente.")
        return redirect('boletasFruta_list')

    return render(request, 'plantaE/boletas/boletas_confirm_devolver.html', {'registros': salidas})
'''
from django.views.generic import ListView, DetailView, UpdateView, View
from django.urls import reverse_lazy
import datetime

# --- Listado de Boletas ---
class BoletasListView(ListView):
    model = Boletas
    template_name = 'plantaE/boletas/boletas_list.html'
    context_object_name = 'registros'

    def get_queryset(self):
        return Boletas.objects.filter(status__isnull=True, fecha__gte=datetime.date(2026, 1, 1)).order_by('-boleta')

class BoletasListProductorView(ListView):
    model = Boletas
    template_name = 'plantaE/boletas/boletas_list_productor.html'
    context_object_name = 'registros'

    def get_queryset(self):
        salidas = Boletas.objects.all()
        nombre_usuario = self.request.user.username
        datos = usuariosAppFruta.objects.filter(correo=nombre_usuario).values('finca', 'encargado')
        fecha_limite = datetime.date(2025, 9, 30)
        if datos.exists():
            return salidas.filter(finca=datos[0]['finca'], fecha__gt=fecha_limite).order_by('-boleta')
        return Boletas.objects.none()


# --- Detalle de Boleta ---
class BoletasDetailView(DetailView):
    model = Boletas
    template_name = 'plantaE/boletas/boletas_detail.html'
    context_object_name = 'registros'


# --- Editar Boleta ---
class BoletasUpdateView(UpdateView):
    model = Boletas
    form_class = boletasForm
    template_name = 'plantaE/boletas/boletas_form.html'
    success_url = reverse_lazy('boletasFruta_list')


# --- Anulación de Boleta ---
class BoletasDeleteView(View):
    template_name = 'plantaE/boletas/boletas_confirm_delete.html'

    def get(self, request, pk):
        registro = get_object_or_404(Boletas, pk=pk)
        return render(request, self.template_name, {'registros': registro})

    def post(self, request, pk):
        registro = get_object_or_404(Boletas, pk=pk)
        with transaction.atomic():
            # Anular boletas
            Boletas.objects.filter(boleta=registro.boleta).update(status='Anulado')

            # Liberar inventario
            inventarioProdTerm.objects.filter(boleta=registro.boleta).exclude(status='Anulado').update(status3=None, boleta=None)

            # Reabrir recepciones
            recepciones_ids = list(detallerecaux.objects.filter(boleta=registro.boleta).exclude(status='Anulado').values_list('recepcion', flat=True).distinct())
            if recepciones_ids:
                detallerec.objects.filter(recepcion__in=recepciones_ids).exclude(status='Anulado').update(status=None)
                detallerecaux.objects.filter(recepcion__in=recepciones_ids).exclude(status='Anulado').update(status='En proceso')

            # Anular detalle auxiliar
            detallerecaux.objects.filter(boleta=registro.boleta).exclude(status='Anulado').update(status='Anulado')

            # Liberar AcumFruta
            acumfruta_ids = list(AcumFrutaaux.objects.filter(boleta=registro.boleta).exclude(status='Anulado').values_list('acumfrutaid', flat=True).distinct())
            if acumfruta_ids:
                AcumFruta.objects.filter(id__in=acumfruta_ids).exclude(status='Anulado').update(status=None)
                AcumFrutaaux.objects.filter(acumfrutaid__in=acumfruta_ids).exclude(status='Anulado').update(status=None)

            # Anular AcumFruta auxiliar
            AcumFrutaaux.objects.filter(boleta=registro.boleta).exclude(status='Anulado').update(status='Anulado')

        messages.success(request, "Registro anulado correctamente.")
        return redirect('boletasFruta_list')


# --- Devolver Boleta ---
class BoletasDevolverView(View):
    template_name = 'plantaE/boletas/boletas_confirm_devolver.html'

    def get(self, request, pk):
        registro = get_object_or_404(Boletas, pk=pk)
        return render(request, self.template_name, {'registros': registro})

    def post(self, request, pk):
        registro = get_object_or_404(Boletas, pk=pk)
        with transaction.atomic():
            # Marcar boletas como anuladas
            Boletas.objects.filter(boleta=registro.boleta).update(status='Anulado')

            # Marcar inventario como devuelto
            inventarioProdTerm.objects.filter(boleta=registro.boleta).exclude(status='Anulado').update(status3="Devuelto")

            # Reabrir recepciones
            recepciones_ids = list(detallerecaux.objects.filter(boleta=registro.boleta).exclude(status='Anulado').values_list('recepcion', flat=True).distinct())
            if recepciones_ids:
                detallerec.objects.filter(recepcion__in=recepciones_ids).exclude(status='Anulado').update(status=None)
                detallerecaux.objects.filter(recepcion__in=recepciones_ids).exclude(status='Anulado').update(status='En proceso')

            # Anular detalle auxiliar
            detallerecaux.objects.filter(boleta=registro.boleta).exclude(status='Anulado').update(status='Anulado')

            # Liberar AcumFruta
            acumfruta_ids = list(AcumFrutaaux.objects.filter(boleta=registro.boleta).exclude(status='Anulado').values_list('acumfrutaid', flat=True).distinct())
            if acumfruta_ids:
                AcumFruta.objects.filter(id__in=acumfruta_ids).exclude(status='Anulado').update(status=None)
                AcumFrutaaux.objects.filter(acumfrutaid__in=acumfruta_ids).exclude(status='Anulado').update(status=None)

            # Anular auxiliares
            AcumFrutaaux.objects.filter(boleta=registro.boleta).exclude(status='Anulado').update(status='Anulado')

        messages.success(request, "Boleta devuelta correctamente.")
        return redirect('boletasFruta_list')