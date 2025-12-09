from django import forms
from .models import Actpeso,tipoCajas,pedidos,controlcajas,usuariosAppFruta,detallerec, detallesEstructuras, causasRechazo,paramenvlocales,Boletas,salidacontenedores,salidasFruta, productoTerm,contenedores, Recepciones, Ccalidad, inventarioProdTerm,AcumFruta, enviosFrutaPlantilla
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Div
from django.db.models import Sum

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
        fields = ['correo','fecha','viaje','encargado', 'orden', 'finca', 'cajas', 'cultivo','variedad']
    
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

        # Fincas únicos
        ordenes = detallesEstructuras.objects.order_by('orden').values_list('orden', flat=True).distinct()
        self.fields['orden'].widget = forms.Select(choices=[('', '---------')] + [(f, f) for f in ordenes])
        self.fields['orden'].widget.attrs.update({'class': 'form-control'})

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

    op_viajes = [
        ('', '---------'), ('Viaje 1', 'Viaje 1'), ('Viaje 2', 'Viaje 2'), ('Viaje 3', 'Viaje 3'),
        ('Viaje 4', 'Viaje 4'), ('Viaje 5', 'Viaje 5'), ('Viaje 6', 'Viaje 6'),
        ('Viaje 7', 'Viaje 7'), ('Viaje 8', 'Viaje 8')
    ]
    viaje = forms.ChoiceField(choices=op_viajes, widget=forms.Select(attrs={'class': 'form-control'}))
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    cajas = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    
    correo = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'form-control'}))
    finca = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'form-control'}))
    orden = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'form-control'}))
    cultivo = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'form-control'}))
    variedad = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'form-control'}))
    estructura = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'form-control'}))
    encargado = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = AcumFruta
        fields = ['correo', 'fecha', 'finca', 'cajas', 'orden', 'cultivo', 'variedad', 'estructura', 'viaje', 'encargado']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            # Encargado
            cuentas = usuariosAppFruta.objects.order_by('encargado').values_list('encargado', flat=True).distinct()
            opciones_encargado = [('', '---------')] + [(c, c) for c in cuentas]

            # Agregar el valor actual si no está en las opciones
            if self.instance.encargado and (self.instance.encargado, self.instance.encargado) not in opciones_encargado:
                opciones_encargado.insert(0, (self.instance.encargado, self.instance.encargado))
            self.fields['encargado'].choices = opciones_encargado

            # Repetir para estructura
            estructuras = detallesEstructuras.objects.order_by('estructura').values_list('estructura', flat=True).distinct()
            opciones_estructura = [('', '---------')] + [(e, e) for e in estructuras]
            if self.instance.estructura and (self.instance.estructura, self.instance.estructura) not in opciones_estructura:
                opciones_estructura.insert(0, (self.instance.estructura, self.instance.estructura))
            self.fields['estructura'].choices = opciones_estructura

            # Correo
            correos = usuariosAppFruta.objects.order_by('correo').values_list('correo', flat=True).distinct()
            opciones_correo = [('', '---------')] + [(c, c) for c in correos]
            if self.instance.correo and (self.instance.correo, self.instance.correo) not in opciones_correo:
                opciones_correo.insert(0, (self.instance.correo, self.instance.correo))
            self.fields['correo'].choices = opciones_correo

            # Cultivo
            cultivos = detallesEstructuras.objects.order_by('cultivo').values_list('cultivo', flat=True).distinct()
            opciones_cultivo = [('', '---------')] + [(c, c) for c in cultivos]
            if self.instance.cultivo and (self.instance.cultivo, self.instance.cultivo) not in opciones_cultivo:
                opciones_cultivo.insert(0, (self.instance.cultivo, self.instance.cultivo))
            self.fields['cultivo'].choices = opciones_cultivo

            # Variedad
            variedades = detallesEstructuras.objects.order_by('variedad').values_list('variedad', flat=True).distinct()
            opciones_variedad = [('', '---------')] + [(v, v) for v in variedades]
            if self.instance.variedad and (self.instance.variedad, self.instance.variedad) not in opciones_variedad:
                opciones_variedad.insert(0, (self.instance.variedad, self.instance.variedad))
            self.fields['variedad'].choices = opciones_variedad

            # Finca
            fincas = detallesEstructuras.objects.order_by('finca').values_list('finca', flat=True).distinct()
            opciones_finca = [('', '---------')] + [(f, f) for f in fincas]
            if self.instance.finca and (self.instance.finca, self.instance.finca) not in opciones_finca:
                opciones_finca.insert(0, (self.instance.finca, self.instance.finca))
            self.fields['finca'].choices = opciones_finca

            # Orden
            ordenes = detallesEstructuras.objects.order_by('orden').values_list('orden', flat=True).distinct()
            opciones_orden = [('', '---------')] + [(o, o) for o in ordenes]
            if self.instance.orden and (self.instance.orden, self.instance.orden) not in opciones_orden:
                opciones_orden.insert(0, (self.instance.orden, self.instance.orden))
            self.fields['orden'].choices = opciones_orden


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

        # === LLAVES (cargadas desde backend sin AJAX) ===
        suma_por_llave = Ccalidad.objects.values('llave').annotate(suma=Sum('porcentaje'))
        suma_dict = {item['llave']: item['suma'] for item in suma_por_llave}

        datos = detallerec.objects.filter(recepcion__gte=2875)
        datos_modificados = []

        for item in datos:
            fecha = item.fechasalidafruta
            semana = fecha.isocalendar()[1] if fecha else ''
            if item.finca == "Productor":
                clave = f"{semana} | {item.llave} | {item.cultivo}"
            else:
                clave = f"{semana} | {item.finca} | {item.cultivo}"
            datos_modificados.append(clave)

        datos_modificados = list(set(datos_modificados))
        datos_modificados = [
            clave for clave in datos_modificados if suma_dict.get(clave, 0) < 1
        ]
        self.fields['llave'].choices = [('', '---------')] + [(clave, clave) for clave in datos_modificados]

        # === CAUSAS DE RECHAZO (también desde backend sin AJAX) ===
        causas = causasRechazo.objects.all()
        opciones_causa = [(c.causa, c.causa) for c in causas]

        # Si estamos editando y la causa no está en la lista, la agregamos
        if self.instance and self.instance.pk:
            if self.instance.causarechazo and (self.instance.causarechazo, self.instance.causarechazo) not in opciones_causa:
                opciones_causa.insert(0, (self.instance.causarechazo, self.instance.causarechazo))
        else:
            # Si estamos en creación, también incluir el valor del POST si viene
            data = kwargs.get('data')
            causa_valor = data.get('causarechazo') if data else None
            if causa_valor and (causa_valor, causa_valor) not in opciones_causa:
                opciones_causa.insert(0, (causa_valor, causa_valor))

        self.fields['causarechazo'].choices = [('', '---------')] + opciones_causa




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
    orden=forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control'})) 
    class Meta:
        
        model = inventarioProdTerm
        fields = ['registro','proveedor','itemsapcode','itemsapname','cajas','libras','lbsintara','pesostd','pesostdxcaja','pesorxcaja','merma','pesosinmerma','orden']
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
    orden2 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    cajasxtarima = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    
    empaque= forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        
        model = productoTerm
        fields = ['cultivo','empaque','orden2','cajasxtarima','itemsapcode','itemsapcodelibra','itemsapname','calidad1','categoria','precio','taraxcaja', 'pesostdxcaja', 'tipo', 'orden']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['itemsapcodelibra'].required = False
        self.fields['orden'].required = False
        self.fields['orden2'].required = False
        self.fields['taraxcaja'].required = False
        self.fields['precio'].required = False
        self.fields['calidad1'].required = False
        self.fields['cajasxtarima'].required = False
        
        self.fields['empaque'].required = False

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

