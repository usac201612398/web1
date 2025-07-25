from django.shortcuts import render
from .models import *
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from.forms import *
from django.contrib import messages
from datetime import date
import calendar
import json
from openpyxl import Workbook
from django.apps import apps
from django.http import HttpResponse

def sdcsemillashomepage(request):
    return render(request,'sdcsemillas/sdcsemillas_home.html')

def exportar_excel_generico(request, nombre_modelo):
    # Obtiene el modelo desde el nombre
    try:
        Modelo = apps.get_model('sdcsemillas', nombre_modelo)
    except LookupError:
        return HttpResponse("Modelo no encontrado", status=404)

    # Crear libro y hoja
    wb = Workbook()
    ws = wb.active
    ws.title = nombre_modelo

    EXPORT_FIELDS = {
        'operariosApp': ['codigo_empleado', 'codigoevo', 'nombre_operario','codigo_lote','camas','supervisor','status'],
        'lotes': ['lote_code', 'variedad_code','apodo_variedad','cultivo','ubicación','estructura','plantas_padre','plantas_madre','harvest_code','status','siembra_madre','metodo_prod','target','surface','tipo','shipment_hub','as_per_SDCMale','as_per_SDCFemale','observaciones'],
        'variedades': ['variedad_codigo', 'apodo_variedad', 'cultivo','cod_padre','cod_madre','status'],
        'conteoplantas': ['codigo_lote', 'operario_name','codigo_empleado','supervisor_name','ubicacion_lote','estructura','apodo_variedad','tipo_cultivo','codigo_madre','codigo_planta','plantas_activas','plantas_faltantes','fecha','camas_incompletas','camas_completas','cocosxcamaincompleta','evento','status','observaciones'],
        'conteosemillas': ['codigo_lote', 'operario_name','codigo_empleado','supervisor_name','ubicacion_lote','estructura','apodo_variedad','tipo_cultivo','fecha','camas_incompletas','cantidad_frutos','semillasxfruto','prom_semillasxfruto','nsemana','clasificacion','status','observaciones'],
        'conteofrutosplanilla': ['codigo_lote', 'operario_name','codigo_empleado','supervisor_name','ubicacion_lote','estructura','apodo_variedad','tipo_cultivo','fecha','cama1','cama2','cama3','cama4','cama5','media','prom_area','prom_general','status','observaciones'],
        'conteofrutos': ['codigo_lote', 'operario_name','codigo_empleado','supervisor_name','ubicacion_lote','estructura','apodo_variedad','tipo_cultivo','fecha','prom_autopolinizados','prom_floresabiertas','prom_polinizados','evento','status','observaciones'],
        'etapasdelote': ['codigo_lote', 'operario_name','codigo_empleado','supervisor_name','ubicacion_lote','estructura','apodo_variedad','tipo_cultivo','fecha','codigo_padre','codigo_madre','evento','status','observaciones'],
        'ccalidadpolen': ['codigo_lote', 'operario_name','codigo_empleado','supervisor_name','ubicacion_lote','estructura','apodo_variedad','tipo_cultivo','fecha','calidad','consistencia','ag_externos','status','observaciones'],
        'indexpolinizacion': ['codigo_lote', 'operario_name','codigo_empleado','supervisor_name','ubicacion_lote','estructura','apodo_variedad','tipo_cultivo','fecha','diasemana','color_lana','cantidad_camas','cantidad_index','cama1','cama2','cama3','cama4','cama5','media','total_index','status','observaciones'],
        'floresabiertas': ['codigo_lote', 'operario_name','codigo_empleado','supervisor_name','ubicacion_lote','estructura','apodo_variedad','tipo_cultivo','fecha','diasemana','nsemana','flores_abiertas','flores_antenas','flores_polinizadas','flores_enmasculadas','flores_sinpistilo','flores_viejas','boton_pequeño','status','observaciones'],
        'controlcosecha': ['codigo_lote', 'operario_name','codigo_empleado','supervisor_name','ubicacion_lote','estructura','apodo_variedad','tipo_cultivo','fecha','cajas_revisadas','frutos_autopol','frutos_sinmarca','frutos_sinlana','frutos_fueratipo','llenado_caja','punto_maduracion','status','observaciones']
    }
    # Obtener todos los campos del modelo
    campos = EXPORT_FIELDS.get(nombre_modelo, [f.name for f in Modelo._meta.fields])

    # Encabezados
    ws.append(campos)

    # Filas de datos
    for obj in Modelo.objects.all():
        fila = [getattr(obj, campo) for campo in campos]
        ws.append(fila)

    # Respuesta HTTP
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={nombre_modelo}.xlsx'
    wb.save(response)
    return response

