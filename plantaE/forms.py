from django import forms
from .models import Actpeso,usuariosAppFruta, detallesEstructuras, causasRechazo,paramenvlocales,Boletas,salidacontenedores,salidasFruta, productoTerm,contenedores, Recepciones, Ccalidad, inventarioProdTerm,AcumFruta, enviosFrutaPlantilla
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Div

class salidasFrutaForm(forms.ModelForm):

    op_viajes = [('','---------'),('Viaje 1','Viaje 1'),('Viaje 2','Viaje 2'),('Viaje 3', 'Viaje 3'),('Viaje 4','Viaje 4'),('Viaje 5','Viaje 5'),('Viaje 6','Viaje 6'),('Viaje 7','Viaje 7'),('Viaje 8','Viaje 8')]
    #op_cultivo = [('','-'),('CHERRY','CHERRY'),('PEPINO','PEPINO'),('AGUACATE','AGUACATE'),('ROMA','ROMA'),('PITAYA','PITAYA'),('MEDLEY','MEDLEY'),('GRAPE','GRAPE'),('GRAPE ORGANICO','GRAPE ORGANICO'),('CHERRY ORGANICO','CHERRY ORGANICO'),('BLOCKY','BLOCKY'),('BLOCKY ORGANICO','BLOCKY ORGANICO'),('MINI','MINI'),('MINI ORGANICO','MINI ORGANICO')]
    
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type':'date','class': 'form-control'}))
    correo = forms.CharField(widget=forms.Select(attrs={'class': 'form-control'}))  # Campo de correo electrónico
    encargado = forms.CharField(widget=forms.Select(attrs={'class': 'form-control'}))  # Campo de texto
    finca = forms.CharField(widget=forms.Select(attrs={'class': 'form-control'}))  # Campo de texto
    variedad = forms.CharField(widget=forms.Select(attrs={'class': 'form-control'}))  # Campo de texto
    viaje = forms.ChoiceField(choices=op_viajes,widget=forms.Select(attrs={'class': 'form-control'}))  # Campo de texto
    cajas = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))  # Campo numérico
    cultivo = forms.CharField(widget=forms.Select(attrs={'class': 'form-control'}))  # Campo de texto
    
    class Meta:
    
        model = salidasFruta
        fields = ['correo','fecha','viaje','encargado',  'finca', 'cajas', 'cultivo','variedad']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Valores únicos de cuenta
        cuentas = usuariosAppFruta.objects.order_by('encargado').values_list('encargado', flat=True).distinct()
        self.fields['encargado'].widget = forms.Select(choices=[('', '---------')] + [(c, c) for c in cuentas])
        self.fields['encargado'].widget.attrs.update({'class': 'form-control'})

        # Valores únicos de cuenta
        correos = usuariosAppFruta.objects.order_by('correo').values_list('correo', flat=True).distinct()
        self.fields['correo'].widget = forms.Select(choices=[('', '---------')] + [(c, c) for c in correos])
        self.fields['correo'].widget.attrs.update({'class': 'form-control'})

        # Cultivos únicos
        cultivos = detallesEstructuras.objects.order_by('cultivo').values_list('cultivo', flat=True).distinct()
        self.fields['cultivo'].widget = forms.Select(choices=[('', '---------')] + [(c, c) for c in cultivos])
        self.fields['cultivo'].widget.attrs.update({'class': 'form-control'})

        # Variedades únicos
        variedades = detallesEstructuras.objects.order_by('variedad').values_list('variedad', flat=True).distinct()
        self.fields['variedad'].widget = forms.Select(choices=[('', '---------')] + [(v, v) for v in variedades])
        self.fields['variedad'].widget.attrs.update({'class': 'form-control'})

        # Fincas únicos
        fincas = detallesEstructuras.objects.order_by('finca').values_list('finca', flat=True).distinct()
        self.fields['finca'].widget = forms.Select(choices=[('', '---------')] + [(f, f) for f in fincas])
        self.fields['finca'].widget.attrs.update({'class': 'form-control'})

