from django import forms
from .models import salidasFruta, usuariosAppFruta, datosProduccion, detallesProduccion

class salidasFrutaForm(forms.ModelForm):
    
    finca = forms.ModelChoiceField(queryset=usuariosAppFruta.objects.all())
    encargado = forms.ModelChoiceField(queryset=usuariosAppFruta.objects.all())
    correo = forms.ModelChoiceField(queryset=usuariosAppFruta.objects.all())
    orden = forms.ModelChoiceField(queryset=datosProduccion.objects.all())
    cultivo = forms.ModelChoiceField(queryset=datosProduccion.objects.all())
    variedad = forms.ModelChoiceField(queryset=detallesProduccion.objects.all())
    class Meta:
    
        model = salidasFruta
        fields = ['finca',  'cajas']
    