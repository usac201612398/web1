from django.shortcuts import render
from django.http import JsonResponse
from .models import QRCodeData
import json
def index(request):
    return render(request, 'ips/escanerqr.html')

def save_qr(request):
    if request.method == 'POST':
        try:
            # Obtener los datos del cuerpo de la solicitud (en formato JSON)
            data = json.loads(request.body)  # Cargar el JSON en un diccionario

            qr_data = data.get('qr_data')  # Obtener el valor del QR desde el JSON
            cantidad_=data.get('cantidad')
            
            if qr_data:
                # Guardar el QR en la base de datos
                QRCodeData.objects.create(data=qr_data,cantidad=cantidad_),
                return JsonResponse({'message': 'QR guardado correctamente'})
            else:
                return JsonResponse({'error': 'No se recibió ningún dato QR'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Error al procesar el JSON'}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

