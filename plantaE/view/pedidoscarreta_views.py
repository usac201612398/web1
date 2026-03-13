from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, UpdateView
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Sum, F, FloatField, ExpressionWrapper
from django.db.models.functions import ExtractMonth, ExtractIsoYear
from django.db import transaction
import json

# modelos
from plantaE.models import (
    pedidos, productoTerm, detallerec, detallerecaux, usuariosAppFruta
)

# formularios
from plantaE.forms import pedidosForm

class PedidosCarretaView(View):

    template_name = "plantaE/pedidoscarreta/pedidos.html"

    def get(self, request):

        fecha = timezone.localtime(timezone.now()).date()
        fecha_ = fecha.strftime("%Y-%m-%d")

        nombre_usuario = request.user.username

        datos = usuariosAppFruta.objects.filter(
            correo=nombre_usuario
        ).values('finca', 'encargado')

        items = productoTerm.objects.filter(
            categoria="Carreta"
        ).values(
            'precio', 'itemsapname', 'itemsapcode', 'cultivo'
        ).distinct().order_by('cultivo')

        cultivos = set(item['cultivo'] for item in items)

        stock_por_cultivo = {}

        for cultivo in cultivos:

            entradas = detallerec.objects.filter(
                cultivo=cultivo
            ).exclude(
                status__in=['Cerrado', 'En proceso', 'Anulado']
            )

            total_entradas = entradas.aggregate(
                total=Sum('libras')
            )['total'] or 0

            salidas = detallerecaux.objects.filter(
                cultivo=cultivo
            ).exclude(status__in=['Cerrado', 'Anulado'])

            total_salidas = salidas.aggregate(
                total=Sum('libras')
            )['total'] or 0

            stock_por_cultivo[cultivo] = round(total_entradas - total_salidas, 2)

        for item in items:
            item['stock'] = stock_por_cultivo.get(item['cultivo'], 0)

        context = {
            'usuario': nombre_usuario,
            'registros': items,
            'fecha': fecha_,
            'encargado': list(datos)[0]['encargado'] if datos else ''
        }

        return render(request, self.template_name, context)

class PedidosListView(ListView):

    model = pedidos
    template_name = "plantaE/pedidoscarreta/pedidos_list.html"
    context_object_name = "registros"

    def get_queryset(self):

        today = timezone.now().date()

        return pedidos.objects.annotate(
            mes=ExtractMonth('fechapedido'),
            anio=ExtractIsoYear('fechapedido'),
        ).filter(
            mes=today.month,
            anio=today.year
        ).exclude(
            status__in=['Anulado', 'Cancelado', 'Entregado']
        ).order_by('-created_at')

class PedidosHistoricoView(ListView):

    model = pedidos
    template_name = "plantaE/pedidoscarreta/pedidos_list_historico.html"
    context_object_name = "registros"

    def get_queryset(self):

        today = timezone.now().date()

        return pedidos.objects.annotate(
            mes=ExtractMonth('fechapedido'),
            anio=ExtractIsoYear('fechapedido'),

            libras_por_empaque=ExpressionWrapper(
                F('libras') / F('empaque'),
                output_field=FloatField()
            ),

            libras_por_entregado=ExpressionWrapper(
                F('libras') / F('cantidadentregado'),
                output_field=FloatField()
            )

        ).filter(
            mes=today.month,
            anio=today.year
        ).exclude(
            pedido=0
        ).order_by('-created_at')

class GuardarPedidoView(View):

    def post(self, request):

        data = json.loads(request.body)
        mensaje = data['array']

        today = timezone.now().date()

        for elemento in mensaje:
            elemento[4] = int(elemento[4])

        with transaction.atomic():

            ultimo = pedidos.objects.order_by('-registro').first()
            nuevo_pedido = ultimo.pedido + 1 if ultimo else 1

            for i in mensaje:

                datos = productoTerm.objects.filter(
                    itemsapcode=i[0]
                ).first()

                if datos.itemsapcode == "305.100.354":

                    empaque = i[4] * datos.empaque

                    if empaque <= 1500:
                        costo = empaque * 12
                    else:
                        costo = 1500 * 12 + (empaque - 1500) * 9

                else:
                    empaque = i[4] * datos.empaque
                    costo = (datos.precio / datos.empaque) * empaque

                pedidos.objects.create(
                    fecha=today,
                    proveedor=i[8],
                    pedido=nuevo_pedido,
                    calidad1=datos.calidad1,
                    fechapedido=i[6],
                    cliente=i[5],
                    cultivo=i[2],
                    categoria=datos.categoria,
                    cantidad=i[4],
                    encargado=i[7],
                    itemsapcode=i[0],
                    itemsapname=i[1],
                    precio=costo,
                    total=datos.precio * i[4],
                    orden=datos.orden,
                    empaque=empaque
                )

        return JsonResponse({'mensaje': mensaje})

