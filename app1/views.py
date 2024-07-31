from django.conf import settings
#import face_recognition as fr
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, FileResponse
from django.views import View 
from random import randint
from app1.models import *
#import imageio as imread
#from app1.rf import *
import cv2
import os
#from io import BytesIO
#from PIL import Image
import numpy as np
import base64
import datetime
from django.views.decorators.csrf import csrf_exempt
#from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from app1.forms import LoginForm
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_extra_fields.fields import Base64ImageField
import face_recognition as fr
# Create your views here.
from django.views.generic import TemplateView
from openpyxl import Workbook
from .forms import ImageUploadForm
from django.utils import timezone
import pytz
from django.contrib.auth import logout as django_logout

def logout_view(request):
    # Cerrar sesión localmente en Django
    django_logout(request)
    
    # Construir la URL de logout de ADFS
    adfs_logout_url = f"{settings.ADFS_LOGOUT_URL}?post_logout_redirect_uri={settings.LOGIN_REDIRECT_URI}"
    
    # Redirigir al usuario a la URL de logout de ADFS
    return redirect(adfs_logout_url)

def exportar_excel(request):
    # Crea un libro de Excel y una hoja
    wb = Workbook()
    ws = wb.active
    ws.title = 'Datos'

    # Obtén los datos de tu modelo
    datos = Ingresop.objects.all()

    

    # Especifica la zona horaria deseada
    zona_horaria_deseada = pytz.timezone('America/Guatemala')  # Cambia esto según sea necesario

    # Agrega los encabezados
    ws.append([field.name for field in Ingresop._meta.fields])
    # Agrega los datos  
    for obj in datos:
        row = []
        for field in Ingresop._meta.fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime):
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
def login_page(request):
    message = None
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    message = "Te has identificado de modo correcto"
                    
                else:
                    message = "Tu usuario está inactivo"
            else: 
                message = "Nombre de usuario y/o password incorrecto"
    else:
        form = LoginForm()
    context ={'message':message,
                'form':form
    }
    return render(request,'app1/login.html',context)

def homepage(request):
    return render(request,'app1/homepage.html')

def logout_view(request):
    logout(request)
    return redirect('homepage')

#@login_required
class consultarR(TemplateView):
    def get(self,request,*args,**kwargs):
        asistencias = Ingresop.objects.all()
        wb = Workbook()
        ws = wb.active
        ws['B1'] = 'Reporte de Asistencias'
        ws.merge_cells('B1:G1')
        ws['B3'] = 'Codigop'
        ws['C3'] = 'Nomprep'
        ws['D3'] = 'Fecha/Hora'
        ws['E3'] = 'Fecha'
        ws['F3'] = 'Origen'
        ws['G3'] = 'Evento'
        cont =  4
        for asistencia in asistencias:
            ws.cell(row = cont, column = 2).value = asistencia.codigop
            ws.cell(row = cont, column = 3).value = asistencia.nombrep
            ws.cell(row = cont, column = 4).value = asistencia.marcat
            ws.cell(row = cont, column = 5).value = asistencia.fecha
            ws.cell(row = cont, column = 6).value = asistencia.origen
            ws.cell(row = cont, column = 7).value = asistencia.evento
            cont = cont + 1 
        nombre_archivo = "ReporteAutorExcel.xlsx"
        response = HttpResponse(content_type = "application/ms-excel")
        content = "attachment; filename = {0}".format(nombre_archivo)
        response['Content-Disposition'] = content
        wb.save(response)
        return response
    
#@csrf_exempt
#@login_required
def consultaRegistros(request):
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

#    Sensor.objects.create(name='Presion Res1:' , tipo='Presion')
    today = timezone.now().date()

    # Filtrar los registros que tienen `created_at` en la fecha de hoy
    registros = Ingresop.objects.filter(fecha=today)
    registros = registros.order_by('-marcat')
#    sensores = TItems.objects.order_by('-id')[:3]
#    sensores = ["sensor 1","sensor 2","sensor 3","sensor 4","sensor 5","sensor 6"]
    
    context = {
        'registros': registros,
        'fecha': fecha_,
    }
    
    return render(request,'app1/registroConsulta.html',context) 