# Create your views here.
def lotes_list(request):
    #today = timezone.localtime(timezone.now()).date()
    salidas = lotes.objects.all()
    return render(request, 'sdcsemillas/lotes_list.html', {'registros': salidas})

def lotes_detail(request, pk):
    salidas = get_object_or_404(lotes, pk=pk)
    return render(request, 'sdcsemillas/lotes_detail.html', {'registros': salidas})

def obtener_variedad_relacionada(request):
    code = request.GET.get('codigo')
    nombre = request.GET.get('nombre')

    if code:
        variedad = variedades.objects.filter(variedad_code=code).first()
        if variedad:
            return JsonResponse({'nombre': variedad.apodo_variedad})
    elif nombre:
        variedad = variedades.objects.filter(apodo_variedad=nombre).first()
        if variedad:
            return JsonResponse({'codigo': variedad.variedad_code})

    return JsonResponse({}, status=404)

def  lotes_create(request):
    if request.method == 'POST':
        form = lotesForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                # Manejar excepciones específicas (por ejemplo, UniqueConstraintError)
                return JsonResponse({'error': str(e)}, status=400)
            return redirect('lotes_list')
        else:
             # Imprimir errores para depuración
            return JsonResponse({'errores': form.errors}, status=400)
    else:
        form = lotesForm()
    return render(request, 'sdcsemillas/lotes_form.html', {'form': form,'modo':'crear'})

def lotes_update(request, pk):
    salidas = get_object_or_404(lotes, pk=pk)
    if request.method == 'POST':
        form = lotesForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('lotes_list')
    else:
        form = lotesForm(instance=salidas)
    return render(request, 'sdcsemillas/lotes_form.html', {'form': form,'modo':'actualizar'})

def lotes_delete(request, pk):

    salidas = get_object_or_404(lotes, pk=pk)

    if request.method == 'POST':
        salidas.status = 'Anulado'
        salidas.save()
        messages.success(request, "Lote anulado correctamente.")
        return redirect('lotes_list')
    
    return render(request, 'sdcsemillas/lotes_confirm_delete.html', {'registros': salidas})

def lotes_detail(request, pk):
    salidas = get_object_or_404(lotes, pk=pk)
    return render(request, 'sdcsemillas/lotes_detail.html', {'registros': salidas})

def variedades_list(request):
    #today = timezone.localtime(timezone.now()).date()
    salidas = variedades.objects.filter( status__isnull=True)
    return render(request, 'sdcsemillas/variedades_list.html', {'registros': salidas})

def  variedades_create(request):
    if request.method == 'POST':
        form = variedadesForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                # Manejar excepciones específicas (por ejemplo, UniqueConstraintError)
                return JsonResponse({'error': str(e)}, status=400)
            return redirect('variedades_list')
        else:
             # Imprimir errores para depuración
            return JsonResponse({'errores': form.errors}, status=400)
    else:
        form = variedadesForm()
    return render(request, 'sdcsemillas/variedades_form.html', {'form': form,'modo':'crear'})

def variedades_update(request, pk):
    salidas = get_object_or_404(variedades, pk=pk)
    if request.method == 'POST':
        form = variedadesForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('variedades_list')
    else:
        form = variedadesForm(instance=salidas)
    return render(request, 'sdcsemillas/variedades_form.html', {'form': form,'modo':'actualizar'})

def variedades_delete(request, pk):

    salidas = get_object_or_404(variedades, pk=pk)

    if request.method == 'POST':
        salidas.status = 'Anulado'
        salidas.save()
        messages.success(request, "Variedad anulado correctamente.")
        return redirect('variedades_list')
    
    return render(request, 'sdcsemillas/variedades_confirm_delete.html', {'registros': salidas})

def variedades_detail(request, pk):
    salidas = get_object_or_404(variedades, pk=pk)
    return render(request, 'sdcsemillas/variedades_detail.html', {'registros': salidas})

def conteoplantas_list(request):
    #today = timezone.localtime(timezone.now()).date()
    salidas = conteoplantas.objects.exclude(status__in=["Anulado", "Cerrado"])
    return render(request, 'sdcsemillas/conteoplantas_list.html', {'registros': salidas})

