from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.db import transaction
from django.urls import reverse_lazy
from plantaE.forms import enviosForm
# modelos
from plantaE.models import enviosrec, inventarioProdTerm, controlcajas

class EnviosLocalListView(ListView):
    model = enviosrec
    template_name = 'plantaE/envioslocal/envioslocal_list.html'
    context_object_name = 'registros'

    def get_queryset(self):
        today = timezone.localtime(timezone.now()).date()
        return enviosrec.objects.filter(
            fecha__year=today.year,
            fecha__month=today.month
        ).exclude(status="Anulado").order_by('-envio')

class EnviosLocalDetailView(DetailView):
    model = enviosrec
    template_name = 'plantaE/envioslocal/envioslocal_detail.html'
    context_object_name = 'registros'


class EnviosLocalDeleteView(View):
    template_name = 'plantaE/envioslocal/envioslocal_confirm_delete.html'

    def get(self, request, pk):
        envio_original = get_object_or_404(enviosrec, pk=pk)
        return render(request, self.template_name, {'registros': envio_original})

    def post(self, request, pk):
        envio_original = get_object_or_404(enviosrec, pk=pk)

        # Obtener todos los registros con el mismo "envio"
        registros_a_anular = enviosrec.objects.filter(envio=envio_original.envio)

        # Registros de inventario relacionados
        inventarios_relacionados = inventarioProdTerm.objects.filter(
            enviorec=envio_original.envio
        ).exclude(status='Anulado')

        # Validar si alguno tiene boleta asignada
        boletas_asignadas = inventarios_relacionados.filter(
            boleta__isnull=False
        ).exclude(boleta=0).exists()

        if boletas_asignadas:
            return render(request, self.template_name, {
                'registros': envio_original,
                'alert_message': "No se puede anular este envío porque uno o más registros tienen boletas asignadas.",
                'redirect_url': reverse('envioslocal_list')
            })

        # Aquí entra la atomicidad
        with transaction.atomic():
            # Anular registros de envío e inventario
            registros_a_anular.update(status='Anulado')
            inventarios_relacionados.update(status='Anulado', status3='Anulado')
            controlcajas.objects.filter(transaccion=envio_original.envio).update(status='Anulado')

        return render(request, self.template_name, {
            'registros': envio_original,
            'alert_message': "El envío y todos los registros relacionados fueron anulados correctamente.",
            'redirect_url': reverse('envioslocal_list')
        })

class EnviosLocalUpdateView(View):
    model = enviosrec
    form_class = enviosForm
    template_name = 'plantaE/envioslocal/envioslocal_form.html'
    success_url = reverse_lazy('envioslocal_update')

'''
def envioslocal_list(request):

    today = timezone.localtime(timezone.now()).date()
    current_month = today.month
    current_year = today.year
    #salidas = Recepciones.objects.filter(fecha=today)
    salidas= enviosrec.objects.filter(fecha__year=current_year,fecha__month=current_month).order_by('-envio').exclude(status="Anulado")

    return render(request, 'plantaE/envioslocal_list.html', {'registros': salidas})

def envioslocal_detail(request, pk):
    salidas = get_object_or_404(enviosrec, pk=pk)
    return render(request, 'plantaE/envioslocal_detail.html', {'registros': salidas})

def envioslocal_delete(request, pk):

    envio_original = get_object_or_404(enviosrec, pk=pk)

    # Obtener todos los registros con el mismo "envio" (o 'registro')
    registros_a_anular = enviosrec.objects.filter(envio=envio_original.envio)

    # Registros de inventario relacionados
    inventarios_relacionados = inventarioProdTerm.objects.filter(
        enviorec=envio_original.envio
    ).exclude(status='Anulado')

    # Validar si alguno de esos registros ya tiene boleta asignada
    boletas_asignadas = inventarios_relacionados.filter(
        boleta__isnull=False
    ).exclude(boleta=0).exists()

    if boletas_asignadas:
        return render(request, 'plantaE/envioslocal_confirm_delete.html', {
            'registros': envio_original,
            'alert_message': "No se puede anular este envío porque uno o más registros tienen boletas asignadas.",
            'redirect_url': reverse('envioslocal_list')
        })

    if request.method == 'POST':
        # Anular todos los registros de envío relacionados
        registros_a_anular.update(status='Anulado')

        # Anular registros de inventario
        inventarios_relacionados.update(status='Anulado', status3='Anulado')
        registros_a_anular_2 = controlcajas.objects.filter(transaccion=envio_original.envio)
        registros_a_anular_2.update(status='Anulado')
        return render(request, 'plantaE/envioslocal_confirm_delete.html', {
            'registros': envio_original,
            'alert_message': "El envío y todos los registros relacionados fueron anulados correctamente.",
            'redirect_url': reverse('envioslocal_list')
        })

    # Mostrar la confirmación inicial
    return render(request, 'plantaE/envioslocal_confirm_delete.html', {
        'registros': envio_original
    })
'''