from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.contrib import messages
from django.db.models import Sum
# modelos
from plantaE.models import Ccalidad, causasRechazo, detallerec

# formularios
from plantaE.forms import ccalidadForm

class CcalidadListView(ListView):
    model = Ccalidad
    template_name = 'plantaE/ccalidad/ccalidad_list.html'
    context_object_name = 'registros'

    def get_queryset(self):
        today = timezone.localtime(timezone.now()).date()

        return Ccalidad.objects.filter(
            fecha__year=today.year,
            fecha__month=today.month
        ).exclude(status="Anulado").order_by('-registro')


class CcalidadDetailView(DetailView):
    model = Ccalidad
    template_name = 'plantaE/ccalidad/ccalidad_detail.html'
    context_object_name = 'registros'

class CcalidadCreateView(CreateView):
    model = Ccalidad
    form_class = ccalidadForm
    template_name = 'plantaE/ccalidad/ccalidad_form.html'
    success_url = reverse_lazy('ccalidad_list')

    def form_invalid(self, form):
        return JsonResponse({'errores': form.errors}, status=400)

    def form_valid(self, form):
        try:
            self.object = form.save()
            return super().form_valid(form)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modo'] = 'crear'
        return context

class CcalidadUpdateView(UpdateView):
    model = Ccalidad
    form_class = ccalidadForm
    template_name = 'plantaE/ccalidad/ccalidad_form_edit.html'
    success_url = reverse_lazy('ccalidad_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modo'] = 'actualizar'
        return context

class CcalidadUpdateAuxView(View):

    def get(self, request):

        pk = request.GET.get('pk')

        salidas = get_object_or_404(Ccalidad, pk=pk)

        causa_rechazo = causasRechazo.objects.all().values('causa')

        return JsonResponse({
            'llave': salidas.llave,
            'recepcion': salidas.recepcion,
            'causa_select': salidas.causarechazo,
            'causas': list(causa_rechazo)
        })
        
class CcalidadDeleteView(View):

    template_name = 'plantaE/ccalidad/ccalidad_confirm_delete.html'

    def get(self, request, pk):
        salidas = get_object_or_404(Ccalidad, pk=pk)
        return render(request, self.template_name, {'registros': salidas})

    def post(self, request, pk):

        salidas = get_object_or_404(Ccalidad, pk=pk)

        salidas.status = 'Anulado'
        salidas.save()

        messages.success(request, "Registro anulado correctamente.")

        return render(request, self.template_name, {'registros': salidas})

class LoadCcalidadParamView(View):

    def get(self, request, *args, **kwargs):
        llave_recepcion = request.GET.get('category_id')

        # Obtener recepciones distintas según criterio
        datos = detallerec.objects.filter(
            criterio=llave_recepcion
        ).values('recepcion').distinct('recepcion')

        # Sumar porcentaje de Ccalidad para esa llave
        valor = Ccalidad.objects.filter(llave=llave_recepcion).aggregate(suma=Sum('porcentaje'))['suma']

        if valor is not None:
            valor = 1 - float(valor)
        else:
            valor = 1

        return JsonResponse({'datos': list(datos), 'valor': valor})

'''
def ccalidad_list(request):
    today = timezone.localtime(timezone.now()).date()
    current_month = today.month
    current_year = today.year
    salidas = Ccalidad.objects.filter(fecha__year=current_year,fecha__month=current_month).order_by('-registro').exclude(status="Anulado")
    

    return render(request, 'plantaE/ccalidad_list.html', {'registros': salidas})

def ccalidad_detail(request, pk):
    salidas = get_object_or_404(Ccalidad, pk=pk)
    return render(request, 'plantaE/ccalidad_detail.html', {'registros': salidas})

def ccalidad_create(request):
    if request.method == 'POST':
        form = ccalidadForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                # Manejar excepciones específicas (por ejemplo, UniqueConstraintError)
                return JsonResponse({'error': str(e)}, status=400)
            return redirect('ccalidad_list')
        else:
             # Imprimir errores para depuración
            return JsonResponse({'errores': form.errors}, status=400)
    else:
        form = ccalidadForm()
    return render(request, 'plantaE/ccalidad_form.html', {'form': form,'modo':'crear'})

def ccalidad_update(request, pk):
    salidas = get_object_or_404(Ccalidad, pk=pk)
    if request.method == 'POST':
        form = ccalidadForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('ccalidad_list')
    else:
        form = ccalidadForm(instance=salidas)
        
    return render(request, 'plantaE/ccalidad_form_edit.html', {'form': form,'modo':'actualizar'})

def ccalidad_update_aux(request):
    pk = request.GET.get('pk')
    salidas = get_object_or_404(Ccalidad, pk=pk)
    causa_rechazo = causasRechazo.objects.all().values('causa')
    return JsonResponse({'llave': salidas.llave,'recepcion':salidas.recepcion,'causa_select':salidas.causarechazo,'causas':list(causa_rechazo)})
    
def ccalidad_delete(request, pk):
    salidas = get_object_or_404(Ccalidad, pk=pk)

    if request.method == 'POST':
        salidas.status = 'Anulado'
        salidas.save()
        
        messages.success(request, "Registro anulado correctamente.")
    return render(request, 'plantaE/ccalidad_confirm_delete.html', {'registros': salidas})
'''