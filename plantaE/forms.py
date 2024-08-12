from django import forms
from .models import salidasFruta, usuariosAppFruta, datosProduccion, detallesProduccion

class salidasFrutaForm(forms.ModelForm):
    



    class Meta:
    
        model = salidasFruta
        fields = ['viaje', 'cajas', 'finca', 'encargado', 'correo', 'orden', 'cultivo', 'variedad']
    