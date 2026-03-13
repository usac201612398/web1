from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse

# modelos
from plantaE.models import contenedores

# formularios
from plantaE.forms import contenedoresForm

class ContenedoresListView(ListView):
    model = contenedores
    template_name = 'plantaE/contenedores/contenedores_list.html'
    context_object_name = 'registros'

    def get_queryset(self):
        return contenedores.objects.exclude(status='Cerrado').order_by('-created_at')

class ContenedoresCreateView(CreateView):
    model = contenedores
    form_class = contenedoresForm
    template_name = 'plantaE/contenedores/contenedores_form.html'
    success_url = reverse_lazy('contenedores_list')

    def get_initial(self):
        initial = super().get_initial()
        ultimo_contenedor = contenedores.objects.last()

        if ultimo_contenedor:
            initial['viaje'] = ultimo_contenedor.viaje + 1

        return initial

    def form_invalid(self, form):
        return JsonResponse({'errores': form.errors}, status=400)

    def form_valid(self, form):
        try:
            self.object = form.save()
            return super().form_valid(form)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ultimo_contenedor'] = contenedores.objects.last()
        return context

class ContenedoresUpdateView(UpdateView):
    model = contenedores
    form_class = contenedoresForm
    template_name = 'plantaE/contenedores/contenedores_form.html'
    success_url = reverse_lazy('contenedores_list')

class ContenedoresDeleteView(DeleteView):
    model = contenedores
    template_name = 'plantaE/contenedores/contenedores_confirm_delete.html'
    context_object_name = 'registros'
    success_url = reverse_lazy('contenedores_list')

'''
def contenedores_list(request):
    salidas = contenedores.objects.exclude(status='Cerrado')  # Excluye los que tienen status 'Cerrado'
    salidas = salidas.order_by('-created_at')
    
    return render(request, 'plantaE/contenedores_list.html', {'registros': salidas})

def contenedores_delete(request, pk):
    salidas = get_object_or_404(contenedores, pk=pk)
    if request.method == 'POST':
        salidas.delete()
        return redirect('contenedores_list')
    return render(request, 'plantaE/contenedores_confirm_delete.html', {'registros': salidas})

def contenedores_create(request):
    if request.method == 'POST':
        form = contenedoresForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                # Manejar excepciones específicas (por ejemplo, UniqueConstraintError)
                return JsonResponse({'error': str(e)}, status=400)
            return redirect('contenedores_list')
        else:
            # Imprimir errores para depuración
            return JsonResponse({'errores': form.errors}, status=400)
    else:
        form = contenedoresForm()

    # Obtener el último registro del contenedor
    ultimo_contenedor = contenedores.objects.last()

    # Si existe un último contenedor, pre-llenar el campo 'nombre' con el valor del último contenedor
    initial_data = {}
    if ultimo_contenedor:
        initial_data['viaje'] = ultimo_contenedor.viaje + 1 # Cambia 'nombre' por el nombre del campo relevante

    # Crear el formulario con los valores iniciales
    form = contenedoresForm(initial=initial_data)

    return render(request, 'plantaE/contenedores_form.html', {
        'form': form,
        'ultimo_contenedor': ultimo_contenedor,
    })

def contenedores_update(request, pk):
    salidas = get_object_or_404(contenedores, pk=pk)
    if request.method == 'POST':
        form = contenedoresForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('contenedores_list')
    else:
        form = contenedoresForm(instance=salidas)
    return render(request, 'plantaE/contenedores_form.html', {'form': form})
'''
