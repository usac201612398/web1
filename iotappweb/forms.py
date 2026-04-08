from django import forms
from .models import SensorDetalles

class sensordetallesForm(forms.ModelForm):
    
    op_priva = [('','-'),('Priva 1','Priva 1'),('Priva 2','Priva 2'),('Priva 3','Priva 3'),('Priva 4','Priva 4'),('Priva 5','Priva 5'),('Priva 6','Priva 6'),('Priva 7','Priva 7'),('Priva 8','Priva 8'),('Priva 9','Priva 9')]
    op_estructura = [('','-'),('CM1','CM1'),('CM2','CM2'),('CM3','CM3'),('CM4','CM4'),('CM5','CM5'),('CM6A','CM6A'),('CM6B','CM6B'),('CM7','CM7'),('CM8','CM8'),('INV1','INV1'),('INV2','INV2')]
    op_finca = [('','-'),('VALLE','VALLE'),('RIO','RIO'),('SL','SL')]
    op_status = [('En uso','En uso'),('Averiado','Averiado')]
    
    sensor = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    nombrearanet = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))  # Campo de texto
    tipo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))  # Campo de texto
    set_point = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))  # Campo numérico
    umbral_max = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))  # Campo numérico
    umbral_min = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))  # Campo numérico
    priva = forms.ChoiceField(choices=op_priva,widget=forms.Select(attrs={'class': 'form-control'}))
    estructura = forms.ChoiceField(choices=op_estructura,widget=forms.Select(attrs={'class': 'form-control'}))
    finca = forms.ChoiceField(choices=op_finca,widget=forms.Select(attrs={'class': 'form-control'}))
    status = forms.ChoiceField(choices=op_status,widget=forms.Select(attrs={'class': 'form-control'}))
    
    class Meta:
    
        model = SensorDetalles
        fields = ['sensor','umbral_min','umbral_max','nombrearanet','tipo', 'set_point','priva','estructura','finca']