def  conteoplantas_create(request):
    nombre_supervisor = ''
    
    try:
        usuario = usuariosApp.objects.get(correo=request.user.email)
        nombre_supervisor = usuario.encargado
    except usuariosApp.DoesNotExist:
        nombre_supervisor = request.user.username  # Fallback si no se encuentra

    if request.method == 'POST':
        form = conteoplantasForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                # Manejar excepciones específicas (por ejemplo, UniqueConstraintError)
                return JsonResponse({'error': str(e)}, status=400)
            return redirect('conteoplantas_list')
        else:
             # Imprimir errores para depuración
            return JsonResponse({'errores': form.errors}, status=400)
    else:
        hoy = date.today()
        #dia_semana = calendar.day_name[hoy.weekday()]  # e.g., 'Monday'
        
        initial_data = {
            'supervisor_name': nombre_supervisor,
            'fecha': hoy
        }
        form = conteoplantasForm(initial=initial_data)
    
    return render(request, 'sdcsemillas/conteoplantas_form.html', {'form': form,'modo':'crear'})

def conteoplantas_update(request, pk):
    salidas = get_object_or_404(conteoplantas, pk=pk)
    if request.method == 'POST':
        form = conteoplantasForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('conteoplantas_list')
    else:
        form = conteoplantasForm(instance=salidas)
    return render(request, 'sdcsemillas/conteoplantas_form.html', {'form': form,'modo':'actualizar'})

def conteoplantas_delete(request, pk):

    salidas = get_object_or_404(conteoplantas, pk=pk)

    if request.method == 'POST':
        salidas.status = 'Anulado'
        salidas.save()
        messages.success(request, "Variedad anulado correctamente.")
        return redirect('conteoplantas_list')
    
    return render(request, 'sdcsemillas/conteoplantas_confirm_delete.html', {'registros': salidas})

def conteoplantas_detail(request, pk):
    salidas = get_object_or_404(conteoplantas, pk=pk)
    return render(request, 'sdcsemillas/conteoplantas_detail.html', {'registros': salidas})


def conteosemillas_list(request):
    #today = timezone.localtime(timezone.now()).date()
    salidas = conteosemillas.objects.exclude(status__in=["Anulado", "Cerrado"])
    return render(request, 'sdcsemillas/conteosemillas_list.html', {'registros': salidas})

def conteosemillas_create(request):
    nombre_supervisor = ''
    
    try:
        usuario = usuariosApp.objects.get(correo=request.user.email)
        nombre_supervisor = usuario.encargado
    except usuariosApp.DoesNotExist:
        nombre_supervisor = request.user.username  # Fallback si no se encuentra

    if request.method == 'POST':
        form = conteosemillasForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                # Manejar excepciones específicas (por ejemplo, UniqueConstraintError)
                return JsonResponse({'error': str(e)}, status=400)
            return redirect('conteosemillas_list')
        else:
             # Imprimir errores para depuración
            return JsonResponse({'errores': form.errors}, status=400)
    else:
        hoy = date.today()
        #dia_semana = calendar.day_name[hoy.weekday()]  # e.g., 'Monday'
        
        initial_data = {
            'supervisor_name': nombre_supervisor,
            'fecha': hoy
        }
        form = conteosemillasForm(initial=initial_data)
        
    return render(request, 'sdcsemillas/conteosemillas_form.html', {'form': form,'modo':'crear'})

def conteosemillas_update(request, pk):
    salidas = get_object_or_404(conteosemillas, pk=pk)
    if request.method == 'POST':
        form = conteosemillasForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('conteosemillas_list')
    else:
        form = conteosemillasForm(instance=salidas)
    return render(request, 'sdcsemillas/conteosemillas_form.html', {'form': form,'modo':'actualizar'})

def conteosemillas_delete(request, pk):

    salidas = get_object_or_404(conteosemillas, pk=pk)

    if request.method == 'POST':
        salidas.status = 'Anulado'
        salidas.save()
        messages.success(request, "Conteo anulado correctamente.")
        return redirect('conteosemillas_list')
    
    return render(request, 'sdcsemillas/conteosemillas_confirm_delete.html', {'registros': salidas})

def conteosemillas_detail(request, pk):
    salidas = get_object_or_404(conteosemillas, pk=pk)
    return render(request, 'sdcsemillas/conteosemillas_detail.html', {'registros': salidas})


