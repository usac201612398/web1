from django.shortcuts import render
from django.http import JsonResponse
import logging
# Create your views here.
from django.shortcuts import get_object_or_404, redirect
from .models import detallerecaux,detallerec,salidasFruta, usuariosAppFruta, datosProduccion, detallesProduccion, detallesEstructuras, Recepciones, Ccalidad,causasRechazo,inventarioProdTerm,productoTerm,cultivoxFinca,AcumFruta
from .forms import salidasFrutaForm, recepcionesForm, ccalidadForm, inventarioFrutaForm, acumFrutaForm
from django.db.models import Sum
from django.utils import timezone
import datetime
import json

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

def obtenerfecha_invFruta(request):
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
    return JsonResponse({'fecha':fecha_})


def load_dataUsuario(request):
    correo_id = request.GET.get('category_id')
    datos = usuariosAppFruta.objects.filter(correo=correo_id).values('finca', 'encargado')
    adicionales = cultivoxFinca.objects.filter(finca=list(datos)[0]['finca']).values('cultivo').distinct('cultivo')
    adicionales_ = datosProduccion.objects.filter(finca=list(datos)[0]['finca']).values('orden').distinct('orden')
    return JsonResponse({'datos': list(datos),'correo':correo_id,'adicionales':list(adicionales),'ordenes':list(adicionales_)})

def load_dataUsuario2(request):
    ordenSelect = request.GET.get('category_id')

    cultivo= datosProduccion.objects.filter(orden=ordenSelect,status="Abierta").values('cultivo')
    variedad = detallesProduccion.objects.filter(cultivo=list(cultivo)[0]['cultivo']).values('variedad')
    estructura = detallesEstructuras.objects.filter(orden=ordenSelect).values('estructura')
    return JsonResponse({'datos': list(cultivo),'variedad':list(variedad),'estructura':list(estructura),'orden':ordenSelect})

def load_dataUsuario3(request):
    cultivo_ = request.GET.get('category_id')
    finca_ = request.GET.get('finca')
    variedad= cultivoxFinca.objects.filter(finca=finca_,cultivo=cultivo_).values('variedad').distinct('variedad')
    #variedad = cultivoxFinca.objects.filter(cultivo=list(cultivo)[0]['cultivo']).values('variedad')
    return JsonResponse({'datos': list(variedad)})

def article_list(request):
    today = timezone.now().date()
    salidas = salidasFruta.objects.filter(fecha=today)
    salidas = salidas.order_by('-created_at')
    
    return render(request, 'plantaE/salidasFruta_list.html', {'registros': salidas})

def article_detail(request, pk):
    salidas = get_object_or_404(salidasFruta, pk=pk)
    return render(request, 'plantaE/salidasFruta_detail.html', {'registros': salidas})

def guardar_plantilla(request):
    data = json.loads(request.body)
    mensaje = data['array']
    #mensaje = request.POST.get('array')
    for i in mensaje:
        
        AcumFruta.objects.create(fecha=i[8],finca=i[7],orden=i[1],cultivo=i[2],estructura=i[3],variedad=i[4],cajas=i[5],correo=i[9])
        
    return JsonResponse({'mensaje':mensaje})                

def article_create_plantilla(request):
    
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
    datos = usuariosAppFruta.objects.filter(correo=nombre_usuario).values('finca','encargado')
    estructura = detallesEstructuras.objects.filter(finca=list(datos)[0]['finca']).values('finca','orden','estructura','variedad','cultivo').distinct()
    estructura = estructura.order_by('estructura')
    context = {

        'usuario': nombre_usuario,
        'registros': list(estructura),
        'fecha': fecha_,
        'encargado': list(datos)[0]['encargado']
    }
    
    return render(request, 'plantaE/salidasFruta_envio.html',context)

def article_create(request):
    if request.method == 'POST':
        form = salidasFrutaForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                # Manejar excepciones específicas (por ejemplo, UniqueConstraintError)
                return JsonResponse({'error': str(e)}, status=400)
            return redirect('salidasFruta_list')
        else:
             # Imprimir errores para depuración
            return JsonResponse({'errores': form.errors}, status=400)
    else:
        form = salidasFrutaForm()
    return render(request, 'plantaE/salidasFruta_form.html', {'form': form})