class controlcajasForm(forms.ModelForm):

    # Field Choices
    l_entra = [('','-'),('PLANTAE','PLANTAE'),('RIO','RIO'),('VALLE','VALLE'),('SEMILLAS','SEMILLAS'),('PRODUCTOS DEL VALLE, S.A.','PRODUCTOS DEL VALLE, S.A.'),('FLE','FLE'),('CENMA','CENMA'),('SANDRA MARTINEZ','SANDRA MARTINEZ'),('FINCA LA PASTORIA, S.A.','FINCA LA PASTORIA, S.A.'),('LA CARRETA “AMATITLAN”','LA CARRETA “AMATITLAN”'),('CATAGUANA/GUATEBERRIES','CATAGUANA/GUATEBERRIES')]
    l_sale = [('','-'),('PLANTAE','PLANTAE'),('RIO','RIO'),('VALLE','VALLE'),('SEMILLAS','SEMILLAS'),('PRODUCTOS DEL VALLE, S.A.','PRODUCTOS DEL VALLE, S.A.'),('FLE','FLE'),('CENMA','CENMA'),('SANDRA MARTINEZ','SANDRA MARTINEZ'),('FINCA LA PASTORIA, S.A.','FINCA LA PASTORIA, S.A.'),('LA CARRETA “AMATITLAN”','LA CARRETA “AMATITLAN”'),('CATAGUANA/GUATEBERRIES','CATAGUANA/GUATEBERRIES')]
    op_mov = [('','-'),('Entrega','Entrega'),('Recepción','Recepción')]
    op_encargado = [('','-'),('Sandra Martínez','Sandra Martínez'),('Kimberly','Kimberly'),('Alfonso Samayoa','Alfonso Samayoa'),('Carlos Hernández','Carlos Hernández'),('Jhony Tecún','Jhony Tecún'),('Ariel Parada','Ariel Parada'),('Gonzalo Mayén','Gonzalo Mayén'),('Carlos Virula','Carlos Virula'),('Crishanda Solares','Crishanda Solares'),('Saul Ruano','Saul Ruano')]
    # Fields
    cajas = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    lugar_entra = forms.ChoiceField(choices=l_entra, widget=forms.Select(attrs={'class': 'form-control'}))
    lugar_sale = forms.ChoiceField(choices=l_sale, widget=forms.Select(attrs={'class': 'form-control'}))
    tipomov = forms.ChoiceField(choices=op_mov, widget=forms.Select(attrs={'class': 'form-control'}))
    encargado = forms.ChoiceField(choices=op_encargado, widget=forms.Select(attrs={'class': 'form-control'}))
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type':'date','class': 'form-control'}))

    # Dynamic Choice Fields (initialized in __init__)
    itemsapcode = forms.ChoiceField(
        choices=[], required=False, 
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_itemsapcode'})
    )
    tipodecaja = forms.ChoiceField(
        choices=[], 
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_tipodecaja'})
    )

    class Meta:
        model = controlcajas
        fields = ['itemsapcode','tipodecaja','cajas','lugar_entra','lugar_sale','tipomov','fecha']

    def __init__(self, *args, **kwargs):
        super(controlcajasForm, self).__init__(*args, **kwargs)
        # Assuming tipoCajas.objects is accessible and works as intended
        items_qs = tipoCajas.objects.exclude(itemsapcode__isnull=True).exclude(itemsapcode='')

        
        # Populate dynamic choices
        self.fields['itemsapcode'].choices = [('', '-')] + [(v.itemsapcode, v.itemsapcode) for v in items_qs]
        self.fields['tipodecaja'].choices = [('', '-')] + [(v.tcaja, v.tcaja) for v in items_qs]

    def clean(self):
        # Call the base clean method to get cleaned data
        cleaned_data = super().clean()
        
        cajas = cleaned_data.get('cajas')
        tipomov = cleaned_data.get('tipomov')

        # Only proceed if both fields have values
        if cajas is not None and tipomov:
            # Check for 'Entrega' (Delivery)
            if tipomov == 'Entrega':
                # If Entrega, boxes must be negative.
                # Use abs() to ensure the number is negative regardless of input
                cleaned_data['cajas'] = -abs(cajas)
            
            # Check for 'Recepcion' (Reception)
            elif tipomov == 'Recepcion':
                # If Recepcion, boxes must be positive.
                # Use abs() to ensure the number is positive regardless of input
                cleaned_data['cajas'] = abs(cajas)

        return cleaned_data

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
    op_categoria = [('','-'),('Aprovechamiento','Aprovechamiento'),('Mediano','Mediano'),('Devolución','Devolución')]
    
    registro = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type':'date','class': 'form-control'}))
    boleta = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    finca = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    ordenfinca = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    proveedor = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    cultivo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    orden = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    calidad1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    itemsapname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly':'readonly'}))  # Campo numérico
    calidad = forms.ChoiceField(choices=op_categoria, widget=forms.Select(attrs={'class': 'form-control'}))
    cajas = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    librasxcaja = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    libras = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    observaciones = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Boletas
        fields = ['fecha', 'registro','boleta','finca', 'ordenfinca','proveedor','cultivo','orden','calidad1','itemsapname','calidad' , 'cajas', 'librasxcaja', 'libras','observaciones']
    
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.fields['observaciones'].required = False
        self.fields['orden'].required = False
        self.fields['ordenfinca'].required = False


class pedidosForm(forms.ModelForm):

    id = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    fechaentrega = forms.DateField(widget=forms.DateInput(attrs={'type':'date','class': 'form-control'}))
    cultivo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    itemsapcode = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    itemsapname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    categoria = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    precio = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'})) 
    cantidad = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'})) 
    
    class Meta:
        
        model = pedidos
        fields = ['id','fechaentrega','cultivo','itemsapcode','itemsapname','categoria','precio', 'cantidad']
    
