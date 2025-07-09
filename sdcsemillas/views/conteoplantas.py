# views/conteoplantas.py
from .base import *
from sdcsemillas.models import conteoplantas
from django.urls import reverse_lazy

class ConteoPlantasList(BaseListView):
    model = conteoplantas

class ConteoPlantasCreate(BaseCreateView):
    model = conteoplantas
    fields = '__all__'
    success_url = reverse_lazy('conteoplantas_list')

class ConteoPlantasUpdate(BaseUpdateView):
    model = conteoplantas
    fields = '__all__'
    success_url = reverse_lazy('conteoplantas_list')

class ConteoPlantasDelete(BaseDeleteView):
    model = conteoplantas
    success_url = reverse_lazy('conteoplantas_list')
