from django import forms
from .models import *

class ubicacionesForm(forms.ModelForm):

    ESTADOS = [
        ('', ''),
        ('Abierta', 'Abierta'),
        ('Cerrada', 'Cerrada'),
        ('Anulada', 'Anulada'),
    ]
    
    nombre = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))  
    status = forms.ChoiceField(choices=ESTADOS,initial="Activa",widget=forms.Select(attrs={'class': 'my-input'}))
    
    class Meta:
    
        model = Ubicacion
        fields = ['nombre','status']