def conteofrutosplan_list(request):
    #today = timezone.localtime(timezone.now()).date()
    salidas =  conteofrutosplanilla.objects.exclude(status__in=["Anulado", "Cerrado"])
    return render(request, 'sdcsemillas/conteofrutosplan_list.html', {'registros': salidas})

def conteofrutosplan_create(request):
    
    nombre_supervisor = ''
    
    try:
        usuario = usuariosApp.objects.get(correo=request.user.email)
        nombre_supervisor = usuario.encargado
    except usuariosApp.DoesNotExist:
        nombre_supervisor = request.user.username  # Fallback si no se encuentra

    if request.method == 'POST':
        form = conteofrutosplanillaForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                # Manejar excepciones específicas (por ejemplo, UniqueConstraintError)
                return JsonResponse({'error': str(e)}, status=400)
            return redirect('conteofrutosplan_list')
        else:
             # Imprimir errores para depuración
            return JsonResponse({'errores': form.errors}, status=400)
    else:
        hoy = date.today()
        #dia_semana = calendar.day_name[hoy.weekday()]  # e.g., 'Monday'
        
        initial_data = {
            'supervisor_name': nombre_supervisor,
            'fecha': hoy
        }
        form = conteofrutosplanillaForm(initial=initial_data)
        
    return render(request, 'sdcsemillas/conteofrutosplan_form.html', {'form': form,'modo':'crear'})

def conteofrutosplan_update(request, pk):
    salidas = get_object_or_404(conteofrutosplanilla, pk=pk)
    if request.method == 'POST':
        form = conteofrutosplanillaForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('conteofrutosplan_list')
    else:
        form = conteofrutosplanillaForm(instance=salidas)
    return render(request, 'sdcsemillas/conteofrutosplan_form.html', {'form': form,'modo':'actualizar'})

def conteofrutosplan_delete(request, pk):

    salidas = get_object_or_404(conteofrutosplanilla, pk=pk)

    if request.method == 'POST':
        salidas.status = 'Anulado'
        salidas.save()
        messages.success(request, "Conteo anulado correctamente.")
        return redirect('conteofrutosplan_list')
    
    return render(request, 'sdcsemillas/conteofrutospla_confirm_delete.html', {'registros': salidas})


def conteofrutosplan_detail(request, pk):
    salidas = get_object_or_404(conteofrutosplanilla, pk=pk)
    return render(request, 'sdcsemillas/conteofrutosplan_detail.html', {'registros': salidas})

def conteofrutos_list(request):
    #today = timezone.localtime(timezone.now()).date()
    salidas = conteofrutos.objects.exclude(status__in=["Anulado", "Cerrado"])
    return render(request, 'sdcsemillas/conteofrutos_list.html', {'registros': salidas})

def conteofrutos_create(request):
    
    nombre_supervisor = ''
    
    try:
        usuario = usuariosApp.objects.get(correo=request.user.email)
        nombre_supervisor = usuario.encargado
    except usuariosApp.DoesNotExist:
        nombre_supervisor = request.user.username  # Fallback si no se encuentra

    if request.method == 'POST':
        form = conteofrutosForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                # Manejar excepciones específicas (por ejemplo, UniqueConstraintError)
                return JsonResponse({'error': str(e)}, status=400)
            return redirect('conteofrutos_list')
        else:
             # Imprimir errores para depuración
            return JsonResponse({'errores': form.errors}, status=400)
    else:
        hoy = date.today()
        #dia_semana = calendar.day_name[hoy.weekday()]  # e.g., 'Monday'
        
        initial_data = {
            'supervisor_name': nombre_supervisor,
            'fecha': hoy
        }
        form = conteofrutosForm(initial=initial_data)
        
    return render(request, 'sdcsemillas/conteofrutos_form.html', {'form': form,'modo':'crear'})

def conteofrutos_update(request, pk):
    salidas = get_object_or_404(conteofrutos, pk=pk)
    if request.method == 'POST':
        form = conteofrutosForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('conteofrutos_list')
    else:
        form = conteofrutosForm(instance=salidas)
    return render(request, 'sdcsemillas/conteofrutos_form.html', {'form': form,'modo':'actualizar'})

def conteofrutos_delete(request, pk):

    salidas = get_object_or_404(conteofrutos, pk=pk)

    if request.method == 'POST':
        salidas.status = 'Anulado'
        salidas.save()
        messages.success(request, "Conteo anulado correctamente.")
        return redirect('conteofrutos_list')
    
    return render(request, 'sdcsemillas/conteofrutos_confirm_delete.html', {'registros': salidas})