class PedidosUpdateView(UpdateView):

    model = pedidos
    form_class = pedidosForm
    template_name = "plantaE/pedidos_form.html"
    success_url = reverse_lazy('pedidos_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modo'] = "actualizar"
        return context

class PedidosDeleteView(View):

    template_name = "plantaE/pedidoscarreta/pedidos_confirm_delete.html"

    def get(self, request, pk):

        pedido = get_object_or_404(pedidos, pk=pk)
        registros = pedidos.objects.filter(pedido=pedido.pedido)

        return render(request, self.template_name, {'registros': registros})

    def post(self, request, pk):

        pedido = get_object_or_404(pedidos, pk=pk)
        pedidos_a_anular = pedidos.objects.filter(pedido=pedido.pedido)

        if pedidos_a_anular.filter(envio__isnull=False).exists():

            return render(request, self.template_name, {
                'alert_message': "No se puede anular este pedido porque ya tiene un envío asignado.",
                'redirect_url': reverse('pedidos_list')
            })

        with transaction.atomic():
            pedidos_a_anular.update(status='Anulado')

        return render(request, self.template_name, {
            'alert_message': "El pedido fue anulado correctamente.",
            'redirect_url': reverse('pedidos_list')
        })

class PedidosCancelView(View):

    template_name = "plantaE/pedidoscarreta/pedidos_confirm_cancel.html"

    def get(self, request, pk):

        registro = get_object_or_404(pedidos, pk=pk)

        return render(request, self.template_name, {'registros': registro})

    def post(self, request, pk):

        registro = get_object_or_404(pedidos, pk=pk)

        if registro.envio:

            return render(request, self.template_name, {
                'alert_message': "No se puede cancelar este pedido porque ya tiene un envío asignado.",
                'redirect_url': reverse('pedidos_list')
            })

        registro.status = "Cancelado"
        registro.save()

        return render(request, self.template_name, {
            'alert_message': "El elemento fue cancelado correctamente.",
            'redirect_url': reverse('pedidos_list')
        })
