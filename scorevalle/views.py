from django.shortcuts import render
import datetime
from django.http import JsonResponse
from .models import scorepersonal, scorecosecha, scoremanejo
from .forms import scorepersonalForm, scorecosechaForm,scoremanejoForm

from django.shortcuts import get_object_or_404, redirect
import json


def index(request):

    salidas = scorepersonal.objects.all()
    
    return render(request, 'scorevalle/menu.html', {'registros': salidas})

def scoremanejo_(request):

   # Obtener la fecha actual
    fecha_actual = datetime.datetime.now()

    # Obtener el número de semana y el año actuales
    numero_semana_actual = fecha_actual.isocalendar()[1]
    año_actual = fecha_actual.year

    # Filtrar los registros de scoremanejo donde el número de semana y el año sean los actuales
    salidas = scoremanejo.objects.filter(semana=numero_semana_actual, año=año_actual)
    
    
    return render(request, 'scorevalle/scoremanejo.html', {'registros': salidas})

def scorecosecha_(request):
    # Obtener la fecha actual
    fecha_actual = datetime.datetime.now()

    # Obtener el número de semana y el año actuales
    numero_semana_actual = fecha_actual.isocalendar()[1]
    año_actual = fecha_actual.year
    salidas = scorecosecha.objects.filter(semana=numero_semana_actual, año=año_actual)
    
    return render(request, 'scorevalle/scorecosecha.html', {'registros': salidas})

def guardar_score(request):
    data = json.loads(request.body)
    mensaje = data['array']
    #mensaje = request.POST.get('array')
    
    
    
    for i in mensaje:

        fecha = datetime.datetime.strptime(i[7], "%Y-%m-%d")  # Ajusta el formato si es necesario

        # Obtener el número de la semana
        numero_semana = fecha.isocalendar()[1]
        año_ = fecha.year  # Obtener el año de la fecha

        if i[6] == "Cosecha":

            scorecosecha.objects.create(finca=i[0],encargado=i[1],cuadrilla=i[2],codigop=i[3],nombrep=i[4],estructura=i[5],area=i[6],fecha=i[7],semana=numero_semana,año=año_)
        else:

            scoremanejo.objects.create(finca=i[0],encargado=i[1],cuadrilla=i[2],codigop=i[3],nombrep=i[4],estructura=i[5],area=i[6],fecha=i[7],semana=numero_semana,año=año_)
        

    
    return JsonResponse({'mensaje':list(mensaje)})                  


def obtener_nombre_usuario_scoresdc(request):
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

def actualizar_scorepersonal(request, pk):
    # Obtener el registro a partir del qr_data
    registro = get_object_or_404(scorepersonal, pk=pk)
    
    if request.method == "POST":
        form = scorepersonalForm(request.POST, instance=registro)
        
        if form.is_valid():
            form.save()  # Guardar los cambios en la base de datos
            return redirect('index')  # Redirigir a una página de éxito o el detalle del registro actualizado
    else:
        form = scorepersonalForm(instance=registro)  # Mostrar el formulario con los datos actuales

    return render(request, 'scorevalle/edit_menu.html', {'form': form})

def actualizar_scoremanejo(request, pk):
    # Obtener el registro a partir del qr_data
    registro = get_object_or_404(scoremanejo, pk=pk)
    
    if request.method == "POST":
        form = scoremanejoForm(request.POST, instance=registro)
        
        if form.is_valid():
            form.save()  # Guardar los cambios en la base de datos
            return redirect('scorevalle_manejo')  # Redirigir a una página de éxito o el detalle del registro actualizado
    else:
        form = scoremanejoForm(instance=registro)  # Mostrar el formulario con los datos actuales

    return render(request, 'scoremanejo/edit_manejo.html', {'form': form})

def actualizar_scorecosecha(request, pk):
    # Obtener el registro a partir del qr_data
    registro = get_object_or_404(scorecosecha, pk=pk)
    
    if request.method == "POST":
        form = scorecosechaForm(request.POST, instance=registro)
        
        if form.is_valid():
            form.save()  # Guardar los cambios en la base de datos
            return redirect('scorevalle_cosecha')  # Redirigir a una página de éxito o el detalle del registro actualizado
    else:
        form = scorecosechaForm(instance=registro)  # Mostrar el formulario con los datos actuales

    return render(request, 'scorevalle/edit_cosecha.html', {'form': form})
