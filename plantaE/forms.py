from django import forms
from .models import salidasFruta, usuariosAppFruta, datosProduccion, detallesProduccion

class salidasFrutaForm(forms.ModelForm):
    
    finca = forms.ModelChoiceField(queryset=usuariosAppFruta.objects.all())
    encargado = forms.ModelChoiceField(queryset=usuariosAppFruta.objects.all())
    correo = forms.ModelChoiceField(queryset=usuariosAppFruta.objects.all())
    orden = forms.ModelChoiceField(queryset=datosProduccion.objects.all())
    cultivo = forms.ModelChoiceField(queryset=datosProduccion.objects.all())
    variedad = forms.ModelChoiceField(queryset=detallesProduccion.objects.none())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'cultivo' in self.data:
            cultivo_id = str(self.data['cultivo'])
            self.fields['variedad'].queryset = detallesProduccion.objects.filter(cultivo=cultivo_id)

    class Meta:
    
        model = salidasFruta
        fields = ['viaje', 'cajas', 'finca', 'encargado', 'correo', 'orden', 'cultivo', 'variedad']
    