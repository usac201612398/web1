from django import forms
from .models import Actpeso,salidacontenedores,salidasFruta, contenedores, Recepciones, Ccalidad, inventarioProdTerm,AcumFruta, enviosFrutaPlantilla
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Div

class salidasFrutaForm(forms.ModelForm):

    op_viajes = [('','-'),('Viaje 1','Viaje 1'),('Viaje 2','Viaje 2'),('Viaje 3', 'Viaje 3'),('Viaje 4','Viaje 4'),('Viaje 5','Viaje 5'),('Viaje 6','Viaje 6'),('Viaje 7','Viaje 7'),('Viaje 8','Viaje 8')]
    op_cultivo = [('CHERRY','CHERRY'),('MEDLEY','MEDLEY'),('GRAPE','GRAPE'),('GRAPE ORGANICO','GRAPE ORGANICO'),('CHERRY ORGANICO','CHERRY ORGANICO'),('BLOCKY','BLOCKY'),('BLOCKY ORGANICO','BLOCKY ORGANICO'),('MINI','MINI'),('MINI ORGANICO','MINI ORGANICO')]
    
    fecha = forms.DateField(widget=forms.DateInput(attrs={'class': 'my-input'}))
    correo = forms.CharField(widget=forms.Select(attrs={'class': 'my-input'}))  # Campo de correo electrónico
    encargado = forms.CharField(widget=forms.Select(attrs={'class': 'my-input'}))  # Campo de texto
    finca = forms.CharField(widget=forms.Select(attrs={'class': 'my-input'}))  # Campo de texto
    variedad = forms.CharField(widget=forms.Select(attrs={'class': 'my-input'}))  # Campo de texto
    viaje = forms.ChoiceField(choices=op_viajes,widget=forms.Select(attrs={'class': 'my-input'}))  # Campo de texto
    cajas = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'}))  # Campo numérico
    cultivo = forms.CharField(widget=forms.Select(attrs={'class': 'my-input'}))  # Campo de texto
    
    class Meta:
    
        model = salidasFruta
        fields = ['correo','fecha','viaje','encargado',  'finca', 'cajas', 'cultivo','variedad']

class pesosForm(forms.ModelForm):

    recepcion = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input'}))
    fecha = forms.DateField(widget=forms.DateInput(attrs={'class': 'my-input'}))
    llave = forms.CharField(widget=forms.Select(attrs={'class': 'my-input'}))  # Campo de correo electrónico
    finca = forms.CharField(widget=forms.Select(attrs={'class': 'my-input'}))  # Campo de texto
    cultivo = forms.CharField(widget=forms.Select(attrs={'class': 'my-input'}))  # Campo de texto
    tarimas = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'}))  # Campo numérico
    cajas = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'}))  # Campo numérico
    libras = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'}))  # Campo numérico
    
    class Meta:
    
        model = Actpeso
        fields = ['recepcion','fecha','llave',  'finca', 'cultivo','tarimas','cajas','libras']

class acumFrutaForm(forms.ModelForm):
    
    fecha = forms.DateField(widget=forms.DateInput(attrs={'class': 'my-input'}))
    correo = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input'}))  # Campo de correo electrónico
    finca = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input'}))  # Campo de texto
    cajas = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'}))  # Campo numérico
    orden = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input'}))  # Campo de texto
    cultivo = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input'}))  # Campo de texto
    variedad = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input'}))  # Campo de texto
    estructura = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input'}))  # Campo de texto
    
    class Meta:
    
        model = AcumFruta
        fields = ['correo','fecha', 'finca', 'cajas', 'orden','cultivo','variedad','estructura']

class recepcionesForm(forms.ModelForm):

    op_status = [('Pendiente','-'),('En proceso','En proceso')]

    recepcion = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input'}))
    fecha = forms.DateField(widget=forms.DateInput(attrs={'class': 'my-input'}))
    finca = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input'}))  # Campo de texto
    cajas = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'}))  # Campo numérico
    libras = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'my-input'}))  # Campo numérico
    cultivo = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input'}))  # Campo de texto
    observaciones = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input'}))  # Campo de texto
    status = forms.ChoiceField(choices=op_status,widget=forms.Select(attrs={'class': 'my-input'}))

    class Meta:
    
        model = Recepciones
        fields = ['recepcion','fecha','finca', 'cajas',  'libras', 'cultivo','observaciones','status']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['observaciones'].required = False

