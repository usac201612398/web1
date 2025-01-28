from django.shortcuts import render
import datetime
from django.http import JsonResponse, HttpResponse
from .models import scorepersonal, scorecosecha, scoremanejo
from .forms import scorepersonalForm, scorecosechaForm,scoremanejoForm
from openpyxl import Workbook
from django.shortcuts import get_object_or_404, redirect
import json
import pandas as pd
import pytz

def exportar_excel(request):
    
    # Crea un libro de Excel y una hoja
    wb = Workbook()
    ws = wb.active
    ws.title = 'Manejo'

    # Obtén los datos de tu modelo
    datos = scorecosecha.objects.all()

    # Especifica la zona horaria deseada
    zona_horaria_deseada = pytz.timezone('America/Guatemala')  # Cambia esto según sea necesario

    # Agrega los encabezados
    ws.append([field.name for field in scoremanejo._meta.fields])
    # Agrega los datos  
    for obj in datos:
        row = []
        for field in scoremanejo._meta.fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                # Convertir a la zona horaria deseada
                if value.tzinfo is not None:
                    value = value.astimezone(zona_horaria_deseada)
                    value = value.replace(tzinfo=None)  # Eliminar la zona horaria para ser compatible con Excel
            row.append(value)
        ws.append(row)
    ws_cosecha = wb.create_sheet(title='Cosecha')
    # Agrega los encabezados
    ws_cosecha.append([field.name for field in scorecosecha._meta.fields])
    # Agrega los datos  
    for obj in datos:
        row = []
        for field in scorecosecha._meta.fields:
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

def index(request):
    # Obtener todos los registros de scorepersonal
    salidas = scorepersonal.objects.all()

    # Obtener la fecha actual
    fecha_actual = datetime.datetime.now()

    # Obtener el número de semana y el año actuales
    numero_semana_actual = fecha_actual.isocalendar()[1]
    año_actual = fecha_actual.year

    # Obtener registros de scoremanejo y scorecosecha de la semana y año actuales
    manejo_sem = scoremanejo.objects.filter(semana=numero_semana_actual, año=año_actual)
    cosecha_sem = scorecosecha.objects.filter(semana=numero_semana_actual, año=año_actual)

    # Filtrar los registros que no están en scoremanejo ni scorecosecha según el área
    registros_filtrados = []

    for i in salidas:
        # Si el área es "Manejo", solo comprobar en scoremanejo
        if i.area == "Manejo":
            if not manejo_sem.filter(cuadrilla=i.cuadrilla, codigop=i.codigop).exists():
                registros_filtrados.append(i)
        # Si el área es "Cosecha", solo comprobar en scorecosecha
        elif i.area == "Cosecha":
            if not cosecha_sem.filter(cuadrilla=i.cuadrilla, codigop=i.codigop).exists():
                registros_filtrados.append(i)

    # Renderizar la plantilla con los registros filtrados (sin los eliminados)
    return render(request, 'scorevalle/menu.html', {'registros': registros_filtrados})



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

        fecha = datetime.datetime.strptime(i[9], "%Y-%m-%d")  # Ajusta el formato si es necesario

        # Obtener el número de la semana
        numero_semana = fecha.isocalendar()[1]
        año_ = fecha.year  # Obtener el año de la fecha

        if i[6] == "Cosecha":

            scorecosecha.objects.create(finca=i[0],encargado=i[1],cuadrilla=i[2],codigop=i[3],nombrep=i[4],estructura=i[5],area=i[6],fecha=i[9],semana=numero_semana,año=año_)
        else:

            scoremanejo.objects.create(finca=i[0],encargado=i[1],cuadrilla=i[2],codigop=i[3],nombrep=i[4],estructura=i[5],area=i[6],fecha=i[9],semana=numero_semana,año=año_)
        

    
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

    return render(request, 'scorevalle/edit_manejo.html', {'form': form})

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