def article_update(request, pk):
    salidas = get_object_or_404(salidasFruta, pk=pk)
    if request.method == 'POST':
        form = salidasFrutaForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('salidasFruta_list')
    else:
        form = salidasFrutaForm(instance=salidas)
    return render(request, 'plantaE/salidasFruta_form.html', {'form': form})

def article_delete(request, pk):
    salidas = get_object_or_404(salidasFruta, pk=pk)
    if request.method == 'POST':
        salidas.delete()
        return redirect('salidasFruta_list')
    return render(request, 'plantaE/salidasFruta_confirm_delete.html', {'registros': salidas})

def acumFruta_list(request):
    today = timezone.now().date()
    salidas = AcumFruta.objects.filter(fecha=today)
    salidas = salidas.order_by('-created_at')
    
    return render(request, 'plantaE/AcumFrutaDia_list.html', {'registros': salidas})

def acumFruta_detail(request, pk):
    salidas = get_object_or_404(AcumFruta, pk=pk)
    return render(request, 'plantaE/AcumFrutaDia_detail.html', {'registros': salidas})

def  acumFruta_create(request):
    if request.method == 'POST':
        form = acumFrutaForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                # Manejar excepciones específicas (por ejemplo, UniqueConstraintError)
                return JsonResponse({'error': str(e)}, status=400)
            return redirect('acumFruta_list')
        else:
             # Imprimir errores para depuración
            return JsonResponse({'errores': form.errors}, status=400)
    else:
        form = acumFrutaForm()
    return render(request, 'plantaE/AcumFrutaDia_form.html', {'form': form})

def acumFruta_update(request, pk):
    salidas = get_object_or_404(AcumFruta, pk=pk)
    if request.method == 'POST':
        form = acumFrutaForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('acumFruta_list')
    else:
        form = acumFrutaForm(instance=salidas)
    return render(request, 'plantaE/AcumFrutaDia_form.html', {'form': form})

def acumFruta_delete(request, pk):
    salidas = get_object_or_404(AcumFruta, pk=pk)
    if request.method == 'POST':
        salidas.delete()
        return redirect('acumFruta_list')
    return render(request, 'plantaE/acumFruta_confirm_delete.html', {'registros': salidas})

def procesarrecepcion(request):
    data = json.loads(request.body)
    mensaje = data['array']
    #mensaje = request.POST.get('array')
    #for i in mensaje:
        
    #    AcumFruta.objects.create(fecha=i[8],finca=i[7],orden=i[1],cultivo=i[2],estructura=i[3],variedad=i[4],cajas=i[5],correo=i[9])
        
    return JsonResponse({'mensaje':mensaje})   

def recepciones_list(request):
    today = timezone.now().date()
    #salidas = Recepciones.objects.filter(fecha=today)
    salidas= detallerec.objects.all()
    salidas2= detallerecaux.objects.all()
    salidas = salidas.order_by('-created').filter(status=None)
    
    for i in salidas:
        cajasacum = salidas2.order_by('-created').filter(status="En Proceso",recepcion=i.recepcion).aggregate(sumacajas=Sum('cajas'))['sumacajas']
        librasacum = salidas2.order_by('-created').filter(status="En Proceso",recepcion=i.recepcion).aggregate(sumalibras=Sum('libras'))['sumalibras']    
        if librasacum != None and cajasacum != None:
            i.cajas = i.cajas - int(cajasacum)
            i.libras = i.libras - float(librasacum)
        

    #existenciaCajas = finca=list(salidas)[0]['cajas']
    #existenciaLibras = finca=list(salidas)[0]['libras']
    #rebajaCajas = finca=list(salidas2)[0]['cajas']
    #rebajaLibras = finca=list(salidas2)[0]['libras']
    #for i in len(salidas):
    #    existenciaCajas 
    return render(request, 'plantaE/recepciones_list.html', {'registros': salidas})

def recepciones_detail(request, pk):
    salidas = get_object_or_404(detallerec, pk=pk)
    return render(request, 'plantaE/recepciones_detail.html', {'registros': salidas})