class pesosForm(forms.ModelForm):

    recepcion = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type':'date','class': 'form-control'}))
    llave = forms.CharField(widget=forms.Select(attrs={'class': 'form-control'}))  # Campo de correo electrónico
    finca = forms.CharField(widget=forms.Select(attrs={'class': 'form-control'}))  # Campo de texto
    cultivo = forms.CharField(widget=forms.Select(attrs={'class': 'form-control'}))  # Campo de texto
    tarimas = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))  # Campo numérico
    cajas = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))  # Campo numérico
    libras = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))  # Campo numérico
    
    class Meta:
    
        model = Actpeso
        fields = ['recepcion','fecha','llave',  'finca', 'cultivo','tarimas','cajas','libras']

class acumFrutaForm(forms.ModelForm):
    
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type':'date','class': 'form-control'}))
    correo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))  # Campo de correo electrónico
    finca = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))  # Campo de texto
    cajas = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))  # Campo numérico
    orden = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))  # Campo de texto
    cultivo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))  # Campo de texto
    variedad = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))  # Campo de texto
    estructura = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))  # Campo de texto
    
    class Meta:
    
        model = AcumFruta
        fields = ['correo','fecha', 'finca', 'cajas', 'orden','cultivo','variedad','estructura']

class recepcionesForm(forms.ModelForm):

    op_status = [('','-'),('Pendiente','-'),('En proceso','En proceso')]

    recepcion = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type':'date','class': 'form-control'}))
    finca = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))  # Campo de texto
    cajas = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))  # Campo numérico
    libras = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))  # Campo numérico
    cultivo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))  # Campo de texto
    observaciones = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))  # Campo de texto
    status = forms.ChoiceField(choices=op_status,widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
    
        model = Recepciones
        fields = ['recepcion','fecha','finca', 'cajas',  'libras', 'cultivo','observaciones','status']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['observaciones'].required = False

class ccalidadForm(forms.ModelForm):

    registro = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type':'date','class': 'form-control'}))
    porcentaje= forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))  # Campo numérico
    llave = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'form-control'}))
    causarechazo = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'form-control'}))

    observaciones = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
   
    class Meta:
    
        model = Ccalidad
        fields = ['registro','fecha','porcentaje',  'llave', 'causarechazo','observaciones']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['observaciones'].required = False
        self.fields['registro'].required = False
        # Si estamos editando
        if self.instance and self.instance.pk:
            # -- CAUSAS DE RECHAZO --
            causas = causasRechazo.objects.all()
            opciones = [(c.causa, c.causa) for c in causas]

            # Si la causa del registro no está en la lista, la añadimos para no perderla
            if self.instance.causarechazo and (self.instance.causarechazo, self.instance.causarechazo) not in opciones:
                opciones.insert(0, (self.instance.causarechazo, self.instance.causarechazo))

            self.fields['causarechazo'].choices = opciones

            # -- LLAVE --
            self.fields['llave'].choices = [(self.instance.llave, self.instance.llave)]
        else:
            # En modo creación: dejar choices vacíos (los llena JavaScript)
            self.fields['llave'].choices = []
            self.fields['causarechazo'].choices = []

