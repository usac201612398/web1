from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.views import View

# modelos
from plantaE.models import Actpeso, Recepciones

class PesosListView(ListView):
    model = Actpeso
    template_name = 'plantaE/actpeso/pesos_list.html'
    context_object_name = 'registros'

    def get_queryset(self):
        today = timezone.now().date()
        return Actpeso.objects.filter(
            fecha=today
        ).exclude(status='Anulado').order_by('created')

class PesosDetailView(DetailView):
    model = Actpeso
    template_name = 'plantaE/actpeso/pesos_detail.html'
    context_object_name = 'registros'

class PesosDeleteView(View):

    template_name = 'plantaE/actpeso/pesos_confirm_delete.html'

    def get(self, request, pk):
        salidas = get_object_or_404(Actpeso, pk=pk)
        return render(request, self.template_name, {'registros': salidas})

    def post(self, request, pk):

        salidas = get_object_or_404(Actpeso, pk=pk)

        recepcion = Recepciones.objects.filter(recepcion=salidas.recepcion)

        if recepcion.exists():
            return render(request, self.template_name, {
                'registros': salidas,
                'alert_message': "No se puede anular este peso porque ya tiene una recepción asignada, anule la recepcion.",
                'redirect_url': reverse('pesos_list')
            })

        salidas.status = 'Anulado'
        salidas.save()

        return render(request, self.template_name, {
            'alert_message': "El registro fue anulado correctamente.",
            'redirect_url': reverse('pesos_list')
        })   
'''
def pesos_list(request):
    today = timezone.now().date()
    salidas = Actpeso.objects.filter(fecha=today).exclude(status='Anulado')
    salidas = salidas.order_by('created')
    
    return render(request, 'plantaE/pesos_list.html', {'registros': salidas})

def pesos_detail(request, pk):
    salidas = get_object_or_404(Actpeso, pk=pk)
    return render(request, 'plantaE/pesos_detail.html', {'registros': salidas})

def pesos_delete(request, pk):
    salidas = get_object_or_404(Actpeso, pk=pk)
    recepcion = Recepciones.objects.filter(recepcion=salidas.recepcion)
    # Validar si tiene recepción asignada
    if recepcion.exists():
        return render(request, 'plantaE/pesos_confirm_delete.html', {
            'registros': salidas,
            'alert_message': "No se puede anular este peso porque ya tiene una recepción asignada, anule la recepcion.",
            'redirect_url': reverse('pesos_list')
        })

    if request.method == 'POST':
        salidas.status = 'Anulado'
        salidas.save()
        return render(request, 'plantaE/pesos_confirm_delete.html', {
            'alert_message': "El registro fue anulado correctamente.",
            'redirect_url': reverse('pesos_list')
        })

    return render(request, 'plantaE/pesos_confirm_delete.html', {'registros': salidas})
'''