#@csrf_exempt
#@login_required
def registroPhoto(request):
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
    lista = ['1']

    for i in lista:

        total_ent= Ingresop.objects.filter(fecha = fecha_).filter(evento="Entrada")
        if total_ent == None:
            entradas = 0
        else:
            entradas = len(total_ent)
        total_sal= Ingresop.objects.filter(fecha = fecha_).filter(evento="Salida")
        if total_sal == None:
            salidas = 0
        else:
            salidas = len(total_sal)
#        ent = len(list(total_entradas.evento))
#        total_salidas= ingresoP.objects.get(fecha = fecha_,evento = "Salida").evento
#    if total_entradas ==None:
#        total_entradas=0
#    if total_salidas==None:
#        total_salidas=0 
    total = int(entradas)-int(salidas)
    path = 'home/bportillo/Proyecto1/web1/app1/static/app1'
    images = []
    clases = []
    lista = os.listdir(path)
#    registro = []
    comp1 = 100
    for i in lista:
        imgdb = cv2.imread(f'{path}/{i}')
        images.append(imgdb)
        clases.append(os.path.splitext(i)[0])
#         rostrosCod = codRostros(images)
    porcentaje = int(len(clases))
    listaCod = []
    for img in images:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        cod = fr.face_encodings(img)[0]
        listaCod.append(cod)

    mensaje = request.POST.get('array')
    
    if mensaje!=None:
         new_mensaje = str(mensaje).replace('[',  '')
         new_mensaje = new_mensaje.replace(']',  '')
         new_mensaje = new_mensaje.replace('"',  '')
         vector = new_mensaje.split(",")
#         path = 'home/bportillo/Proyecto1/web1/app1/static/app1/muestra.jpg'
         new_mensaje = vector[3] + "," + vector[4]
         new_mensaje = new_mensaje.replace('"','')
         new_mensaje = new_mensaje[new_mensaje.index(',')+1:]
#         response = {'mensaje':new_mensaje , 'vector':vector, 'saludo':"Brandon"}
        
         nparr= np.fromstring(base64.b64decode(new_mensaje),np.uint8)
         img = cv2.imdecode(nparr,cv2.IMREAD_COLOR)
         frame2 = cv2.resize(img,(0,0),None,0.25,0.25)
         rgb = cv2.cvtColor(frame2,cv2.COLOR_BGR2RGB)
         faces = fr.face_locations(rgb)
         facesCod = fr.face_encodings(rgb,faces)
         contador = 0
         for facecod, faceloc in zip(facesCod,faces):
            
            comparacion = fr.compare_faces(listaCod,facecod)
            simi = fr.face_distance(listaCod,facecod)
            min = np.argmin(simi)

            contador = contador + 1
            if comparacion[min]:
                codigoE = clases[min].upper()

                yi, xf, yf, xi = faceloc
                yi, xf, yf, xi = yi*4, xf*4, yf*4, xi*4

                #indice = comparacion.index(True)

            #if comp1!= indice:
            #    comp1 = indice

            #if comp1 == indice:
                nombreT = Listapersonal.objects.get(codigop=str(codigoE))
                #nombreT = "Brandon"
                marcaT = datetime.datetime.now()
                nombre = nombreT.nombrep
                #nombre = nombreT
                fechaT = vector[0]
                origenT = vector[1]
                eventoT= vector[2]
                if eventoT == "Entrada":
                    saludo = "Bienvenido " + nombre
                elif eventoT =="Salida":
                    saludo = "Excelente día " + nombre

                response = {'codigoP':codigoE,'marcaT':marcaT,'photo':new_mensaje,'saludo':saludo,'total':total,'p':porcentaje}
                Ingresop.objects.create(codigop=codigoE,nombrep=nombre,marcat=marcaT,fecha=fechaT,origen=origenT,evento=eventoT)
         if contador == 0:    
             nombre = "DESCONOCIDO"
             saludo = "USUARIO NO REGISTRADO"
             response = {'codigoP':nombre,'photo':new_mensaje, 'saludo':saludo, 'aux':vector}
##         response = {'photo':vector, 'imagen':new_mensaje}
         return JsonResponse(response)

    else:
         saludo = ""
         response = {'codigoP':0,'marcaT':0,'photo':0,'mensaje':'None', 'fecha' : fecha_, 'saludo':saludo,'total':total,'p':porcentaje}
##         response = {'mensaje':new_mensaje}
    return render(request,'app1/reconocimientof.html',response)