class inventarioFrutaForm(forms.ModelForm):

    op_empaque = [('','-'),('Cajas','Cajas'),('Libras','Libras')]
    op_proveedor = [('','-'),('INVERSIONES LA PASTORIA, S.A.','INVERSIONES LA PASTORIA, S.A.'),('SDC','SDC'),('AGROINDUSTRIAS SAN RAFAEL, S.A.','AGROINDUSTRIAS SAN RAFAEL, S.A.'),('INVERNADEROS TECNOLOGICOS S.A','INVERNADEROS TECNOLOGICOS S.A'),('HORTEX, S.A.','HORTEX, S.A.'),('DANIEL ESTUARDO GALICIA CARRERA','DANIEL ESTUARDO GALICIA CARRERA'),('PRODUCTOS DEL VALLE, S.A.','PRODUCTOS DEL VALLE, S.A.')]
    op_cultivo = [('','-'),('CHERRY','CHERRY'),('MEDLEY','MEDLEY'),('GRAPE','GRAPE'),('GRAPE ORGANICO','GRAPE ORGANICO'),('CHERRY ORGANICO','CHERRY ORGANICO'),('BLOCKY','BLOCKY'),('BLOCKY ORGANICO','BLOCKY ORGANICO'),('MINI','MINI'),('MINI ORGANICO','MINI ORGANICO')]
    op_categoria = [('','-'),('Mastronardi','Mastronardi'),('Carreta','Carreta'),('Cenma','Cenma'),('Devolucion','Devolucion')]
    
    registro = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    proveedor = forms.ChoiceField(choices=op_proveedor, widget=forms.Select(attrs={'class': 'form-control'}))
    itemsapcode = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})) 
    itemsapname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))   # Campo de texto
    cajas = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))  # Campo numérico
    libras = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))  # Campo numérico
    lbsintara=forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))  # Campo numérico
    pesostd=forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))  # Campo numérico
    pesosinmerma=forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))  # Campo numérico
    merma=forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))  # Campo numérico
    pesostdxcaja=forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))  # Campo numérico
    pesorxcaja=forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))  # Campo numérico
    
    class Meta:
        
        model = inventarioProdTerm
        fields = ['registro','proveedor','itemsapcode','itemsapname','cajas','libras','lbsintara','pesostd','pesostdxcaja','pesorxcaja','merma','pesosinmerma']
    def clean(self):
        cleaned_data = super().clean()

        # Obtener el nombre del artículo (itemsapname) y buscar el precio
        itemsapcode = cleaned_data.get('itemsapcode')
        try:
            ref2 = productoTerm.objects.get(itemsapcode=itemsapcode)
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

    op_status = [('','-'),('Pendiente','-'),('Cerrado','Cerrado')]
    op_destino = [('','-'),('Jonestown','Jonestown'),('Lakeland','Lakeland'),('Laredo, Texas','Laredo, Texas'),('Miami','Miami')]
    op_naviera = [('','-'),('SEABOARD','SEABOARD'),('CROWLEY','CROWLEY')]

    fecha = forms.DateField(widget=forms.DateInput(attrs={'type':'date','class': 'form-control'}))
    eta = forms.DateField(widget=forms.DateInput(attrs={'type':'date','class': 'form-control'}))
    etd = forms.DateField(widget=forms.DateInput(attrs={'type':'date','class': 'form-control'}))
    destino = forms.ChoiceField(choices=op_destino, widget=forms.Select(attrs={'class': 'form-control'}))
    contenedor = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    bl = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    booking = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    transportista = forms.ChoiceField(choices=op_naviera, widget=forms.Select(attrs={'class': 'form-control'}))
    viaje = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))  # Campo numérico
    piloto = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    temperatura = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))  # Campo numérico
    ventilacion = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))  # Campo numérico
    marchamo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    placacamion = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    horasalida = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control'}))  # Campo numérico
    
    class Meta:
        
        model = contenedores
        fields = ['fecha','destino','contenedor','transportista','viaje','piloto','temperatura', 'ventilacion', 'marchamo', 'placacamion','horasalida','eta','etd','bl','booking']

class itemsForm(forms.ModelForm):

    op_cultivo =   [('','-'),('ROMA','ROMA'),('AGUACATE','AGUACATE'),('PEPINO','PEPINO'),('PITAYA','PITAYA'),('ARANDANO','ARANDANO'),('CHERRY','CHERRY'),('MEDLEY','MEDLEY'),('BEEF','BEEF'),('SALADETTE','SALADETTE'),('GRAPE','GRAPE'),('GRAPE ORGANICO','GRAPE ORGANICO'),('CHERRY ORGANICO','CHERRY ORGANICO'),('BLOCKY','BLOCKY'),('BLOCKY ORGANICO','BLOCKY ORGANICO'),('MINI','MINI'),('MINI ORGANICO','MINI ORGANICO')]
    op_categoria = [('','-'),('Exportación','Exportación'),('Carreta','Carreta'),('Cenma','Cenma'),('Devolución','Devolución')]
    op_tipo =      [('','-'),('Tomate','Tomate'),('Aguacate','Aguacate'),('Chile','Chile'),('Arandano','Arandano'),('Pitaya','Pitaya'),('Pepino','Pepino')]
    
    cultivo = forms.ChoiceField(choices=op_cultivo, widget=forms.Select(attrs={'class': 'form-control'}))
    itemsapcode = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    itemsapname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    itemsapcodelibra = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    calidad1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    categoria = forms.ChoiceField(choices=op_categoria, widget=forms.Select(attrs={'class': 'form-control'}))
    precio = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'})) 
    taraxcaja = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'})) 
    pesostdxcaja = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'})) 
    tipo = forms.ChoiceField(choices=op_tipo, widget=forms.Select(attrs={'class': 'form-control'}))  # Campo numérico
    orden = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        
        model = productoTerm
        fields = ['cultivo','itemsapcode','itemsapcodelibra','itemsapname','calidad1','categoria','precio','taraxcaja', 'pesostdxcaja', 'tipo', 'orden']

