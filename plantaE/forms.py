from django import forms
from .models import Actpeso,salidacontenedores,salidasFruta, productoTerm,contenedores, Recepciones, Ccalidad, inventarioProdTerm,AcumFruta, enviosFrutaPlantilla
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
    op_proveedor = [('','-'),('INVERSIONES LA PASTORIA, S.A.','INVERSIONES LA PASTORIA, S.A.'),('SDC','SDC'),('AGROINDUSTRIAS SAN RAFAEL, S.A.','AGROINDUSTRIAS SAN RAFAEL, S.A.'),('INVERNADEROS TECNOLOGICOS S.A','INVERNADEROS TECNOLOGICOS S.A'),('HORTEX, S.A.','HORTEX, S.A.'),('DANIEL ESTUARDO GALICIA CARRERA','DANIEL ESTUARDO GALICIA CARRERA'),('PRODUCTOS DEL VALLE, S.A.','PRODUCTOS DEL VALLE, S.A.')]
    op_cultivo = [('','-'),('CHERRY','CHERRY'),('MEDLEY','MEDLEY'),('GRAPE','GRAPE'),('GRAPE ORGANICO','GRAPE ORGANICO'),('CHERRY ORGANICO','CHERRY ORGANICO'),('BLOCKY','BLOCKY'),('BLOCKY ORGANICO','BLOCKY ORGANICO'),('MINI','MINI'),('MINI ORGANICO','MINI ORGANICO')]
    op_categoria = [('','-'),('Mastronardi','Mastronardi'),('Carreta','Carreta'),('Cenma','Cenma'),('Devolucion','Devolucion')]
    
    registro = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input', 'readonly': 'readonly'}))
    proveedor = forms.ChoiceField(choices=op_proveedor, widget=forms.Select(attrs={'class': 'my-input'}))
    itemsapname = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input', 'readonly': 'readonly'}))   # Campo de texto
    cajas = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input', 'readonly': 'readonly'}))  # Campo numérico
    
    class Meta:
        
        model = inventarioProdTerm
        fields = ['registro','proveedor','itemsapname','cajas']

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

class itemsForm(forms.ModelForm):

    op_cultivo =   [('ROMA','ROMA'),('AGUACATE','AGUACATE'),('ARANDANO','ARANDANO'),('CHERRY','CHERRY'),('MEDLEY','MEDLEY'),('BEEF','BEEF'),('SALADETTE','SALADETTE'),('GRAPE','GRAPE'),('GRAPE ORGANICO','GRAPE ORGANICO'),('CHERRY ORGANICO','CHERRY ORGANICO'),('BLOCKY','BLOCKY'),('BLOCKY ORGANICO','BLOCKY ORGANICO'),('MINI','MINI'),('MINI ORGANICO','MINI ORGANICO')]
    op_categoria = [('Exportación','Exportación'),('Carreta','Carreta'),('Cenma','Cenma'),('Devolución','Devolución')]
    op_tipo =      [('Tomate','Tomate'),('Aguacate','Aguacate'),('Chile','Chile'),('Arandano','Arandano')]
    
    cultivo = forms.ChoiceField(choices=op_cultivo, widget=forms.Select(attrs={'class': 'my-input'}))
    itemsapcode = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input'}))
    itemsapname = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input'}))
    calidad1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input'}))
    categoria = forms.ChoiceField(choices=op_categoria, widget=forms.Select(attrs={'class': 'my-input'}))
    precio = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'my-input'})) 
    taraxcaja = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'my-input'})) 
    pesostdxcaja = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'my-input'})) 
    tipo = forms.ChoiceField(choices=op_tipo, widget=forms.Select(attrs={'class': 'my-input'}))  # Campo numérico
    orden = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input'}))
    
    class Meta:
        
        model = productoTerm
        fields = ['cultivo','itemsapcode','itemsapname','calidad1','categoria','precio','taraxcaja', 'pesostdxcaja', 'tipo', 'orden']
    
    
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
    # Agregar un campo "importe" solo para mostrarlo, no para que sea editado por el usuario
    importe = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'class': 'my-input', 'readonly': 'readonly'}))
    
    libras = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'my-input'}))  # Campo numérico
    
    class Meta:
        
        model = salidacontenedores
        fields = ['fecha','contenedor','palet','proveedor','cultivo', 'itemsapname', 'cajas', 'importe','libras']

    def clean(self):
        cleaned_data = super().clean()

        # Obtener el itemsapcode (en tu formulario no veo este campo, supongo que lo extraes de otro campo como 'itemsapname')
        itemsapname = cleaned_data.get('itemsapname')
        try:
            ref2 = productoTerm.objects.get(itemsapname=itemsapname)
            precio = ref2.precio if ref2.precio else 0.0
        except productoTerm.DoesNotExist:
            precio = 0.0  # Si no se encuentra el itemsapname, el precio será 0
        
        # Obtener las libras y cajas
        libras = cleaned_data.get('libras')
        cajas = cleaned_data.get('cajas')
        
        # Si las cajas son 0, evita división por cero
        if cajas > 0:
            libras_por_caja = libras / cajas  # Calcular las libras por caja
        else:
            libras_por_caja = 0  # Si no hay cajas, no calculamos libras por caja

        # Calcular el importe
        importe = precio * cajas
        
        # Guardar los resultados calculados
        cleaned_data['importe'] = importe
        cleaned_data['libras_por_caja'] = libras_por_caja  # Almacenamos libras por caja

        return cleaned_data

