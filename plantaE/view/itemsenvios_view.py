from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse

# modelos
from plantaE.models import paramenvlocales

# formularios
from plantaE.forms import itemsenviosForm

class ItemsEnviosListView(ListView):
    model = paramenvlocales
    template_name = 'plantaE/itemsenvios/itemsenvios_list.html'
    context_object_name = 'registros'

    def get_queryset(self):
        return paramenvlocales.objects.all().order_by('-registro')

class ItemsEnviosCreateView(CreateView):
    model = paramenvlocales
    form_class = itemsenviosForm
    template_name = 'plantaE/itemsenvios/itemsenvios_form.html'
    success_url = reverse_lazy('itemsenvios_list')

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
        context['modo'] = 'crear'
        return context

class ItemsEnviosUpdateView(UpdateView):
    model = paramenvlocales
    form_class = itemsenviosForm
    template_name = 'plantaE/itemsenvios/itemsenvios_form.html'
    success_url = reverse_lazy('itemsenvios_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modo'] = 'actualizar'
        return context

class ItemsEnviosDeleteView(DeleteView):
    model = paramenvlocales
    template_name = 'plantaE/itemsenvios/itemsenvios_confirm_delete.html'
    context_object_name = 'registros'
    success_url = reverse_lazy('itemsenvios_list')


'''
def itemsenvios_list(request):
    salidas = paramenvlocales.objects.all() # Excluye los que tienen status 'Cerrado'
    salidas = salidas.order_by('-registro')
    
    return render(request, 'plantaE/itemsenvios_list.html', {'registros': salidas})

def itemsenvios_delete(request, pk):
    salidas = get_object_or_404(paramenvlocales, pk=pk)
    if request.method == 'POST':
        salidas.delete()
        return redirect('itemsenvios_list')
    return render(request, 'plantaE/itemsenvios_confirm_delete.html', {'registros': salidas})

def itemsenvios_create(request):
    if request.method == 'POST':
        form = itemsenviosForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                # Manejar excepciones específicas (por ejemplo, UniqueConstraintError)
                return JsonResponse({'error': str(e)}, status=400)
            return redirect('itemsenvios_list')
        else:
             # Imprimir errores para depuración
            return JsonResponse({'errores': form.errors}, status=400)
    else:
        form = itemsenviosForm()
    return render(request, 'plantaE/itemsenvios_form.html', {'form': form,'modo':'crear'})

def itemsenvios_update(request, pk):
    salidas = get_object_or_404(paramenvlocales, pk=pk)
    if request.method == 'POST':
        form = itemsenviosForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('itemsenvios_list')
    else:
        form = itemsenviosForm(instance=salidas)
    return render(request, 'plantaE/itemsenvios_form.html', {'form': form,'modo':'actualizar'})
'''