class ccalidadForm(forms.ModelForm):

    registro = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'}))
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type':'date','class': 'my-input'}))
    porcentaje= forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'my-input'}))  # Campo numérico
    llave = forms.CharField(widget=forms.Select(attrs={'class': 'my-input'}))
    causarechazo = forms.CharField(widget=forms.Select(attrs={'class': 'my-input'}))
    observaciones = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input'}))
   
    class Meta:
    
        model = Ccalidad
        fields = ['registro','fecha','porcentaje',  'llave', 'causarechazo','observaciones']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['observaciones'].required = False
        self.fields['registro'].required = False

class inventarioFrutaForm(forms.ModelForm):

    op_empaque = [('Cajas','Cajas'),('Libras','Libras')]
    op_proveedor = [('','-'),('RIO','RIO'),('VALLE','VALLE'),('CIP','CIP'),('PASTORIA','PASTORIA')]
    op_cultivo = [('','-'),('CHERRY','CHERRY'),('MEDLEY','MEDLEY'),('GRAPE','GRAPE'),('GRAPE ORGANICO','GRAPE ORGANICO'),('CHERRY ORGANICO','CHERRY ORGANICO'),('BLOCKY','BLOCKY'),('BLOCKY ORGANICO','BLOCKY ORGANICO'),('MINI','MINI'),('MINI ORGANICO','MINI ORGANICO')]
    op_categoria = [('','-'),('Mastronardi','Mastronardi'),('Carreta','Carreta'),('Cenma','Cenma'),('Devolucion','Devolucion')]
    
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type':'date','class': 'my-input'}))
    proveedor = forms.ChoiceField(choices=op_proveedor, widget=forms.Select(attrs={'class': 'my-input'}))
    cultivo = forms.ChoiceField(choices=op_cultivo, widget=forms.Select(attrs={'class': 'my-input'}))
    categoria = forms.ChoiceField(choices=op_categoria, widget=forms.Select(attrs={'class': 'my-input'}))
    calidad1 = forms.CharField(widget=forms.Select(attrs={'class': 'my-input'}))
    empaque = forms.ChoiceField(choices=op_empaque, widget=forms.Select(attrs={'class': 'my-input'}))
    cajas = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'my-input'}))  # Campo numérico
    libras = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'my-input'}))  # Campo numérico

    class Meta:
        
        model = inventarioProdTerm
        fields = ['fecha','proveedor', 'cultivo', 'categoria', 'calidad1','empaque','cajas','libras']

class contenedoresForm(forms.ModelForm):

    op_status = [('Pendiente','-'),('Cerrado','Cerrado')]
    op_destino = [('Jonestown','Jonestown'),('Lakeland','Lakeland'),('Laredo, Texas','Laredo, Texas'),('Miami','Miami')]
    op_naviera = [('SEABOARD','SEABOARD'),('CROWLEY','CROWLEY')]

    fecha = forms.DateField(widget=forms.DateInput(attrs={'type':'date','class': 'my-input'}))
    eta = forms.DateField(widget=forms.DateInput(attrs={'type':'date','class': 'my-input'}))
    etd = forms.DateField(widget=forms.DateInput(attrs={'type':'date','class': 'my-input'}))
    destino = forms.ChoiceField(choices=op_destino, widget=forms.Select(attrs={'class': 'my-input'}))
    contenedor = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input'}))
    bl = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input'}))
    booking = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input'}))
    transportista = forms.ChoiceField(choices=op_naviera, widget=forms.Select(attrs={'class': 'my-input'}))
    viaje = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'}))  # Campo numérico
    piloto = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input'}))
    temperatura = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'my-input'}))  # Campo numérico
    ventilacion = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'my-input'}))  # Campo numérico
    marchamo = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input'}))
    placacamion = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input'}))
    horasalida = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'my-input'}))  # Campo numérico
    
    class Meta:
        
        model = contenedores
        fields = ['fecha','destino','contenedor','transportista','viaje','piloto','temperatura', 'ventilacion', 'marchamo', 'placacamion','horasalida','eta','etd','bl','booking']

class salidacontenedoresForm(forms.ModelForm):

    #op_status = [('Pendiente','-'),('Cerrado','Cerrado')]
    #op_destino = [('Jonestown','Jonestown'),('Lakeland','Lakeland'),('Laredo, Texas','Laredo, Texas'),('Miami','Miami')]
    #op_naviera = [('SEABOARD','SEABOARD'),('CROWLEY','CROWLEY')]

    fecha = forms.DateField(widget=forms.DateInput(attrs={'type':'date','class': 'my-input'}))
    contenedor = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input'}))
    palet = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'})) 
    proveedor = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input'}))
    cultivo = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input'})) 
    itemsapname = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input'}))
    cajas = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'}))  # Campo numérico

    
    class Meta:
        
        model = salidacontenedores
        fields = ['fecha','contenedor','palet','proveedor','cultivo', 'itemsapname', 'cajas']


