from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
from django.shortcuts import get_object_or_404, redirect
from .models import salidasFruta, usuariosAppFruta, datosProduccion, detallesProduccion
from .forms import salidasFrutaForm


def obtener_nombre_usuario(request):
    # Obtén el nombre de usuario del usuario autenticado
    nombre_usuario = request.user.username
    return JsonResponse({'username': nombre_usuario})

def load_dataUsuario(request):
    correo_id = request.GET.get('category_id')
    datos = usuariosAppFruta.objects.filter(correo=correo_id).values('finca', 'encargado')
    adicionales = datosProduccion.objects.filter(finca=list(datos)[0]['finca'],status="Abierta").values('orden')
    return JsonResponse({'datos': list(datos),'correo':correo_id,'adicionales':list(adicionales)})

def load_dataUsuario2(request):
    ordenSelect = request.GET.get('category_id')
    cultivo= datosProduccion.objects.filter(orden=ordenSelect,status="Abierta").values('cultivo')
    variedad = detallesProduccion.objects.filter(cultivo=list(cultivo)[0]['cultivo']).values('variedad')
    return JsonResponse({'datos': list(cultivo),'variedad':list(variedad)})

def article_list(request):
    salidas = salidasFruta.objects.all()
    return render(request, 'plantaE/salidasFruta_list.html', {'registros': salidas})

def article_detail(request, pk):
    salidas = get_object_or_404(salidasFruta, pk=pk)
    return render(request, 'plantaE/salidasFruta_detail.html', {'registros': salidas})

def article_create(request):
    VALID_OPTIONS= {

        'finca':{'RIO','VALLE','CIP','FLE','PASTORIA'},
        'cultivo':{'MEDLEY','CHERRY','GRAPE','GRAPE ORGANICO','CHERRY ORGANICO','BLOCKY','BLOCKY ORGANICO','MINI','MINI ORGANICO','ROJO'},
        'encargado' : {'Brandon Portillo', 'Isaías García'},
        'variedad': {'BAMANO','IVORINO','DUNNE','KM 5512','NEBULA'},
        'orden': {'60202046','60206054','60206055','60206056'},
        'correo': {'brandon.portillo@popoyan.com.gt'}
    }
    if request.method == 'POST':
        form = salidasFrutaForm(request.POST)
        if form.is_valid():
            finca = form.cleaned_data['finca']
            cultivo = form.cleaned_data['cultivo']
            encargado = form.cleaned_data['encargado']
            variedad = form.cleaned_data['variedad']
            orden = form.cleaned_data['orden']
            correo = form.cleaned_data['correo']

            if finca in VALID_OPTIONS['finca'] or cultivo in VALID_OPTIONS['cultivo'] or encargado in VALID_OPTIONS['encargado'] or variedad in VALID_OPTIONS['variedad'] or orden in VALID_OPTIONS[orden] or correo in VALID_OPTIONS[correo]:
                form.save()
                return redirect('salidasFruta_list')
            else:
                return JsonResponse({'errores': form.errors}, status=400)
        
    else:
        form =salidasFrutaForm()
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