#@login_required
#@csrf_exempt
def vector_prueba(request):
#    Sensor.objects.create(name='Presion Res1:' , tipo='Presion')
    items = TItem.objects.all()
    centros = TCentros.objects.all()
    despachos = TDespachos.objects.latest("envio")
#    sensores = TItems.objects.order_by('-id')[:3]
#    sensores = ["sensor 1","sensor 2","sensor 3","sensor 4","sensor 5","sensor 6"]
    now = datetime.datetime.now()
    fecha = now.date()
    dia= fecha.day
    mes= fecha.month
    año= fecha.year
    if mes < 10:
        mes = "0" + str(mes)
    fecha_= "{}-{}-{}".format(str(año),str(mes),str(dia))
    requis = str(despachos.envio)  
    context = {
        'sensores': items,
        'centros': centros,
        'fecha' : fecha_,
        'correlativo' : str(despachos),
    }

    mensaje = request.POST.get('array', None)

    if mensaje != None:
        new_mensaje = str(mensaje).replace('[',  '')
        new_mensaje = new_mensaje.replace(']',  '')
        new_mensaje = new_mensaje.replace('"',  '')
        vector = new_mensaje.split(",")
        a = 1
        matriz = []
        fila = []
        for i in vector:
            fila.append(i)
            a +=1
            if a ==11:
                matriz.append(fila)
                fila=[]
                a=1

        if requis == str(TDespachos.objects.latest("envio").envio):
                requis = int(requis) + 1

        items = TItems.objects.all()
        centros = TCentros.objects.all()
        for i in range(len(matriz)):
            print(matriz[i])
            
            if i > 0:
#                print(f'TDespachos.objects.create(mtemporal={now} , fecha={fecha_},origen="RLemus",rubro={matriz[i][7]},citem={matriz[i][0]},cantidad={matriz[i][2]},ccentro={matriz[i][4]})')
                TDespachos.objects.create(mtemporal=now , fecha=matriz[i][8],envio=requis,origen=matriz[i][9],rubro=matriz[i][7],citem=matriz[i][0],cantidad=matriz[i][2],ccentro=matriz[i][4])
                
    return render(request,'app1/iniciar_pedido.html',context) 

#@csrf_exempt
#@login_required
def repuesta(request):

    mensaje = request.POST.get('data', None)
    print(f'data: {mensaje}')
#    EjemploMedicion.objects.create(valor=valor_aleatorio)
#   mediciones = EjemploMedicion.objects.order_by('-created')[:5]
#    nombre = request.POST.get('nombre',None)
#    carnet = request.POST.get('carnet',None)
#    edad = request.POST.get('edad',None)
#    print(nombre,carnet,edad)

    temporal = list()

#    for medicion in mediciones:
#        temporal.append(medicion.valor)

    data = {
        'mediciones': mensaje
    }

#    print(temporal)
    return JsonResponse(data)

#@csrf_exempt
#@login_required
def vector_prueba2(request):

    despachos = TDespachos.objects.latest("envio")
    correlativo = int(str(despachos.envio))+1
    now = datetime.datetime.now()

    fecha = now.date()
    dia= fecha.day
    mes= fecha.month
    año= fecha.year
    
    if mes < 10:
        mes = "0" + str(mes)
    fecha_= "{}-{}-{}".format(str(año),str(mes),str(dia))

   
    context = {
        "fecha" : fecha_,
        "correlativo" : correlativo,
        "pedido": "",
    }

    mensaje = request.POST.get('array', None)
    requis = str(despachos.envio)

    if mensaje != None:
        new_mensaje = str(mensaje).replace('[',  '')
        new_mensaje = new_mensaje.replace(']',  '')
        new_mensaje = new_mensaje.replace('"',  '')
        vector = new_mensaje.split(",")
        a = 1
        if vector[0] != "excel-file":
            matriz = []
            fila = []
            print(vector[0])
            for i in vector:
                fila.append(i)
                a +=1

                if a == 8:
                    matriz.append(fila)
                    fila=[]
                    a=1
            
            if requis == str(TDespachos.objects.latest("envio").envio):
                    requis = int(requis) + 1

            now = datetime.datetime.now()
