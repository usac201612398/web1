
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse

# modelos
from plantaE.models import productoTerm

# formularios
from plantaE.forms import itemsForm

class ItemsListView(ListView):
    model = productoTerm
    template_name = 'plantaE/itemsprodterm/items_list.html'
    context_object_name = 'registros'

    def get_queryset(self):
        return productoTerm.objects.all().order_by('-registro')

class ItemsCreateView(CreateView):
    model = productoTerm
    form_class = itemsForm
    template_name = 'plantaE/itemsprodterm/items_form.html'
    success_url = reverse_lazy('items_list')

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

class ItemsUpdateView(UpdateView):
    model = productoTerm
    form_class = itemsForm
    template_name = 'plantaE/itemsprodterm/items_form.html'
    success_url = reverse_lazy('items_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modo'] = 'actualizar'
        return context

class ItemsDeleteView(DeleteView):
    model = productoTerm
    template_name = 'plantaE/itemsprodterm/items_confirm_delete.html'
    context_object_name = 'registros'
    success_url = reverse_lazy('items_list')      

'''
def items_list(request):
    salidas = productoTerm.objects.all() # Excluye los que tienen status 'Cerrado'
    salidas = salidas.order_by('-registro')
    
    return render(request, 'plantaE/items_list.html', {'registros': salidas})

def items_delete(request, pk):
    salidas = get_object_or_404(productoTerm, pk=pk)
    if request.method == 'POST':
        salidas.delete()
        return redirect('items_list')
    return render(request, 'plantaE/items_confirm_delete.html', {'registros': salidas})

def items_create(request):
    if request.method == 'POST':
        form = itemsForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                # Manejar excepciones específicas (por ejemplo, UniqueConstraintError)
                return JsonResponse({'error': str(e)}, status=400)
            return redirect('items_list')
        else:
             # Imprimir errores para depuración
            return JsonResponse({'errores': form.errors}, status=400)
    else:
        form = itemsForm()
    return render(request, 'plantaE/items_form.html', {'form': form,'modo':'crear'})

def items_update(request, pk):
    salidas = get_object_or_404(productoTerm, pk=pk)
    if request.method == 'POST':
        form = itemsForm(request.POST, instance=salidas)
        if form.is_valid():
            form.save()
            return redirect('items_list')
    else:
        form = itemsForm(instance=salidas)
    return render(request, 'plantaE/items_form.html', {'form': form,'modo':'actualizar'})

'''