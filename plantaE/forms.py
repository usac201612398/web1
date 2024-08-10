from django import forms
from .models import salidasFruta, usuariosAppFruta

class salidasFrutaForm(forms.ModelForm):
    class Meta:
        model = salidasFruta
        fields = ['finca', 'viaje', 'encargado', 'orden', 'cultivo', 'variedad','correo', 'cajas']
    finca = forms.ModelChoiceField(queryset=usuariosAppFruta.objects.all())
    encargado = forms.ModelChoiceField(queryset=usuariosAppFruta.objects.none())