def conteofrutos_detail(request, pk):
    salidas = get_object_or_404(conteofrutos, pk=pk)
    return render(request, 'sdcsemillas/conteofrutos_detail.html', {'registros': salidas})

def etapasdelote_list(request):
    #today = timezone.localtime(timezone.now()).date()
    salidas = etapasdelote.objects.exclude(status__in=["Anulado", "Cerrado"])
    return render(request, 'sdcsemillas/etapasdelote_list.html', {'registros': salidas})

def etapasdelote_create(request):
    nombre_supervisor = ''
    
    try:
        usuario = usuariosApp.objects.get(correo=request.user.email)
        nombre_supervisor = usuario.encargado
    except usuariosApp.DoesNotExist:
        nombre_supervisor = request.user.username  # Fallback si no se encuentra

    if request.method == 'POST':
        form = etapasdeloteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('etapasdelote_list')
        else:
            return JsonResponse({'errores': form.errors}, status=400)
    else:
        hoy = date.today()
        dia_semana = calendar.day_name[hoy.weekday()]  # e.g., 'Monday'
        
        initial_data = {
            'supervisor_name': nombre_supervisor,
            'fecha': hoy
        }
        form = etapasdeloteForm(initial=initial_data)
    
    return render(request, 'sdcsemillas/etapasdelote_form.html', {'form': form,'modo':'crear'})

def obtener_datos_lote(request):
    if request.method == 'POST':
        # Asumiendo que recibes un JSON o form-urlencoded con 'codigo_lote'
        codigo_lote = request.POST.get('codigo_lote') or json.loads(request.body).get('codigo_lote')

        try:
            lote = lotes.objects.get(id=int(codigo_lote))
            variedad = variedades.objects.get(variedad_code=lote.variedad_code)

            data = {
                'codigo_lote': lote.id,
                'apodo_variedad': lote.apodo_variedad,
                'tipo_cultivo': lote.cultivo,
                'ubicacion_lote': lote.ubicación,
                'estructura': lote.estructura,
                'codigo_padre': variedad.cod_padre,
                'codigo_madre': variedad.cod_madre
            }
            return JsonResponse(data)

        except lotes.DoesNotExist:
            return JsonResponse({'error': 'Lote no encontrado'}, status=404)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    

