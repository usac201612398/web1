from django.shortcuts import render
import datetime
from django.http import JsonResponse
from .models import scorepersonal
import json
# Create your views here.

def index(request):

    salidas = scorepersonal.objects.filter(area="Cosecha")
    
    return render(request, 'scorevalle/menu.html', {'registros': salidas})

def guardar_scorecosecha(request):
    data = json.loads(request.body)
    mensaje = data['array']
    #mensaje = request.POST.get('array')
    '''
    for elemento in mensaje:
        elemento[5] = int(elemento[5])

    df = pd.DataFrame(mensaje,columns=['Encargado','Orden','Cultivo','Estructura','Variedad','Cajas','Blank','Finca','Viaje','Fecha','Correo'])
    
    resultado = df.groupby(['Variedad','Orden'] ).agg({
        'Encargado': 'first',  # O 'last', 'min', 'max', etc.
        'Cultivo': 'first',
        'Finca': 'first',
        'Viaje': 'first',
        'Fecha': 'first',
        'Correo': 'first',
        'Cajas': 'sum'
    }).reset_index()
    resultado_lista = resultado.to_dict(orient='records')
     # Creación de registros en la base de datos
    for i in resultado_lista:
        salidasFruta.objects.create(
            fecha=i['Fecha'],       # Ajusta el nombre según tu modelo
            finca=i['Finca'],
            encargado=i['Encargado'],
            cultivo=i['Cultivo'],
            variedad=i['Variedad'],
            cajas=i['Cajas'],
            viaje=i['Viaje'],
            correo=i['Correo']
        )
    
    for i in mensaje:
        
        AcumFruta.objects.create(fecha=i[9],finca=i[7],orden=i[1],cultivo=i[2],estructura=i[3],variedad=i[4],cajas=i[5],correo=i[10],viaje=i[8])
    
    '''
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