def recepciones_update(request, pk):
    salidas = get_object_or_404(detallerec, pk=pk)
    if request.method == 'POST':
        form = recepcionesForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('recepcionesFruta_list')
        else:
            return JsonResponse({'errores': form.errors}, status=400)
    else:
        form = recepcionesForm(instance=salidas)
    return render(request, 'plantaE/recepciones_form.html', {'form': form})

def ccalidad_list(request):
    salidas = Ccalidad.objects.all()
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
    return render(request, 'plantaE/ccalidad_form.html', {'form': form})

def ccalidad_update(request, pk):
    salidas = get_object_or_404(Ccalidad, pk=pk)
    if request.method == 'POST':
        form = ccalidadForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('ccalidad_list')
    else:
        form = ccalidadForm(instance=salidas)
        
    return render(request, 'plantaE/ccalidad_form_edit.html', {'form': form})

def ccalidad_update_aux(request):
    pk = request.GET.get('pk')
    salidas = get_object_or_404(Ccalidad, pk=pk)
    causa_rechazo = causasRechazo.objects.all().values('causa')
    return JsonResponse({'llave': salidas.llave,'recepcion':salidas.recepcion,'causa_select':salidas.causarechazo,'causas':list(causa_rechazo)})
    

def ccalidad_delete(request, pk):
    salidas = get_object_or_404(Ccalidad, pk=pk)
    if request.method == 'POST':
        salidas.delete()
        return redirect('ccalidad_list')
    return render(request, 'plantaE/ccalidad_confirm_delete.html', {'registros': salidas})

def obtener_llave_recepcion(request):
    # Obtén el nombre de usuario del usuario autenticado
    llave_recepcion = Recepciones.objects.values('criterio').distinct('criterio')
    causa_rechazo = causasRechazo.objects.all().values('causa')
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
    return JsonResponse({'llaves': list(llave_recepcion),'causa':list(causa_rechazo),'fecha':fecha_})

def load_ccalidadparam(request):
    llave_recepcion = request.GET.get('category_id')
    datos = Recepciones.objects.filter(criterio=llave_recepcion).values('recepcion').distinct('recepcion')
    valor = Ccalidad.objects.filter(llave=llave_recepcion).aggregate(suma=Sum('porcentaje'))['suma']
    if valor != None:
        valor = 1-float(Ccalidad.objects.filter(llave=llave_recepcion).aggregate(suma=Sum('porcentaje'))['suma'])
    else:
        valor=1
    return JsonResponse({'datos': list(datos),'valor':valor})

def inventarioProd_list(request):
    salidas = inventarioProdTerm.objects.all()
    return render(request, 'plantaE/inventarioProd_list.html', {'registros': salidas})

def inventarioProd_detail(request, pk):
    salidas = get_object_or_404(inventarioProdTerm, pk=pk)
    return render(request, 'plantaE/inventarioProd_detail.html', {'registros': salidas})

def inventarioProd_create(request):
    if request.method == 'POST':
        form = inventarioFrutaForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                # Manejar excepciones específicas (por ejemplo, UniqueConstraintError)
                return JsonResponse({'error': str(e)}, status=400)
            return redirect('inventarioProd_list')
        else:
             # Imprimir errores para depuración
            return JsonResponse({'errores': form.errors}, status=400)
    else:
        form = inventarioFrutaForm()
    return render(request, 'plantaE/inventarioProd_form.html', {'form': form})

def inventarioProd_delete(request, pk):
    salidas = get_object_or_404(inventarioProdTerm, pk=pk)
    if request.method == 'POST':
        salidas.delete()
        return redirect('inventarioProd_list')
    return render(request, 'plantaE/inventarioProd_confirm_delete.html', {'registros': salidas})

def load_inventarioProdparam(request):
    cultivo_ = request.GET.get('campo1')
    categoria_ = request.GET.get('campo2')

    if cultivo_ != None and categoria_ != None:
        datos = productoTerm.objects.filter(cultivo=cultivo_,categoria=categoria_).values('calidad1')
    
    return JsonResponse({'datos': list(datos),'cultivo':cultivo_,'categoria':categoria_})

def plantaEhomepage(request):
    return render(request,'plantaE/plantaE_home.html')