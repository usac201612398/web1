from django import forms
from .models import salidasFruta

class salidasFrutaForm(forms.ModelForm):
    class Meta:
        model = salidasFruta
        fields = ['finca', 'viaje', 'encargado', 'orden', 'cultivo', 'variedad', 'cajas']