class itemsenviosForm(forms.ModelForm):

    op_clasificacion =   [('','-'),('EMPAQUE','EMPAQUE'),('FRUTA','FRUTA'),('FERRETERIA','FERRETERIA')]
    op_almacen = [('','-'),('PH-0100','PH-0100'),('PH-0200','PH-0200'),('PH-0400','PH-0400'),('PH-0600','PH-0600'),('PH-0603','PH-0603'),('02','02')]
    op_rubro =   [('','-'),('Empaque','Empaque'),('Fruta','Fruta'),('Insumos','Insumos'),('MAT.LIMPIEZA','MAT.LIMPIEZA')]
    op_grupo =   [('','-'),('Empaque','Empaque'),('Fruta','Fruta'),('MAT.LIMPIEZA','MAT.LIMPIEZA'),('Insumos','Insumos')]
    u_m =   [('','-'),('gl','gl'),('kg','kg'),('g','g'),('lb','lb'),('lt','lt'),('mil','mil'),('millar','millar'),('und','und'),('mts','mts'),('pie','pie'),('par','par'),('rl','rl')]
    
    item = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    descripcion = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    u_m = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    clasificacion = forms.ChoiceField(choices=op_clasificacion, widget=forms.Select(attrs={'class': 'form-control'}))
    almacen = forms.ChoiceField(choices=op_almacen, widget=forms.Select(attrs={'class': 'form-control'}))
    grupo = forms.ChoiceField(choices=op_grupo, widget=forms.Select(attrs={'class': 'form-control'}))
    rubro = forms.ChoiceField(choices=op_rubro, widget=forms.Select(attrs={'class': 'form-control'}))
    
    class Meta:
        
        model = paramenvlocales
        fields = ['item','descripcion','u_m','clasificacion','almacen','grupo','rubro']

    
class salidacontenedoresForm(forms.ModelForm):
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type':'date','class': 'form-control'}))
    contenedor = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    palet = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    proveedor = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    cultivo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    itemsapname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    cajas = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly':'readonly'}))  # Campo numérico
    importe = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    lbsintara = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly':'readonly'}))  # Campo numérico
    pesorxcaja = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly':'readonly'}))  # Campo numérico
    pesostd = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly':'readonly'}))  # Campo numérico
    pesostdxcaja = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly':'readonly'}))  # Campo numérico
    pesosinmerma = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly':'readonly'}))  # Campo numérico
    merma = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly':'readonly'}))  # Campo numérico
    
    libras_por_caja = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))

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


class boletasForm(forms.ModelForm):
    
    registro = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type':'date','class': 'form-control'}))
    boleta = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    finca = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    ordenfinca = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    proveedor = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    cultivo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    orden = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    calidad1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    itemsapname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly':'readonly'}))  # Campo numérico
    calidad = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    cajas = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    librasxcaja = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    libras = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    observaciones = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Boletas
        fields = ['fecha', 'registro','boleta','finca', 'ordenfinca','proveedor','cultivo','orden','calidad1','itemsapname','calidad' , 'cajas', 'librasxcaja', 'libras','observaciones']