'''

def article_create_pedidos(request):

    fecha = timezone.now().date()
    dia = fecha.day
    mes = fecha.month
    año = fecha.year
    if mes < 10:
        mes = "0" + str(mes)
    if dia < 10:
        dia = "0" + str(dia)
    fecha_ = "{}-{}-{}".format(str(año), str(mes), str(dia))

    nombre_usuario = request.user.username
    datos = usuariosAppFruta.objects.filter(correo=nombre_usuario).values('finca', 'encargado')

    # Traemos todos los items de la categoría Carreta
    items = productoTerm.objects.filter(categoria="Carreta").values(
        'precio', 'itemsapname', 'itemsapcode', 'cultivo'
    ).distinct().order_by('cultivo')

    cultivos = set(item['cultivo'] for item in items)

    stock_por_cultivo = {}

    for cultivo in cultivos:
        # Entradas (inventario inicial)
        entradas = detallerec.objects.filter(
            cultivo=cultivo
        ).exclude(status__in=['Cerrado', 'En proceso']).exclude(status='Anulado')

        total_entradas = entradas.aggregate(total=Sum('libras'))['total'] or 0

        # Salidas (inventario entregado)
        salidas = detallerecaux.objects.filter(
            cultivo=cultivo
        ).exclude(status='Cerrado').exclude(status='Anulado')

        total_salidas = salidas.aggregate(total=Sum('libras'))['total'] or 0

        stock = total_entradas - total_salidas
        stock_por_cultivo[cultivo] = round(stock, 2)

    # Agregar el stock a cada item
    for item in items:
        cultivo = item['cultivo']
        item['stock'] = stock_por_cultivo.get(cultivo, 0)

    context = {
        'usuario': nombre_usuario,
        'registros':items,
        'fecha': fecha_,
        'encargado': list(datos)[0]['encargado'] if datos else ''
    }

    return render(request, 'plantaE/pedidos.html', context)

def pedidos_list(request):
    today = timezone.now().date()
    
    # Para Python 3.8: isocalendar() devuelve una tupla (año, semana, día)
    current_month = today.month
    current_year = today.year

    salidas = pedidos.objects.annotate(
        mes=ExtractMonth('fechapedido'),
        anio=ExtractIsoYear('fechapedido'),
    ).filter(
        mes=current_month,
        anio=current_year
    ).order_by('-created_at').exclude(status__in=['Anulado', 'Cancelado', 'Entregado'])

    return render(request, 'plantaE/pedidos_list.html', {'registros': salidas})

def pedidos_list_historico(request):
    today = timezone.now().date()
    current_month = today.month
    current_year = today.year

    salidas = pedidos.objects.annotate(
        mes=ExtractMonth('fechapedido'),
        anio=ExtractIsoYear('fechapedido'),
        libras_por_empaque=ExpressionWrapper(
            F('libras') / F('empaque'),
            output_field=FloatField()
        ),
        libras_por_entregado=ExpressionWrapper(
            F('libras') / F('cantidadentregado'),
            output_field=FloatField()
        )
    ).filter(
        mes=current_month,
        anio=current_year
    ).exclude(pedido=0).order_by('-created_at')

    return render(request, 'plantaE/pedidos_list_historico.html', {'registros': salidas})

def guardar_pedido(request):
    data = json.loads(request.body)
    mensaje = data['array']
    today = timezone.now().date()
    #mensaje = request.POST.get('array')
   
    for elemento in mensaje:
        elemento[4] = int(elemento[4])

    ultimo_pedido_obj = pedidos.objects.order_by('-registro').first()
    nuevo_pedido = ultimo_pedido_obj.pedido + 1 if ultimo_pedido_obj else 1
    
    for i in mensaje:

        datos = productoTerm.objects.filter(itemsapcode=i[0]).first()
        
        if datos.itemsapcode == "305.100.354":
            empaque = i[4]*datos.empaque 
            if empaque <=1500:
                costo = empaque*12
            else:
                costo = 1500*12 + (empaque-1500)*9
        else:
            costo = (datos.precio/datos.empaque)*empaque

        pedidos.objects.create(fecha=today,proveedor=i[8],pedido=nuevo_pedido,calidad1=datos.calidad1,fechapedido=i[6],cliente=i[5],cultivo=i[2],categoria=datos.categoria,cantidad=i[4],encargado=i[7],itemsapcode=i[0],itemsapname=i[1],precio=costo,total=datos.precio*i[4],orden=datos.orden,empaque=datos.empaque*i[4])
    
    
    return JsonResponse({'mensaje':mensaje})  

def pedidos_update(request, pk):
    salidas = get_object_or_404(pedidos, pk=pk)
    if request.method == 'POST':
        form = pedidosForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('pedidos_list')
    else:
        form = pedidosForm(instance=salidas)
    return render(request, 'plantaE/pedidos_form.html', {'form': form,'modo':'actualizar'})

def pedidos_delete(request, pk):
    salidas = get_object_or_404(pedidos, pk=pk)
    pedido_numero = salidas.pedido  # Este es el número de pedido
    pedidos_a_anular = pedidos.objects.filter(pedido=pedido_numero)

    # Verificar si alguno de los registros ya tiene envío
    if pedidos_a_anular.filter(envio__isnull=False).exists():
        return render(request, 'plantaE/pedidos_confirm_delete.html', {
            'alert_message': "No se puede anular este pedido porque ya tiene un envío asignado.",
            'redirect_url': reverse('pedidos_list')
        })

    # Si la solicitud es POST, proceder a anular
    if request.method == 'POST':
        for pedido in pedidos_a_anular:
            pedido.status = 'Anulado'
            pedido.save()

        return render(request, 'plantaE/pedidos_confirm_delete.html', {
            'alert_message': "El pedido fue anulado correctamente.",
            'redirect_url': reverse('pedidos_list')
        })

    # Confirmación de anulación (GET request)
    return render(request, 'plantaE/pedidos_confirm_delete.html', {
        'registros': pedidos_a_anular  # Puedes mostrar todos los registros relacionados
    })

def pedidos_cancel(request, pk):
    salidas = get_object_or_404(pedidos, pk=pk)

    # Verificar si alguno de los registros ya tiene envío
    if salidas.filter(envio__isnull=False).exists():
        return render(request, 'plantaE/pedidos_confirm_delete.html', {
            'alert_message': "No se puede cancelar este pedido porque ya tiene un envío asignado.",
            'redirect_url': reverse('pedidos_list')
        })

    # Si la solicitud es POST, proceder a anular
    if request.method == 'POST':
        salidas.status = 'Cancelado'
        salidas.save()

        return render(request, 'plantaE/pedidos_confirm_delete.html', {
            'alert_message': "El elemento fue cancelado correctamente.",
            'redirect_url': reverse('pedidos_list')
        })

    # Confirmación de anulación (GET request)
    return render(request, 'plantaE/pedidos_confirm_cancel.html', {
        'registros': salidas  # Puedes mostrar todos los registros relacionados
    })
'''