#            despachos=TDespachos.objects.filter(envio=int(requis)-1)   
            for i in matriz:

                itemrow=TItems.objects.get(código_articulo=str(i[1]))
                centrorow=TCentros.objects.get(centro=str(i[3]))
                TDespachos.objects.create(mtemporal=now , fecha=i[6],envio=requis,origen=i[5],rubro=i[4],citem=i[1],cantidad=i[2],ccentro=i[3])
 
        else:
            matriz = []
            fila = []
            
            for i in vector:
                
                fila.append(i)
                a +=1

                if a == 5:
                    matriz.append(fila)
                    fila=[]
                    a=1
                
#            for i in range(len(matriz)):

#                if i > 0:
#                    pass
    #                itemrow=TItems.objects.get(código_articulo=str(matriz[i][0]))
    #                centrorow=TCentros.objects.get(centro=str(matriz[i][2]))
    #                itemrow.artículo
    #                itemrow.unidad_medida
    #                centrorow.descripción
    #                print(f'TDespachos.objects.create(mtemporal={now} , fecha={fecha_},origen="RLemus",rubro={matriz[i][7]},citem={matriz[i][0]},cantidad={matriz[i][2]},ccentro={matriz[i][4]})')
    #                TDespachos.objects.create(mtemporal=now , fecha=matriz[i][4],envio=requis,origen=matriz[i][5],rubro=matriz[i][3],citem=matriz[i][0],cantidad=matriz[i][1],ccentro=matriz[i][2])
            pedido = []
#            despachos=TDespachos.objects.filter(envio=int(requis)-1)   
            for i in matriz:
                itemrow=TItems.objects.get(código_articulo=str(i[1]))
                centrorow=TCentros.objects.get(centro=str(i[3]))

                pedido.append([i[1],itemrow.artículo,i[2],itemrow.unidad_medida,i[3],centrorow.descripción])
            respuesta = {
            "pedido": pedido,
            } 
            return JsonResponse(respuesta)
  
    
    return render(request,'app1/pedido_masivo.html',context) 


#@csrf_exempt
#@login_required
def vector_prueba4(request):
    despachos = TDespachos.objects.latest("envio")
    correlativo = int(str(despachos.envio))+1
    now = datetime.datetime.now()

    fecha = now.date()
    dia= fecha.day
    mes= fecha.month
    año= fecha.year
    
    if mes < 10:
        mes = "0" + str(mes)
    fecha_= "{}-{}-{}".format(str(año),str(mes),str(dia))

   
    context = {
        "fecha" : fecha_,
        "correlativo" : correlativo,
        "pedido": "",
    }

    mensaje = request.POST.get('array', None)
    
    if mensaje != None:
        
        new_mensaje = str(mensaje).replace('[',  '')
        new_mensaje = new_mensaje.replace(']',  '')
        new_mensaje = new_mensaje.replace('"',  '')
        vector = new_mensaje.split(",")
        pedido = []
        for i in range(len(vector)):
            if i ==0:
                itemrow=TItems.objects.get(código_articulo=str(vector[i]))
                pedido.append(itemrow.artículo)
                pedido.append(itemrow.unidad_medida)
            if i == 2:
                centrorow=TCentros.objects.get(centro=str(vector[i]))
                pedido.append(centrorow.descripción)
        vector.extend(pedido)

        #                TDespachos.objects.create(mtemporal=now , fecha=matriz[i][4],envio=requis,origen=matriz[i][5],rubro=matriz[i][3],citem=matriz[i][0],cantidad=matriz[i][1],ccentro=matriz[i][2])
#            despachos=TDespachos.objects.filter(envio=int(requis)-1)   
        

        print(vector)

        respuesta = {
        "pedido": vector,
        } 

        return JsonResponse(respuesta)
    
    return render(request,'app1/iniciar_pedido_conv_panel.html',context) 

#@csrf_exempt
#@login_required
def vector_prueba3(request):
#    Sensor.objects.create(name='Presion Res1:' , tipo='Presion')
    items = TItem.objects.all()
    centros = TCentros.objects.all()
#    sensores = TItems.objects.order_by('-id')[:3]
#    sensores = ["sensor 1","sensor 2","sensor 3","sensor 4","sensor 5","sensor 6"]
    
    context = {
        'sensores': items,
        'centros': centros,
    }
    
    return render(request,'app1/iniciar_pedido_conv_carrito.html',context) 