def obtener_semana_desde_polinizacion(request):
    if request.method == 'POST':
        codigo_lote = request.POST.get('codigo_lote')

        if not codigo_lote:
            return JsonResponse({'error': 'Código de lote requerido'}, status=400)

        try:
            etapa = etapasdelote.objects.filter(
                codigo_lote=int(codigo_lote),
                status='Inicio',
                evento='Polinización'
            ).order_by('fecha').first()

            if etapa:
                fecha_inicio = etapa.fecha
                dias_diff = (date.today() - fecha_inicio).days
                semanas = (dias_diff // 7) + 1 if dias_diff >= 0 else 1
                semanas = min(semanas, 6)
                mensaje_semana = ""
            else:
                fecha_inicio = ""
                semanas = ""
                mensaje_semana = "No se ha indicado la fecha de inicio de polinización para este lote."

            return JsonResponse({
                'fecha_inicio': fecha_inicio.isoformat() if fecha_inicio else "",
                'semana': semanas,
                'mensaje':mensaje_semana
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        

    return JsonResponse({'error': 'Método no permitido'}, status=405)

def obtener_semana_desde_cosecha(request):
    if request.method == 'POST':
        codigo_lote = request.POST.get('codigo_lote')

        if not codigo_lote:
            return JsonResponse({'error': 'Código de lote requerido'}, status=400)

        try:
            etapa = etapasdelote.objects.filter(
                codigo_lote=int(codigo_lote),
                status='Inicio',
                evento='Cosecha'
            ).order_by('fecha').first()

            if etapa:
                fecha_inicio = etapa.fecha
                dias_diff = (date.today() - fecha_inicio).days
                semanas = (dias_diff // 7) + 1 if dias_diff >= 0 else 1
                semanas = min(semanas, 6)
                mensaje_semana = ""
            else:
                fecha_inicio = ""
                semanas = ""
                mensaje_semana = "No se ha indicado la fecha de inicio de cosecha para este lote."

            return JsonResponse({
                'fecha_inicio': fecha_inicio.isoformat() if fecha_inicio else "",
                'semana': semanas,
                'mensaje':mensaje_semana
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        

    return JsonResponse({'error': 'Método no permitido'}, status=405)

def etapasdelote_update(request, pk):
    salidas = get_object_or_404(etapasdelote, pk=pk)
    if request.method == 'POST':
        form = etapasdeloteForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('etapasdelote_list')
    else:
        
        form = etapasdeloteForm(instance=salidas)
    return render(request, 'sdcsemillas/etapasdelote_form.html', {'form': form,'modo':'actualizar'})

def etapasdelote_delete(request, pk):

    salidas = get_object_or_404(etapasdelote, pk=pk)

    if request.method == 'POST':
        salidas.status = 'Anulado'
        salidas.save()
        messages.success(request, "Etapa anulada correctamente.")
        return redirect('etapasdelote_list')
    
    return render(request, 'sdcsemillas/etapasdelote_confirm_delete.html', {'registros': salidas})

def etapasdelote_detail(request, pk):
    salidas = get_object_or_404(etapasdelote, pk=pk)
    return render(request, 'sdcsemillas/etapasdelote_detail.html', {'registros': salidas})


def ccalidadpolen_list(request):
    #today = timezone.localtime(timezone.now()).date()
    salidas = ccalidadpolen.objects.exclude(status__in=["Anulado", "Cerrado"])
    return render(request, 'sdcsemillas/ccalidadpolen_list.html', {'registros': salidas})

def ccalidadpolen_create(request):
    nombre_supervisor = ''
    
    try:
        usuario = usuariosApp.objects.get(correo=request.user.email)
        nombre_supervisor = usuario.encargado
    except usuariosApp.DoesNotExist:
        nombre_supervisor = request.user.username  # Fallback si no se encuentra

    if request.method == 'POST':
        form = ccalidadpolenForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                # Manejar excepciones específicas (por ejemplo, UniqueConstraintError)
                return JsonResponse({'error': str(e)}, status=400)
            return redirect('ccalidadpolen_list')
        else:
             # Imprimir errores para depuración
            return JsonResponse({'errores': form.errors}, status=400)
    else:
        hoy = date.today()
        #dia_semana = calendar.day_name[hoy.weekday()]  # e.g., 'Monday'
        
        initial_data = {
            'supervisor_name': nombre_supervisor,
            'fecha': hoy
        }
        form = ccalidadpolenForm(initial=initial_data)
     
    return render(request, 'sdcsemillas/ccalidadpolen_form.html', {'form': form,'modo':'crear'})

def ccalidadpolen_update(request, pk):
    salidas = get_object_or_404(ccalidadpolen, pk=pk)
    if request.method == 'POST':
        form = ccalidadpolenForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('ccalidadpolen_list')
    else:
        form = ccalidadpolenForm(instance=salidas)
    return render(request, 'sdcsemillas/ccalidadpolen_form.html', {'form': form,'modo':'actualizar'})

def ccalidadpolen_delete(request, pk):

    salidas = get_object_or_404(ccalidadpolen, pk=pk)

    if request.method == 'POST':
        salidas.status = 'Anulado'
        salidas.save()
        messages.success(request, "Control anulado correctamente.")
        return redirect('ccalidadpolen_list')
    
    return render(request, 'sdcsemillas/ccalidadpolen_confirm_delete.html', {'registros': salidas})

def ccalidadpolen_detail(request, pk):
    salidas = get_object_or_404(ccalidadpolen, pk=pk)
    return render(request, 'sdcsemillas/ccalidadpolen_detail.html', {'registros': salidas})

def indexpolinizacion_list(request):
    #today = timezone.localtime(timezone.now()).date()
    salidas = indexpolinizacion.objects.exclude(status__in=["Anulado", "Cerrado"])
    return render(request, 'sdcsemillas/indexpolinizacion_list.html', {'registros': salidas})

def indexpolinizacion_create(request):
    nombre_supervisor = ''
    
    try:
        usuario = usuariosApp.objects.get(correo=request.user.email)
        nombre_supervisor = usuario.encargado
    except usuariosApp.DoesNotExist:
        nombre_supervisor = request.user.username  # Fallback si no se encuentra

    if request.method == 'POST':
        form = indexpolinizacionForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                # Manejar excepciones específicas (por ejemplo, UniqueConstraintError)
                return JsonResponse({'error': str(e)}, status=400)
            return redirect('indexpolinizacion_list')
        else:
             # Imprimir errores para depuración
            return JsonResponse({'errores': form.errors}, status=400)
    else:
        hoy = date.today()
        dia_semana = calendar.day_name[hoy.weekday()]  # e.g., 'Monday'
        dias_traducidos = {
            'Monday': 'Lunes',
            'Tuesday': 'Martes',
            'Wednesday': 'Miércoles',
            'Thursday': 'Jueves',
            'Friday': 'Viernes',
            'Saturday': 'Sábado',
            'Sunday': 'Domingo',
        }

        initial_data = {
            'supervisor_name': nombre_supervisor,
            'fecha': hoy,
            'diasemana': dias_traducidos.get(dia_semana, ''),
        }
        form = indexpolinizacionForm(initial=initial_data)
      
    return render(request, 'sdcsemillas/indexpolinizacion_form.html', {'form': form,'modo':'crear'})

def indexpolinizacion_update(request, pk):
    salidas = get_object_or_404(indexpolinizacion, pk=pk)
    if request.method == 'POST':
        form = indexpolinizacionForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('indexpolinizacion_list')
    else:
        form = indexpolinizacionForm(instance=salidas)
    return render(request, 'sdcsemillas/indexpolinizacion_form.html', {'form': form,'modo':'actualizar'})

def indexpolinizacion_delete(request, pk):

    salidas = get_object_or_404(indexpolinizacion, pk=pk)

    if request.method == 'POST':
        salidas.status = 'Anulado'
        salidas.save()
        messages.success(request, "Index anulado correctamente.")
        return redirect('indexpolinizacion_list')
    
    return render(request, 'sdcsemillas/indexpolinizacion_confirm_delete.html', {'registros': salidas})

def indexpolinizacion_detail(request, pk):
    salidas = get_object_or_404(indexpolinizacion, pk=pk)
    return render(request, 'sdcsemillas/indexpolinizacion_detail.html', {'registros': salidas})

def conteoflores_list(request):
    #today = timezone.localtime(timezone.now()).date()
    salidas = floresabiertas.objects.exclude(status__in=["Anulado", "Cerrado"])
    return render(request, 'sdcsemillas/conteoflores_list.html', {'registros': salidas})

def conteoflores_create(request):
    nombre_supervisor = ''
    
    try:
        usuario = usuariosApp.objects.get(correo=request.user.email)
        nombre_supervisor = usuario.encargado
    except usuariosApp.DoesNotExist:
        nombre_supervisor = request.user.username  # Fallback si no se encuentra

    if request.method == 'POST':
        form = conteofloresForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                # Manejar excepciones específicas (por ejemplo, UniqueConstraintError)
                return JsonResponse({'error': str(e)}, status=400)
            return redirect('conteoflores_list')
        else:
             # Imprimir errores para depuración
            return JsonResponse({'errores': form.errors}, status=400)
    else:
        hoy = date.today()
        dia_semana = calendar.day_name[hoy.weekday()]  # e.g., 'Monday'
        dias_traducidos = {
            'Monday': 'Lunes',
            'Tuesday': 'Martes',
            'Wednesday': 'Miércoles',
            'Thursday': 'Jueves',
            'Friday': 'Viernes',
            'Saturday': 'Sábado',
            'Sunday': 'Domingo',
        }

        initial_data = {
            'supervisor_name': nombre_supervisor,
            'fecha': hoy,
            'diasemana': dias_traducidos.get(dia_semana, ''),
        }
        form = conteofloresForm(initial=initial_data)
       
    return render(request, 'sdcsemillas/conteoflores_form.html', {'form': form,'modo':'crear'})

def conteoflores_update(request, pk):
    salidas = get_object_or_404(floresabiertas, pk=pk)
    if request.method == 'POST':
        form = conteofloresForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('conteoflores_list')
    else:
        form = conteofloresForm(instance=salidas)
    return render(request, 'sdcsemillas/conteoflores_form.html', {'form': form,'modo':'actualizar'})

def conteoflores_delete(request, pk):

    salidas = get_object_or_404(floresabiertas, pk=pk)

    if request.method == 'POST':
        salidas.status = 'Anulado'
        salidas.save()
        messages.success(request, "Conteo anulada correctamente.")
        return redirect('conteoflores_list')
    
    return render(request, 'sdcsemillas/conteoflores_confirm_delete.html', {'registros': salidas})

def conteoflores_detail(request, pk):
    salidas = get_object_or_404(floresabiertas, pk=pk)
    return render(request, 'sdcsemillas/conteoflores_detail.html', {'registros': salidas})

def controlcosecha_list(request):
    #today = timezone.localtime(timezone.now()).date()
    salidas = controlcosecha.objects.exclude(status__in=["Anulado", "Cerrado"])
    return render(request, 'sdcsemillas/controlcosecha_list.html', {'registros': salidas})

def controlcosecha_create(request):
    
    nombre_supervisor = ''
    
    try:
        usuario = usuariosApp.objects.get(correo=request.user.email)
        nombre_supervisor = usuario.encargado
    except usuariosApp.DoesNotExist:
        nombre_supervisor = request.user.username  # Fallback si no se encuentra

    if request.method == 'POST':
        form = controlcosechaForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                # Manejar excepciones específicas (por ejemplo, UniqueConstraintError)
                return JsonResponse({'error': str(e)}, status=400)
            return redirect('controlcosecha_list')
        else:
             # Imprimir errores para depuración
            return JsonResponse({'errores': form.errors}, status=400)
    else:
        hoy = date.today()
        #dia_semana = calendar.day_name[hoy.weekday()]  # e.g., 'Monday'
        
        initial_data = {
            'supervisor_name': nombre_supervisor,
            'fecha': hoy
        }
        form = controlcosechaForm(initial=initial_data)
       
    return render(request, 'sdcsemillas/controlcosecha_form.html', {'form': form,'modo':'crear'})

def controlcosecha_update(request, pk):
    salidas = get_object_or_404(controlcosecha, pk=pk)
    if request.method == 'POST':
        form = controlcosechaForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('controlcosecHa_list')
    else:
        form = controlcosechaForm(instance=salidas)
    return render(request, 'sdcsemillas/controlcosecha_list.html', {'form': form,'modo':'actualizar'})

def controlcosecha_delete(request, pk):

    salidas = get_object_or_404(controlcosecha, pk=pk)

    if request.method == 'POST':
        salidas.status = 'Anulado'
        salidas.save()
        messages.success(request, "Control anulado correctamente.")
        return redirect('controlcosecha_list')
    
    return render(request, 'sdcsemillas/controlcosecha_confirm_delete.html', {'registros': salidas})

def controlcosecha_detail(request, pk):
    salidas = get_object_or_404(controlcosecha, pk=pk)
    return render(request, 'sdcsemillas/controlcosecha_detail.html', {'registros': salidas})

def obtener_datos_empleado_post(request):
    if request.method == "POST":
        codigo = request.POST.get('codigo_empleado', '').strip()
        try:
            empleado = operariosApp.objects.get(codigo_empleado=codigo)
            data = {
                'codigo_empleado': empleado.codigo_empleado,
                'codigoevo': empleado.codigoevo,
                'nombre_operario': empleado.nombre_operario
            }
            return JsonResponse(data)
        except operariosApp.DoesNotExist:
            return JsonResponse({'error': 'Empleado no encontrado'}, status=404)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

# Create your views here.
def operarios_list(request):
    #today = timezone.localtime(timezone.now()).date()
    salidas = operariosApp.objects.all()
    return render(request, 'sdcsemillas/operarios_list.html', {'registros': salidas})

def operarios_detail(request, pk):
    salidas = get_object_or_404(operariosApp, pk=pk)
    return render(request, 'sdcsemillas/operarios_detail.html', {'registros': salidas})

def  operarios_create(request):
    if request.method == 'POST':
        form = operariosForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                # Manejar excepciones específicas (por ejemplo, UniqueConstraintError)
                return JsonResponse({'error': str(e)}, status=400)
            return redirect('operarios_list')
        else:
             # Imprimir errores para depuración
            return JsonResponse({'errores': form.errors}, status=400)
    else:
        form = operariosForm()
    return render(request, 'sdcsemillas/operarios_form.html', {'form': form,'modo':'crear'})

def operarios_update(request, pk):
    salidas = get_object_or_404(operariosApp, pk=pk)
    if request.method == 'POST':
        form = operariosForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('operarios_list')
    else:
        form = operariosForm(instance=salidas)
    return render(request, 'sdcsemillas/operarios_form.html', {'form': form,'modo':'actualizar'})

def operarios_delete(request, pk):

    salidas = get_object_or_404(operariosApp, pk=pk)

    if request.method == 'POST':
        salidas.status = 'Anulado'
        salidas.save()
        messages.success(request, "Persona eliminada correctamente.")
        return redirect('operarios_list')
    
    return render(request, 'sdcsemillas/operarios_confirm_delete.html', {'registros': salidas})