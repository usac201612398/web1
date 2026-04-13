from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView
from django.http import JsonResponse
from django.db.models import Sum, Case, When, Value as V, F, IntegerField
from django.db.models.functions import Trim, Abs

# modelos
from plantaE.models import controlcajas, tipoCajas, envioccajas

# formularios
from plantaE.forms import controlcajasForm

def cerrar_envio(request, envio_id):
    envio = get_object_or_404(envioccajas, id=envio_id)
    envio.destino = request.POST.get("destino")
    envio.recibe = request.POST.get("recibe")
    envio.observaciones = request.POST.get("observaciones")
    envio.save()
    # 🔥 VALIDACIONES
    if not envio.destino or not envio.recibe:
        return redirect('envio_workspace', envio_id=envio.id)

    return redirect('controlcajas_list')
def anular_caja(request, pk):
    caja = get_object_or_404(controlcajas, pk=pk)

    caja.status = "Anulado"
    caja.save()

    return redirect('envio_workspace', envio_id=caja.envio)
class ControlCajasPrintView(View):

    def get(self, request, pk):
        registro = get_object_or_404(controlcajas, pk=pk)

        return render(
            request,
            'plantaE/controlcajas/controlcajas_print.html',
            {'registro': registro}
        )
class EnvioCreateAutoView(View):

    def post(self, request):

        ultimo = envioccajas.objects.order_by('-id').exclude(status='Anulado').first()
        nuevo_id = (ultimo.id + 1) if ultimo else 1

        envio = envioccajas.objects.create(
            id=nuevo_id,
            status="Abierto"
        )

        return JsonResponse({
            "envio_id": envio.id,
            "redirect": reverse('envio_workspace', args=[envio.id])
        })

class EnvioWorkspaceView(View):

    def get(self, request, envio_id):

        envio = get_object_or_404(envioccajas, id=envio_id)
        cajas = controlcajas.objects.exclude(status='Anulado').filter(envio=envio_id)

        total = sum([c.cajas or 0 for c in cajas])

        return render(request, "plantaE/controlcajas/controlcajas_workspace.html", {
            "envio": envio,
            "cajas": cajas,
            "total": total
        })

    def post(self, request, envio_id):

        envio = get_object_or_404(envioccajas, id=envio_id)

        envio.destino = request.POST.get("destino")
        envio.recibe = request.POST.get("recibe")
        envio.observaciones = request.POST.get("observaciones")

        envio.save()

        return redirect('envio_workspace', envio_id=envio.id) 

class ControlCajasListView(ListView):
    model = controlcajas
    template_name = 'plantaE/controlcajas/controlcajas_list.html'
    context_object_name = 'registros'

    def get_queryset(self):
        return controlcajas.objects.exclude(tipomov="Recepción").order_by('-registro')

class ControlCajasInventarioView(View):

    def get(self, request):

        resumen = (
            controlcajas.objects
            .annotate(
                lugar=Case(
                    When(tipomov='Recepción', then=Trim(F('lugar_entra'))),
                    When(tipomov='Entrega', then=Trim(F('lugar_sale'))),
                    default=V(''),
                ),
                item=Trim(F('itemsapcode')),
                cajas_signo=Case(
                    When(tipomov='Recepción', then=Abs(F('cajas'))),
                    When(tipomov='Entrega', then=-Abs(F('cajas'))),
                    default=V(0),
                    output_field=IntegerField()
                ),
            )
            .exclude(lugar__isnull=True).exclude(lugar__exact='')
            .exclude(item__isnull=True).exclude(item__exact='')
            .values('lugar', 'item', 'tipodecaja')
            .annotate(total_cajas=Sum('cajas_signo'))
            .order_by('lugar', 'item', 'tipodecaja')
        )

        total_general = sum(row['total_cajas'] for row in resumen)

        return render(
            request,
            'plantaE/controlcajas/controlcajas_inventario.html',
            {'resumen': resumen, 'total_general': total_general}
        )

class ControlCajasCreateView(CreateView):
    model = controlcajas
    form_class = controlcajasForm
    template_name = 'plantaE/controlcajas/controlcajas_form.html'
    success_url = reverse_lazy('controlcajas_list')
    def get_initial(self):
        initial = super().get_initial()
        initial['fecha'] = timezone.now().date()
        return initial
        
    def dispatch(self, request, *args, **kwargs):
        self.envio_id = request.GET.get("envio_id")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)

        if self.envio_id:
            obj.envio = self.envio_id

        obj.save()

        # 🔥 IMPORTANTE: volver al workspace, no al list
        return redirect('envio_workspace', envio_id=self.envio_id)

class ControlCajasUpdateView(UpdateView):
    model = controlcajas
    form_class = controlcajasForm
    template_name = 'plantaE/controlcajas/controlcajas_form.html'
    success_url = reverse_lazy('controlcajas_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modo'] = 'actualizar'
        return context

