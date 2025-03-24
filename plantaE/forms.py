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
    cajas = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'}))  # Campo numérico
    libras = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'}))  # Campo numérico
    lbsintara=forms.FloatField(widget=forms.NumberInput(attrs={'class': 'my-input', 'readonly': 'readonly'}))  # Campo numérico
    pesostd=forms.FloatField(widget=forms.NumberInput(attrs={'class': 'my-input', 'readonly': 'readonly'}))  # Campo numérico
    pesosinmerma=forms.FloatField(widget=forms.NumberInput(attrs={'class': 'my-input', 'readonly': 'readonly'}))  # Campo numérico
    merma=forms.FloatField(widget=forms.NumberInput(attrs={'class': 'my-input', 'readonly': 'readonly'}))  # Campo numérico
    pesostdxcaja=forms.FloatField(widget=forms.NumberInput(attrs={'class': 'my-input', 'readonly': 'readonly'}))  # Campo numérico
    pesorxcaja=forms.FloatField(widget=forms.NumberInput(attrs={'class': 'my-input', 'readonly': 'readonly'}))  # Campo numérico
    
    class Meta:
        
        model = inventarioProdTerm
        fields = ['registro','proveedor','itemsapname','cajas','libras','lbsintara','pesostd','pesostdxcaja','pesorxcaja','merma','pesosinmerma']
    def clean(self):
        cleaned_data = super().clean()

        # Obtener el nombre del artículo (itemsapname) y buscar el precio
        itemsapname = cleaned_data.get('itemsapname')
        try:
            ref2 = productoTerm.objects.get(itemsapname=itemsapname)
            taraxcaja = ref2.taraxcaja if ref2.taraxcaja else 0.0
            pesostdxcaja = ref2.pesostdxcaja if ref2.pesostdxcaja else 0.0
        except productoTerm.DoesNotExist:
            precio = 0.0  # Si no se encuentra el itemsapname, el precio será 0
        
        # Obtener las libras y las cajas
        pesorxcaja = cleaned_data.get('pesorxcaja')
        
        libras = cleaned_data.get('libras')
        cajas = cleaned_data.get('cajas')
        
        tara = taraxcaja*cajas
        lbsintara = libras-tara
        pesorxcaja = lbsintara/cajas
        pesostd = pesostdxcaja*cajas
        if lbsintara - pesostd > 0:
            merma = lbsintara - pesostd
            pesosinmerma = lbsintara-merma
        else:
            merma = 0 
            pesosinmerma = lbsintara
    
        # Recalcular las libras totales después de la actualización de las cajas
        if cajas > 0:
            total_libras = float(pesorxcaja) * cajas  # Recalcular libras totales
        else:
            total_libras = 0  # Si no hay cajas, el total de libras es 0

        # Guardar los valores calculados en cleaned_data
        cleaned_data['pesostd'] = pesostd
        cleaned_data['lbsintara'] = total_libras  # Guardamos el valor de libras totales
        cleaned_data['pesorxcaja'] = total_libras/cajas  # Guardamos el valor de libras totales
        cleaned_data['pesostdxcaja'] = pesostdxcaja  # Guardamos el valor de libras totales
        cleaned_data['tara'] =   tara# Guardamos el valor de libras totales

        if float(cleaned_data['lbsintara'])-float(cleaned_data['pesostd'])>0:
            cleaned_data['merma'] = float(cleaned_data['lbsintara'])-float(cleaned_data['pesostd'])  # Guardamos el valor de libras totales
            cleaned_data['pesosinmerma'] = float(cleaned_data['lbsintara'])-float(cleaned_data['merma'])  # Guardamos el valor de libras totales
        else:
            cleaned_data['merma'] = 0  # Guardamos el valor de libras totales
            cleaned_data['pesosinmerma'] = float(cleaned_data['lbsintara'])  # Guardamos el valor de libras totales
        
            
        return cleaned_data

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
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type':'date','class': 'my-input'}))
    contenedor = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input', 'readonly': 'readonly'}))
    palet = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'}))
    proveedor = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input', 'readonly': 'readonly'}))
    cultivo = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input', 'readonly': 'readonly'}))
    itemsapname = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input', 'readonly': 'readonly'}))
    cajas = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'}))  # Campo numérico
    importe = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'class': 'my-input', 'readonly': 'readonly'}))
    lbsintara = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'my-input', 'readonly':'readonly'}))  # Campo numérico
    pesorxcaja = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'my-input', 'readonly':'readonly'}))  # Campo numérico
    pesostd = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'my-input', 'readonly':'readonly'}))  # Campo numérico
    pesostdxcaja = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'my-input', 'readonly':'readonly'}))  # Campo numérico
    pesosinmerma = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'my-input', 'readonly':'readonly'}))  # Campo numérico
    merma = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'my-input', 'readonly':'readonly'}))  # Campo numérico
    
    libras_por_caja = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'class': 'my-input', 'readonly': 'readonly'}))

    class Meta:
        model = salidacontenedores
        fields = ['fecha', 'contenedor','pesorxcaja','pesostdxcaja','pesostd','pesosinmerma','merma', 'palet', 'proveedor', 'cultivo', 'itemsapname', 'cajas', 'importe', 'lbsintara', 'libras_por_caja']

    def clean(self):
        cleaned_data = super().clean()

        # Obtener el nombre del artículo (itemsapname) y buscar el precio
        itemsapname = cleaned_data.get('itemsapname')
        try:
            ref2 = productoTerm.objects.get(itemsapname=itemsapname)
            precio = ref2.precio if ref2.precio else 0.0
        except productoTerm.DoesNotExist:
            precio = 0.0  # Si no se encuentra el itemsapname, el precio será 0
        
        # Obtener las libras y las cajas
        pesorxcaja = cleaned_data.get('pesorxcaja')
        cajas = cleaned_data.get('cajas')

        # Calcular el importe
        importe = precio * cajas
        
        # Recalcular las libras totales después de la actualización de las cajas
        if cajas > 0:
            total_libras = float(pesorxcaja) * cajas  # Recalcular libras totales
        else:
            total_libras = 0  # Si no hay cajas, el total de libras es 0

        # Guardar los valores calculados en cleaned_data
        cleaned_data['importe'] = importe
        cleaned_data['lbsintara'] = total_libras  # Guardamos el valor de libras totales
        cleaned_data['pesorxcaja'] = total_libras/cajas  # Guardamos el valor de libras totales
        
        cleaned_data['pesostd'] =   cleaned_data['pesostdxcaja']*cajas# Guardamos el valor de libras totales
        if float(cleaned_data['lbsintara'])-float(cleaned_data['pesostd'])>0:
            cleaned_data['merma'] = float(cleaned_data['lbsintara'])-float(cleaned_data['pesostd'])  # Guardamos el valor de libras totales
            cleaned_data['pesosinmerma'] = float(cleaned_data['lbsintara'])-float(cleaned_data['merma'])  # Guardamos el valor de libras totales
        else:
            cleaned_data['merma'] = 0  # Guardamos el valor de libras totales
            cleaned_data['pesosinmerma'] = float(cleaned_data['lbsintara'])  # Guardamos el valor de libras totales
        
            
        return cleaned_data


