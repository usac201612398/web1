from django import forms
from .models import salidasFruta, Recepciones, Ccalidad, inventarioProdTerm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Div

class salidasFrutaForm(forms.ModelForm):
    op_viajes = [('','-'),('Viaje 1','Viaje 1'),('Viaje 2','Viaje 2'),('Viaje 3', 'Viaje 3'),('Viaje 4','Viaje 4'),('Viaje 5','Viaje 5'),('Viaje 6','Viaje 6'),('Viaje 7','Viaje 7'),('Viaje 8','Viaje 8')]
    op_cultivo = [('CHERRY','CHERRY'),('MEDLEY','MEDLEY'),('GRAPE','GRAPE'),('GRAPE ORGANICO','GRAPE ORGANICO'),('CHERRY ORGANICO','CHERRY ORGANICO'),('BLOCKY','BLOCKY'),('BLOCKY ORGANICO','BLOCKY ORGANICO'),('MINI','MINI'),('MINI ORGANICO','MINI ORGANICO')]
    
    fecha = forms.DateField(widget=forms.DateInput(attrs={'class': 'my-input'}))
    correo = forms.CharField(widget=forms.Select(attrs={'class': 'my-input'}))  # Campo de correo electrónico
    encargado = forms.CharField(widget=forms.Select(attrs={'class': 'my-input'}))  # Campo de texto
    finca = forms.CharField(widget=forms.Select(attrs={'class': 'my-input'}))  # Campo de texto
    viaje = forms.ChoiceField(choices=op_viajes,widget=forms.Select(attrs={'class': 'my-input'}))  # Campo de texto
    cajas = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'}))  # Campo numérico
    orden = forms.CharField(widget=forms.Select(attrs={'class': 'my-input'}))  # Campo de texto
    cultivo = forms.ChoiceField(choices=op_cultivo,widget=forms.Select(attrs={'class': 'my-input'}))  # Campo de texto
    
    #variedad = forms.CharField(widget=forms.Select(attrs={'class': 'my-input'}))  # Campo de texto
    #estructura = forms.CharField(widget=forms.Select(attrs={'class': 'my-input'}))  # Campo de texto
    
    class Meta:
    
        model = salidasFruta
        fields = ['correo','fecha','viaje','encargado',  'finca', 'cajas',  'orden', 'cultivo']

class recepcionesForm(forms.ModelForm):
    op_status = [('Pendiente','-'),('En proceso','En proceso')]
    recepcion = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input'}))
    fecha = forms.DateField(widget=forms.DateInput(attrs={'class': 'my-input'}))
    finca = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input'}))  # Campo de texto
    cajas = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'}))  # Campo numérico
    libras = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'my-input'}))  # Campo numérico
    orden = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input'}))  # Campo de texto
    cultivo = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input'}))  # Campo de texto
    variedad = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input'}))  # Campo de texto
    estructura = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input'}))  # Campo de texto
    observaciones = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input'}))  # Campo de texto
    status = forms.ChoiceField(choices=op_status,widget=forms.Select(attrs={'class': 'my-input'}))

    class Meta:
    
        model = Recepciones
        fields = ['recepcion','fecha','finca', 'cajas',  'libras', 'orden','cultivo','estructura', 'variedad','observaciones','status']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['observaciones'].required = False

class ccalidadForm(forms.ModelForm):
    op_status2 = [('Pendiente','-'),('Inspeccionado','Inspeccionado')]
    registro = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'}))
    recepcion = forms.CharField(widget=forms.Select(attrs={'class': 'my-input'}))
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type':'date','class': 'my-input'}))
    porcentaje= forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'my-input'}))  # Campo numérico
    status2 = forms.ChoiceField(choices=op_status2,widget=forms.Select(attrs={'class': 'my-input'}))
    llave = forms.CharField(widget=forms.Select(attrs={'class': 'my-input'}))
    causarechazo = forms.CharField(widget=forms.Select(attrs={'class': 'my-input'}))
    observaciones = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input'}))

    class Meta:
    
        model = Ccalidad
        fields = ['registro','recepcion','fecha','porcentaje', 'status2', 'llave', 'causarechazo','observaciones']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['observaciones'].required = False
        self.fields['registro'].required = False

class inventarioFrutaForm(forms.ModelForm):

    op_proveedor = [('','-'),('RIO','RIO'),('VALLE','VALLE'),('CIP','CIP'),('PASTORIA','PASTORIA')]
    op_cultivo = [('','-'),('CHERRY','CHERRY'),('MEDLEY','MEDLEY'),('GRAPE','GRAPE'),('GRAPE ORGANICO','GRAPE ORGANICO'),('CHERRY ORGANICO','CHERRY ORGANICO'),('BLOCKY','BLOCKY'),('BLOCKY ORGANICO','BLOCKY ORGANICO'),('MINI','MINI'),('MINI ORGANICO','MINI ORGANICO')]
    op_categoria = [('','-'),('Mastronardi','Mastronardi'),('Carreta','Carreta'),('Cenma','Cenma'),('Devolucion','Devolucion')]
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type':'date','class': 'my-input'}))
    proveedor = forms.ChoiceField(choices=op_proveedor, widget=forms.Select(attrs={'class': 'my-input'}))
    cultivo = forms.ChoiceField(choices=op_cultivo, widget=forms.Select(attrs={'class': 'my-input'}))
    categoria = forms.ChoiceField(choices=op_categoria, widget=forms.Select(attrs={'class': 'my-input'}))
    calidad1 = forms.CharField(widget=forms.Select(attrs={'class': 'my-input'}))
    cajas = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'my-input'}))  # Campo numérico

    class Meta:
    
        model = inventarioProdTerm
        fields = ['fecha','proveedor', 'cultivo', 'categoria', 'calidad1','cajas']
