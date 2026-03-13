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

class ObtenerLlaveRecepcionView(View):

    def get(self, request, *args, **kwargs):

        # Filtramos recepciones >= 2875
        llave_recepcion = detallerec.objects.filter(recepcion__gte=2875).values('criterio').distinct()
        llave_recepcion2 = detallerec.objects.filter(recepcion__gte=2875).values('recepcion').distinct()

        # Sumas de porcentaje por llave en Ccalidad
        suma_por_llave = Ccalidad.objects.values('llave').annotate(suma=Sum('porcentaje'))
        suma_dict = {item['llave']: item['suma'] for item in suma_por_llave}

        # Obtener registros de detallerec filtrando por recepcion
        datos = detallerec.objects.filter(recepcion__gte=2875)

        datos_modificados = []

        for item in datos:
            # Número de semana de fechasalidafruta
            semana = item.fechasalidafruta.isocalendar()[1] if item.fechasalidafruta else None

            # Concatenación condicional
            clave = f"{semana} | {item.llave} | {item.cultivo}" if item.finca == "Productor" else f"{semana} | {item.finca} | {item.cultivo}"

            datos_modificados.append(clave)

        # Eliminar duplicados
        datos_modificados = list(set(datos_modificados))

        # Filtrar por suma de porcentaje < 1
        datos_modificados = [clave for clave in datos_modificados if suma_dict.get(clave, 0) < 1]

        # Obtener causas de rechazo
        causa_rechazo = causasRechazo.objects.all().values('causa')

        # Fecha actual
        now = timezone.localtime(timezone.now()).date()
        fecha_ = now.strftime("%Y-%m-%d")

        return JsonResponse({
            'llaves': "",
            'causa': list(causa_rechazo),
            'fecha': fecha_,
            'llave': list(llave_recepcion2),
            'datos_filtrados': datos_modificados
        })
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

def obtener_llave_recepcion(request):
    # Obtén los criterios únicos filtrando por 'recepcion' mayor o igual a 2875
    llave_recepcion = detallerec.objects.filter(recepcion__gte=2875).values('criterio').distinct()
    llave_recepcion2 = detallerec.objects.filter(recepcion__gte=2875).values('recepcion').distinct()

    # Crea un diccionario para almacenar las sumas de porcentaje por llave en Ccalidad
    suma_por_llave = Ccalidad.objects.values('llave').annotate(suma=Sum('porcentaje'))

    # Convierte el resultado a un diccionario para facilitar el acceso
    suma_dict = {item['llave']: item['suma'] for item in suma_por_llave}

    # Obtener los registros de detallerec filtrando por 'recepcion' y calculando la semana de 'fechasalidafruta'
    datos = detallerec.objects.filter(recepcion__gte=2875)

    # Lista para almacenar las concatenaciones de la semana, finca/llave y cultivo
    datos_modificados = []

    for item in datos:
        # Extraer el número de semana de la fecha 'fechasalidafruta'
        fecha = item.fechasalidafruta
        if fecha:
            semana = fecha.isocalendar()[1]  # Usamos isocalendar() para obtener el número de semana
        else:
            semana = None

        # Realizar la concatenación condicional de 'finca' o 'llave' y 'cultivo'
        if item.finca == "Productor":
            clave = f"{semana} | {item.llave} | {item.cultivo}"
        else:
            clave = f"{semana} | {item.finca} | {item.cultivo}"

        # Agregar la clave concatenada a la lista de datos modificados
        datos_modificados.append(clave)

    # Eliminar duplicados en la lista de concatenaciones
    datos_modificados = list(set(datos_modificados))

    # Filtrar los datos_modificados para mantener solo aquellos con suma de porcentaje menor a 1
    datos_modificados = [
        clave for clave in datos_modificados
        if suma_dict.get(clave, 0) < 1  # Solo mantener claves cuyo porcentaje es menor que 1
    ]

    # Obtener las causas de rechazo
    causa_rechazo = causasRechazo.objects.all().values('causa')

    # Obtener la fecha actual en formato 'YYYY-MM-DD'
    now = datetime.datetime.now()
    fecha = now.date()
    dia = fecha.day
    mes = fecha.month
    año = fecha.year

    # Asegurarse de que el día y el mes tengan 2 dígitos
    if mes < 10:
        mes = "0" + str(mes)
    if dia < 10:
        dia = "0" + str(dia)
    
    # Formatear la fecha
    fecha_ = f"{año}-{mes}-{dia}"

    # Devolver los datos en formato JSON
    return JsonResponse({
        'llaves': "",
        'causa': list(causa_rechazo),
        'fecha': fecha_,
        'llave': list(llave_recepcion2),
        'datos_filtrados': datos_modificados  # Aquí se agregan las claves filtradas
    })
'''