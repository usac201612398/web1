from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.db import transaction
from django.utils import timezone
from django.views.generic import ListView, UpdateView, DetailView

# modelos
from plantaE.models import detallerec, detallerecaux, Actpeso, Recepciones, AcumFruta, salidasFruta

# formularios
from plantaE.forms import recepcionesForm
from django.views import View

class RecepcionesListView(ListView):
    model = detallerec
    template_name = 'plantaE/recepciones/recepciones_list.html'
    context_object_name = 'registros'

    def get_queryset(self):
        today = timezone.localtime(timezone.now()).date()
        return detallerec.objects.filter(
            fecha__year=today.year,
            fecha__month=today.month
        ).exclude(status="Anulado").order_by('-recepcion')

class RecepcionesDetailView(DetailView):
    model = detallerec
    template_name = 'plantaE/recepciones/recepciones_detail.html'
    context_object_name = 'registros'

class RecepcionesUpdateView(UpdateView):
    model = detallerec
    form_class = recepcionesForm
    template_name = 'plantaE/recepciones/recepciones_form.html'
    success_url = reverse_lazy('recepcionesFruta_list')

class RecepcionesFrutaDeleteView(View):

    template_name = 'plantaE/recepciones/recepciones_confirm_delete.html'

    def get(self, request, pk):
        salidas = get_object_or_404(detallerec, pk=pk)
        return render(request, self.template_name, {'registros': salidas})

    def post(self, request, pk):

        salidas = get_object_or_404(detallerec, pk=pk)

        # verificar si hay registros en boletas
        existe_en_aux = detallerecaux.objects.filter(
            recepcion=salidas.recepcion
        ).exclude(status="Anulado").exists()

        if existe_en_aux:
            return render(request, self.template_name, {
                'registros': salidas,
                'alert_message': "No se puede anular esta recepción porque tiene registros relacionados en boletas.",
                'redirect_url': reverse('recepcionesFruta_list')
            })

        with transaction.atomic():

            salidas.status = 'Anulado'
            salidas.save()

            Actpeso.objects.filter(
                recepcion=salidas.recepcion
            ).exclude(status='Anulado').update(status='Anulado')

            Recepciones.objects.filter(
                recepcion=salidas.recepcion
            ).exclude(status='Anulado').update(status='Anulado')

            AcumFruta.objects.filter(
                recepcion=salidas.recepcion
            ).exclude(status='Anulado').update(
                libras=None,
                recepcion=None,
                viaje=None,
                nsalidafruta=None
            )

            salidasFruta.objects.filter(
                recepcion=salidas.recepcion
            ).exclude(status='Anulado').update(
                libras=None,
                recepcion=None,
                status=None
            )

        return render(request, self.template_name, {
            'registros': salidas,
            'alert_message': "Registro anulado correctamente.",
            'redirect_url': reverse('recepcionesFruta_list')
        })
'''
def recepciones_list(request):

    today = timezone.localtime(timezone.now()).date()
    current_month = today.month
    current_year = today.year
    salidas= detallerec.objects.filter(fecha__year=current_year,fecha__month=current_month).order_by('-recepcion').exclude(status="Anulado")
    
    return render(request, 'plantaE/recepciones_list.html', {'registros': salidas})

def recepcionesFruta_delete(request, pk):

    salidas = get_object_or_404(detallerec, pk=pk)

    # Verificar si existen registros en detallerecaux con la misma recepción
    existe_en_aux = detallerecaux.objects.filter(recepcion=salidas.recepcion).exclude(status="Anulado").exists()

    if existe_en_aux:
        return render(request, 'plantaE/recepciones_confirm_delete.html', {
            'registros': salidas,
            'alert_message': "No se puede anular esta recepción porque tiene registros relacionados en boletas.",
            'redirect_url': reverse('recepcionesFruta_list')
        })

    if request.method == 'POST':
        # Anular detallerec
        with transaction.atomic():

            salidas.status = 'Anulado'
            salidas.save()

            # Anular Actpeso y Recepciones
            Actpeso.objects.filter(recepcion=salidas.recepcion).exclude(status='Anulado').update(status='Anulado')
            Recepciones.objects.filter(recepcion=salidas.recepcion).exclude(status='Anulado').update(status='Anulado')

            # Limpiar campos en AcumFruta y salidasFruta
            AcumFruta.objects.filter(recepcion=salidas.recepcion).exclude(status='Anulado').update(
                libras=None,
                recepcion=None,
                viaje=None,
                nsalidafruta=None
            )
            salidasFruta.objects.filter(recepcion=salidas.recepcion).exclude(status='Anulado').update(
                libras=None,
                recepcion=None,
                status=None
            )

        return render(request, 'plantaE/recepciones_confirm_delete.html', {
            'registros': salidas,
            'alert_message': "Registro anulado correctamente.",
            'redirect_url': reverse('recepcionesFruta_list')
        })

    return render(request, 'plantaE/recepciones_confirm_delete.html', {'registros': salidas})

def recepciones_detail(request, pk):
    salidas = get_object_or_404(detallerec, pk=pk)

    return render(request, 'plantaE/recepciones_detail.html', {'registros': salidas})

def recepciones_update(request, pk):
    salidas = get_object_or_404(detallerec, pk=pk)
    if request.method == 'POST':
        form = recepcionesForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('recepcionesFruta_list')
        else:
            return JsonResponse({'errores': form.errors}, status=400)
    else:
        form = recepcionesForm(instance=salidas)
    return render(request, 'plantaE/recepciones_form.html', {'form': form})
'''