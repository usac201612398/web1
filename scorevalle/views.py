from django.shortcuts import render
import datetime
from django.http import JsonResponse
from models import scorepersonal
# Create your views here.

def index(request):

    salidas = scorepersonal.objects.filter(area="Cosecha")
    
    return render(request, 'scorevalle/menu.html', {'registros': salidas})

def obtener_nombre_usuario(request):
    # Obtén el nombre de usuario del usuario autenticado
    now = datetime.datetime.now()
    fecha = now.date()
    dia= fecha.day
    mes= fecha.month
    año= fecha.year
    if mes < 10:
        mes = "0" + str(mes)
    if dia < 10:
        dia = "0" + str(dia)
    fecha_= "{}-{}-{}".format(str(año),str(mes),str(dia))
    nombre_usuario = request.user.username
    
    return JsonResponse({'username': nombre_usuario,'fecha':fecha_})
