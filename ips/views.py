from django.shortcuts import render
from .models import QRCodeData
import json
from django.http import JsonResponse, HttpResponse
from openpyxl import Workbook
from .forms import RegistroQRForm
from django.shortcuts import get_object_or_404, redirect
# Create your views here.
import json
import pandas as pd
import pytz
import datetime

def index(request):
    return render(request, 'ips/escanerqr.html')

def exportar_excel(request):
    
    # Crea un libro de Excel y una hoja
    wb = Workbook()
    ws = wb.active
    ws.title = 'Datos'
    # Obtiene parámetros de fecha desde GET
    fecha_inicio_str = request.GET.get('fecha_inicio')
    fecha_fin_str = request.GET.get('fecha_fin')
    # Obtén los datos de tu modelo
    datos = QRCodeData.objects.all()

    # Especifica la zona horaria deseada
    zona_horaria_deseada = pytz.timezone('America/Guatemala')  # Cambia esto según sea necesario
    
    if fecha_inicio_str and fecha_fin_str:
        try:
            # Convertimos strings a objetos datetime (inicio del día y fin del día)
            fecha_inicio = datetime.datetime.strptime(fecha_inicio_str, "%Y-%m-%d")
            fecha_fin = datetime.datetime.strptime(fecha_fin_str, "%Y-%m-%d")
            fecha_inicio = datetime.datetime.combine(fecha_inicio, datetime.time.min)
            fecha_fin = datetime.datetime.combine(fecha_fin, datetime.time.max)

            datos = datos.filter(created_at__range=(fecha_inicio, fecha_fin))
        except ValueError:
            pass  # Manejo básico si el formato es incorrecto

    # Agrega los encabezados
    ws.append([field.name for field in QRCodeData._meta.fields])
    # Agrega los datos  
    for obj in datos:
        row = []
        for field in QRCodeData._meta.fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                # Convertir a la zona horaria deseada
                if value.tzinfo is not None:
                    value = value.astimezone(zona_horaria_deseada)
                    value = value.replace(tzinfo=None)  # Eliminar la zona horaria para ser compatible con Excel
            row.append(value)
        ws.append(row)
    
    # Crea una respuesta HTTP que sirva el archivo Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=datos.xlsx'

    # Guarda el libro de Excel en la respuesta
    wb.save(response)

    return response

def ips_visualizar(request):
    salidas = QRCodeData.objects.exclude(status='Cerrado')  # Excluye los que tienen status 'Cerrado'
    salidas = salidas.order_by('-created_at')
    
    return render(request, 'ips/listqr.html', {'registros': salidas})

def ips_visualizarall(request):
    salidas = QRCodeData.objects.all()  # Excluye los que tienen status 'Cerrado'
    salidas = salidas.order_by('-created_at')
    
    return render(request, 'ips/listqrall.html', {'registros': salidas})

def ips_borrar(request, pk):
    salidas = get_object_or_404(QRCodeData, pk=pk)
    if request.method == 'POST':
        salidas.delete()
        return redirect('ips_visualizar')
    return render(request, 'ips/escanerqr_confirm_delete.html', {'registros': salidas})

def save_qr(request):
    if request.method == 'POST':
        try:
            # Obtener los datos del cuerpo de la solicitud (en formato JSON)
            data = json.loads(request.body)  # Cargar el JSON en un diccionario
            qr_data = data.get('qr_data')  # Obtener el valor del QR desde el JSON
            cantidad_=data.get('cantidad')
            color_ = data.get('color')
            cosechador_ = data.get('cosechador')
            blossom_ = data.get('blossom')

            if qr_data:
                # Guardar el QR en la base de datos
                QRCodeData.objects.create(data=qr_data,cantidad=cantidad_,color=color_,cosechador=cosechador_,blossom=blossom_),
                return JsonResponse({'message': 'QR guardado correctamente'})
            else:
                return JsonResponse({'error': 'No se recibió ningún dato QR'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Error al procesar el JSON'}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

def actualizar_registro(request, pk):
    # Obtener el registro a partir del qr_data
    registro = get_object_or_404(QRCodeData, pk=pk)
    
    if request.method == "POST":
        form = RegistroQRForm(request.POST, instance=registro)
        
        if form.is_valid():
            form.save()  # Guardar los cambios en la base de datos
            return redirect('ips_visualizar')  # Redirigir a una página de éxito o el detalle del registro actualizado
    else:
        form = RegistroQRForm(instance=registro)  # Mostrar el formulario con los datos actuales

    return render(request, 'ips/editqrlist.html', {'form': form})