class ControlCajasDeleteView(View):

    template_name = 'plantaE/controlcajas/controlcajas_confirm_delete.html'

    def get(self, request, pk):
        salidas = get_object_or_404(controlcajas, pk=pk)
        return render(request, self.template_name, {'registros': salidas})

    def post(self, request, pk):

        salidas = get_object_or_404(controlcajas, pk=pk)

        if salidas.tipomov != "Manual":
            return render(request, self.template_name, {
                'registros': salidas,
                'alert_message': "No se puede anular este movimiento porque no es de serie manual.",
                'redirect_url': reverse('controlcajas_list')
            })

        salidas.status = 'Anulado'
        salidas.save()

        return render(request, self.template_name, {
            'alert_message': "El registro fue anulado correctamente.",
            'redirect_url': reverse('controlcajas_list')
        })     

class ObtenerItemsRelacionadosView(View):

    def get(self, request):

        code = request.GET.get('codigo')
        nombre = request.GET.get('nombre')

        if code:
            variedad = tipoCajas.objects.filter(itemsapcode=code).first()
            if variedad:
                return JsonResponse({'nombre': variedad.tcaja})

        elif nombre:
            variedad = tipoCajas.objects.filter(tcaja=nombre).first()
            if variedad:
                return JsonResponse({'codigo': variedad.itemsapcode})

        return JsonResponse({}, status=404)                      
'''
def controlcajas_list(request):
    salidas = controlcajas.objects.all() # Excluye los que tienen status 'Cerrado'
    salidas = salidas.order_by('-registro')
    return render(request, 'plantaE/controlcajas_list.html', {'registros': salidas})

def controlcajas_inventario(request):
    resumen = (controlcajas.objects
        .annotate(
            # Lugar según el tipo de movimiento
            lugar=Case(
                When(tipomov='Recepción', then=Trim(F('lugar_entra'))),
                When(tipomov='Entrega', then=Trim(F('lugar_sale'))),
                default=V(''),
            ),
            # Item (SAP)
            item=Trim(F('itemsapcode')),
            # Cajas con signo según la regla de negocio
            cajas_signo=Case(
                When(tipomov='Recepción', then=Abs(F('cajas'))),
                When(tipomov='Entrega', then=-Abs(F('cajas'))),
                default=V(0),
                output_field=IntegerField()
            ),
        )
        .exclude(lugar__isnull=True).exclude(lugar__exact='')
        .exclude(item__isnull=True).exclude(item__exact='')
        .values('lugar', 'item', 'tipodecaja')   # puedes usar solo 'lugar', 'item'
        .annotate(total_cajas=Sum('cajas_signo'))
        .order_by('lugar', 'item', 'tipodecaja')
    )

    # Si además quieres un total general:
    total_general = sum(row['total_cajas'] for row in resumen)

    return render(
        request,
        'plantaE/controlcajas_inventario.html',
        {'resumen': resumen, 'total_general': total_general})
   


def controlcajas_delete(request, pk):

    salidas = get_object_or_404(controlcajas, pk=pk)

    if salidas.tipomov!="Manual":
        return render(request, 'plantaE/controlcajas_confirm_delete.html', {
            'registros': salidas,
            'alert_message': "No se puede anular este  movimiento porque ya tiene no es de serie manual.",
            'redirect_url': reverse('controlcajas_list')
        })

    if request.method == 'POST':
        salidas.status = 'Anulado'
        salidas.save()
        return render(request, 'plantaE/controlpesos_confirm_delete.html', {
            'alert_message': "El registro fue anulado correctamente.",
            'redirect_url': reverse('controlpesos_list')
        })
    
    return render(request, 'plantaE/controlcajas_confirm_delete.html', {'registros': salidas})

def controlcajas_create(request):
    if request.method == 'POST':
        form = controlcajasForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                # Manejar excepciones específicas (por ejemplo, UniqueConstraintError)
                return JsonResponse({'error': str(e)}, status=400)
            return redirect('controlcajas_list')
        else:
             # Imprimir errores para depuración
            return JsonResponse({'errores': form.errors}, status=400)
    else:
        form = controlcajasForm()
    return render(request, 'plantaE/controlcajas_form.html', {'form': form,'modo':'crear'})

def obtener_items_relacionados(request):

    code = request.GET.get('codigo')
    nombre = request.GET.get('nombre')

    if code:
        variedad = tipoCajas.objects.filter(itemsapcode=code).first()
        
        if variedad:
            return JsonResponse({'nombre': variedad.tcaja})
    elif nombre:
        variedad = tipoCajas.objects.filter(tcaja=nombre).first()
        if variedad:
            return JsonResponse({'codigo': variedad.itemsapcode})

    return JsonResponse({}, status=404)

def controlcajas_update(request, pk):

    salidas = get_object_or_404(controlcajas, pk=pk)
    
    if request.method == 'POST':
        form = controlcajasForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('controlcajas_list')
    else:
        form = controlcajasForm(instance=salidas)
    return render(request, 'plantaE/controlcajas_form.html', {'form': form,'modo':'actualizar'})
'''