from django.shortcuts import render
from django.http import JsonResponse
from .models import QRCodeData

def index(request):
    return render(request, 'escanerqr.html')

def save_qr(request):
    if request.method == 'POST':
        qr_data = request.POST.get('qr_data')
        if qr_data:
            # Guardar el QR en la base de datos
            QRCodeData.objects.create(data=qr_data)
            return JsonResponse({'message': 'QR guardado correctamente'})
        else:
            return JsonResponse({'error': 'No se recibió ningún dato QR'}, status=400)
        
    return JsonResponse({'error': 'Método no permitido'}, status=405)

