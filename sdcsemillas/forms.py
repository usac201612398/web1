from django import forms
from .models import *
from django import forms
from .models import lotes, variedades


class lotesForm(forms.ModelForm):

    op_ubicacion = [('', '-'), ('SL', 'SL'), ('CIP', 'CIP'), ('Cecilio', 'Cecilio'), ('Bella Vista', 'Bella Vista')]
    op_modulo = [('', '-')] + [(f'Modulo {i}', f'Modulo {i}') for i in range(1, 12)]
    op_invernadero = [('', '-')] + [(f'Invernadero {i}', f'Invernadero {i}') for i in range(1, 12)]
    op_malla = [('', '-'), ('Casa Malla', 'Casa Malla')]
    op_estructura = op_invernadero + op_modulo + op_malla
    op_cultivo = [('', '-'), ('Chile', 'Chile'), ('Tomate', 'Tomate')]
    op_status = [('', '-'), ('En proceso', 'En proceso'), ('Finalizado', 'Finalizado'), ('Anulado', 'Anulado')]
    op_metodos = [('', '-'), ('Greenhouse', 'Greenhouse'), ('Macrotunel', 'Macrotunel'), ('Nethouse', 'Nethouse')]
    
    lote_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    apodo_variedad = forms.ChoiceField(
        choices=[],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_apodo_variedad'})
    )
    variedad_code = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_variedad_code'})
    )

    cultivo = forms.ChoiceField(choices=op_cultivo, widget=forms.Select(attrs={'class': 'form-control'}))
    ubicación = forms.ChoiceField(choices=op_ubicacion, widget=forms.Select(attrs={'class': 'form-control'}))
    estructura = forms.ChoiceField(choices=op_estructura, widget=forms.Select(attrs={'class': 'form-control'}))

    plantas_padre = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    plantas_madre = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

    harvest_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    status = forms.ChoiceField(choices=op_status, widget=forms.Select(attrs={'class': 'form-control'}))

    siembra_madre = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control','type':'date'}))
    metodo_prod = forms.ChoiceField(choices=op_metodos, widget=forms.Select(attrs={'class': 'form-control'}))

    target = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    surface = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

    observaciones = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )

    shipment_hub = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    tipo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    as_per_SDCMale = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    as_per_SDCFemale = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = lotes
        fields = [
            'lote_code', 'variedad_code', 'apodo_variedad', 'cultivo',
            'ubicación', 'estructura', 'plantas_padre', 'plantas_madre',
            'harvest_code', 'status', 'siembra_madre', 'metodo_prod',
            'target', 'surface', 'observaciones','shipment_hub','tipo','as_per_SDCMale','as_per_SDCFemale'
        ]

    def __init__(self, *args, **kwargs):
        super(lotesForm, self).__init__(*args, **kwargs)
        variedades_qs = variedades.objects.all()
        self.fields['variedad_code'].choices = [('', '-')] + [(v.variedad_code, v.variedad_code) for v in variedades_qs]
        self.fields['apodo_variedad'].choices = [('', '-')] + [(v.apodo_variedad, v.apodo_variedad) for v in variedades_qs]

class variedadesForm(forms.ModelForm):

    op_cultivo = [('','-'),('Chile','Chile'),('Tomate','Tomate')]
    
    #op_status = [('','-'),('En proceso','En proceso'),('Finalizado','Finalizado'),('Anulado','Anulado')]

    variedad_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))  
    apodo_variedad = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    cultivo = forms.ChoiceField(choices=op_cultivo,widget=forms.Select(attrs={'class': 'form-control'})) 
    cod_padre = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))  
    cod_madre = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'})) 
    #status = forms.ChoiceField(choices=op_status,widget=forms.Select(attrs={'class': 'my-input'}))
    
    class Meta:
    
        model = variedades
        fields = ['variedad_code','apodo_variedad','cultivo', 'cod_padre','cod_madre']

class conteoplantasForm(forms.ModelForm):

    op_ubicacion = [('','-'),('SL','SL'),('CIP','CIP'),('Cecilio', 'Cecilio'),('Bella Vista', 'Bella Vista')]
    op_modulo = [('','-'),('Modulo 1','Modulo 1'),('Modulo 2','Modulo 2'),('Modulo 3', 'Modulo 3'),('Modulo 4','Modulo 4'),('Modulo 5','Modulo 5'),('Modulo 6', 'Modulo 6'),('Modulo 7','Modulo 7'),('Modulo 8','Modulo 8'),('Modulo 9', 'Modulo 9'),('Modulo 10','Modulo 10'),('Modulo 11','Modulo 11')]
    op_invernadero = [('','-'),('Invernadero 1','Invernadero 1'),('Invernadero 2','Invernadero 2'),('Invernadero 3', 'Invernadero 3'),('Invernadero 4','Invernadero 4'),('Invernadero 5','Invernadero 5'),('Invernadero 6', 'Invernadero 6'),('Invernadero 7','Invernadero 7'),('Invernadero 8','Invernadero 8'),('Invernadero 9', 'Invernadero 9'),('Invernadero 10','Invernadero 10'),('Invernadero 11','Invernadero 11')]
    op_malla = [('','-'),('Casa Malla','Casa Malla')]
    op_cultivo = [('','-'),('Chile','Chile'),('Tomtate','Tomate')]
    op_status = [('','-'),('En proceso','En proceso'),('Finalizado','Finalizado')]
    op_estructura = op_invernadero + op_modulo + op_malla
    
    op_eventos = [('','-'),('Al transplante','Al transplante'),('Polinización','Polinización'),('Cosecha','Cosecha')]

    codigo_lote = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control','readonly': 'readonly'}))
    supervisor_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}))
    ubicacion_lote = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'})) 
    apodo_variedad = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}))
    tipo_cultivo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'})) 
    #codigo_planta = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))  
    codigo_madre = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'})) 
    plantas_activas = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'})) 
    plantas_faltantes = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'})) 
    fecha = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control','type': 'date'}))
    camas_completas = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'})) 
    camas_incompletas = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'})) 
    cocosxcamaincompleta = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'})) 
    estructura = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}))  
    status = forms.ChoiceField(choices=op_status,widget=forms.Select(attrs={'class': 'form-control'}))
    evento = forms.ChoiceField(choices=op_eventos,widget=forms.Select(attrs={'class': 'form-control'}))
    observaciones = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))  

    class Meta:
    
        model = conteoplantas
        fields = ['codigo_lote','supervisor_name','ubicacion_lote','apodo_variedad','tipo_cultivo','codigo_madre','plantas_activas','plantas_faltantes','fecha','camas_completas','camas_incompletas','cocosxcamaincompleta', 'estructura', 'status','evento','observaciones']
   
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        
        self.fields['plantas_activas'].required = False
        self.fields['plantas_faltantes'].required = False
        self.fields['camas_completas'].required = False
        self.fields['camas_incompletas'].required = False
        self.fields['cocosxcamaincompleta'].required = False
        self.fields['observaciones'].required = False

class conteosemillasForm(forms.ModelForm):

    op_ubicacion = [('','-'),('SL','SL'),('CIP','CIP'),('Cecilio', 'Cecilio'),('Bella Vista', 'Bella Vista')]
    op_modulo = [('','-'),('Modulo 1','Modulo 1'),('Modulo 2','Modulo 2'),('Modulo 3', 'Modulo 3'),('Modulo 4','Modulo 4'),('Modulo 5','Modulo 5'),('Modulo 6', 'Modulo 6'),('Modulo 7','Modulo 7'),('Modulo 8','Modulo 8'),('Modulo 9', 'Modulo 9'),('Modulo 10','Modulo 10'),('Modulo 11','Modulo 11')]
    op_invernadero = [('','-'),('Invernadero 1','Invernadero 1'),('Invernadero 2','Invernadero 2'),('Invernadero 3', 'Invernadero 3'),('Invernadero 4','Invernadero 4'),('Invernadero 5','Invernadero 5'),('Invernadero 6', 'Invernadero 6'),('Invernadero 7','Invernadero 7'),('Invernadero 8','Invernadero 8'),('Invernadero 9', 'Invernadero 9'),('Invernadero 10','Invernadero 10'),('Invernadero 11','Invernadero 11')]
    op_malla = [('','-'),('Casa Malla','Casa Malla')]
    op_cultivo = [('','-'),('Chile','Chile'),('Tomtate','Tomate')]
    op_status = [('','-'),('En proceso','En proceso'),('Finalizado','Finalizado')]
    op_estructura = op_invernadero + op_modulo + op_malla
    op_clasificacion = [('','-'),('Fruto maduro','Fruto maduro'),('Fruto verde','Fruto verde')]
    op_semana = [('','-'),(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),(6,'6')]
    nsemana = forms.ChoiceField(choices=op_semana,widget=forms.Select(attrs={'class': 'form-control'}))
    codigo_lote = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control','readonly': 'readonly'}))
    codigo_empleado = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}))
    operario_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}))
    supervisor_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}))
    ubicacion_lote = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'})) 
    apodo_variedad = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}))
    tipo_cultivo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'})) 
    cantidad_frutos = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'})) 
    semillasxfruto= forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'})) 
    prom_semillasxfruto = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'})) 
    fecha = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control','type': 'date'}))
    estructura = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}))  
    status = forms.ChoiceField(choices=op_status,widget=forms.Select(attrs={'class': 'form-control'}))
    clasificacion = forms.ChoiceField(choices=op_clasificacion,widget=forms.Select(attrs={'class': 'form-control'}))
    observaciones = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))  

    class Meta:
    
        model = conteosemillas
        fields = ['codigo_lote','codigo_empleado','operario_name','supervisor_name','ubicacion_lote','apodo_variedad','tipo_cultivo','cantidad_frutos','semillasxfruto','prom_semillasxfruto','nsemana','fecha','estructura','status','clasificacion','observaciones']
    
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        
        self.fields['cantidad_frutos'].required = False
        self.fields['semillasxfruto'].required = False
        self.fields['prom_semillasxfruto'].required = False
        self.fields['observaciones'].required = False
        self.fields['codigo_empleado'].required = False
        self.fields['operario_name'].required = False

class conteofrutosForm(forms.ModelForm):

    op_ubicacion = [('','-'),('SL','SL'),('CIP','CIP'),('Cecilio', 'Cecilio'),('Bella Vista', 'Bella Vista')]
    op_modulo = [('','-'),('Modulo 1','Modulo 1'),('Modulo 2','Modulo 2'),('Modulo 3', 'Modulo 3'),('Modulo 4','Modulo 4'),('Modulo 5','Modulo 5'),('Modulo 6', 'Modulo 6'),('Modulo 7','Modulo 7'),('Modulo 8','Modulo 8'),('Modulo 9', 'Modulo 9'),('Modulo 10','Modulo 10'),('Modulo 11','Modulo 11')]
    op_invernadero = [('','-'),('Invernadero 1','Invernadero 1'),('Invernadero 2','Invernadero 2'),('Invernadero 3', 'Invernadero 3'),('Invernadero 4','Invernadero 4'),('Invernadero 5','Invernadero 5'),('Invernadero 6', 'Invernadero 6'),('Invernadero 7','Invernadero 7'),('Invernadero 8','Invernadero 8'),('Invernadero 9', 'Invernadero 9'),('Invernadero 10','Invernadero 10'),('Invernadero 11','Invernadero 11')]
    op_malla = [('','-'),('Casa Malla','Casa Malla')]
    op_cultivo = [('','-'),('Chile','Chile'),('Tomtate','Tomate')]
    op_status = [('','-'),('En proceso','En proceso'),('Finalizado','Finalizado')]
    op_estructura = op_invernadero + op_modulo + op_malla
    
    op_clasificacion = [('','-'),('Autopolinizado','Autopolinizado'),('Postpolinizado','Postpolinizado'),('General','General')]
    
    codigo_empleado = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}))
    codigo_lote = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control','readonly': 'readonly'}))
    operario_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}))
    supervisor_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}))
    ubicacion_lote = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'})) 
    apodo_variedad = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}))
    tipo_cultivo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'})) 
    prom_autopolinizados = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    prom_floresabiertas = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    prom_polinizados = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'})) 
    fecha = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control','type': 'date'}))
    estructura = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}))  
    status = forms.ChoiceField(choices=op_status,widget=forms.Select(attrs={'class': 'form-control'}))
    evento = forms.ChoiceField(choices=op_clasificacion,widget=forms.Select(attrs={'class': 'form-control'}))
    observaciones = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))  

    class Meta:
    
        model = conteofrutos
        fields = ['codigo_lote','codigo_empleado','operario_name','supervisor_name','ubicacion_lote','apodo_variedad','tipo_cultivo','prom_autopolinizados','prom_floresabiertas','prom_polinizados','fecha','estructura','status','evento','observaciones']
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        
        self.fields['prom_autopolinizados'].required = False
        self.fields['prom_floresabiertas'].required = False
        self.fields['prom_polinizados'].required = False
        self.fields['observaciones'].required = False
        self.fields['codigo_empleado'].required = False
        self.fields['operario_name'].required = False

class conteofrutosplanillaForm(forms.ModelForm):

    op_ubicacion = [('','-'),('SL','SL'),('CIP','CIP'),('Cecilio', 'Cecilio'),('Bella Vista', 'Bella Vista')]
    op_modulo = [('','-'),('Modulo 1','Modulo 1'),('Modulo 2','Modulo 2'),('Modulo 3', 'Modulo 3'),('Modulo 4','Modulo 4'),('Modulo 5','Modulo 5'),('Modulo 6', 'Modulo 6'),('Modulo 7','Modulo 7'),('Modulo 8','Modulo 8'),('Modulo 9', 'Modulo 9'),('Modulo 10','Modulo 10'),('Modulo 11','Modulo 11')]
    op_invernadero = [('','-'),('Invernadero 1','Invernadero 1'),('Invernadero 2','Invernadero 2'),('Invernadero 3', 'Invernadero 3'),('Invernadero 4','Invernadero 4'),('Invernadero 5','Invernadero 5'),('Invernadero 6', 'Invernadero 6'),('Invernadero 7','Invernadero 7'),('Invernadero 8','Invernadero 8'),('Invernadero 9', 'Invernadero 9'),('Invernadero 10','Invernadero 10'),('Invernadero 11','Invernadero 11')]
    op_malla = [('','-'),('Casa Malla','Casa Malla')]
    op_cultivo = [('','-'),('Chile','Chile'),('Tomtate','Tomate')]
    op_status = [('','-'),('En proceso','En proceso'),('Finalizado','Finalizado')]
    op_estructura = op_invernadero + op_modulo + op_malla
    
    codigo_empleado = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}))
    codigo_lote = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control','readonly': 'readonly'}))
    operario_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}))
    supervisor_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}))
    ubicacion_lote = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'})) 
    apodo_variedad = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}))
    tipo_cultivo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'})) 
    cama1 = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    cama2 = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    cama3 = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    cama4 = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    cama5 = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    media = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    prom_area = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'})) 
    prom_general = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'})) 
    fecha = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control','type': 'date'}))
    estructura = forms.CharField( widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}))  
    status = forms.ChoiceField(choices=op_status,widget=forms.Select(attrs={'class': 'form-control'}))
    observaciones = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))  

    class Meta:
    
        model = conteofrutosplanilla
        fields = ['codigo_lote','codigo_empleado','operario_name','supervisor_name','ubicacion_lote','apodo_variedad','tipo_cultivo','cama1','cama2','cama3','cama4','cama5','media','prom_area','prom_general','fecha','estructura','status','observaciones']
   
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        
        self.fields['cama1'].required = False
        self.fields['cama2'].required = False
        self.fields['cama3'].required = False
        self.fields['cama4'].required = False
        self.fields['cama5'].required = False
        self.fields['media'].required = False
        self.fields['prom_area'].required = False
        self.fields['prom_general'].required = False
        self.fields['observaciones'].required = False
        self.fields['codigo_empleado'].required = False
        self.fields['operario_name'].required = False

class etapasdeloteForm(forms.ModelForm):

    op_ubicacion = [('','-'),('SL','SL'),('CIP','CIP'),('Cecilio', 'Cecilio'),('Bella Vista', 'Bella Vista')]
    op_modulo = [('','-'),('Modulo 1','Modulo 1'),('Modulo 2','Modulo 2'),('Modulo 3', 'Modulo 3'),('Modulo 4','Modulo 4'),('Modulo 5','Modulo 5'),('Modulo 6', 'Modulo 6'),('Modulo 7','Modulo 7'),('Modulo 8','Modulo 8'),('Modulo 9', 'Modulo 9'),('Modulo 10','Modulo 10'),('Modulo 11','Modulo 11')]
    op_invernadero = [('','-'),('Invernadero 1','Invernadero 1'),('Invernadero 2','Invernadero 2'),('Invernadero 3', 'Invernadero 3'),('Invernadero 4','Invernadero 4'),('Invernadero 5','Invernadero 5'),('Invernadero 6', 'Invernadero 6'),('Invernadero 7','Invernadero 7'),('Invernadero 8','Invernadero 8'),('Invernadero 9', 'Invernadero 9'),('Invernadero 10','Invernadero 10'),('Invernadero 11','Invernadero 11')]
    op_malla = [('','-'),('Casa Malla','Casa Malla')]
    op_cultivo = [('','-'),('Chile','Chile'),('Tomtate','Tomate')]
    op_status = [('','-'),('Inicio','Inicio'),('Fin','Fin')]
    op_estructura = op_invernadero + op_modulo + op_malla
    op_clasificacion = [('','-'),('Cosecha','Cosecha'),('Polinizacion','Polinizacion')]

    #operario_name = forms.ChoiceField(widget=forms.TextInput(attrs={'class': 'my-input'}))
    codigo_lote = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control','readonly': 'readonly'}))
    supervisor_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}))
    ubicacion_lote = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'})) 
    apodo_variedad = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}))
    tipo_cultivo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'})) 
    codigo_madre = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'})) 
    codigo_padre = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'})) 
    fecha = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control','type': 'date'}))
    estructura = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}))  
    status = forms.ChoiceField(choices=op_status,widget=forms.Select(attrs={'class': 'form-control'}))
    evento = forms.ChoiceField(choices=op_clasificacion,widget=forms.Select(attrs={'class': 'form-control'}))
    observaciones = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))  

    class Meta:
    
        model = etapasdelote
        fields = ['codigo_lote','supervisor_name','ubicacion_lote','apodo_variedad','tipo_cultivo','codigo_madre','codigo_padre','fecha','estructura','status','evento','observaciones']

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        
        self.fields['observaciones'].required = False

class ccalidadpolenForm(forms.ModelForm):

    op_ubicacion = [('','-'),('SL','SL'),('CIP','CIP'),('Cecilio', 'Cecilio'),('Bella Vista', 'Bella Vista')]
    op_modulo = [('','-'),('Modulo 1','Modulo 1'),('Modulo 2','Modulo 2'),('Modulo 3', 'Modulo 3'),('Modulo 4','Modulo 4'),('Modulo 5','Modulo 5'),('Modulo 6', 'Modulo 6'),('Modulo 7','Modulo 7'),('Modulo 8','Modulo 8'),('Modulo 9', 'Modulo 9'),('Modulo 10','Modulo 10'),('Modulo 11','Modulo 11')]
    op_invernadero = [('','-'),('Invernadero 1','Invernadero 1'),('Invernadero 2','Invernadero 2'),('Invernadero 3', 'Invernadero 3'),('Invernadero 4','Invernadero 4'),('Invernadero 5','Invernadero 5'),('Invernadero 6', 'Invernadero 6'),('Invernadero 7','Invernadero 7'),('Invernadero 8','Invernadero 8'),('Invernadero 9', 'Invernadero 9'),('Invernadero 10','Invernadero 10'),('Invernadero 11','Invernadero 11')]
    op_malla = [('','-'),('Casa Malla','Casa Malla')]
    op_cultivo = [('','-'),('Chile','Chile'),('Tomtate','Tomate')]
    op_status = [('','-'),('Inicio','Inicio'),('Fin','Fin')]
    op_calidad = [('','-'),('Bueno','Bueno'),('Malo','Malo')]
    op_consistencia = [('','-'),('Normal','Normal'),('Grumosa','Grumosa')]
    op_agexternos= [('','-'),('Insectos','Insectos'),('Restos de vegetales','Restos de vegetales')]
    op_estructura = op_invernadero + op_modulo + op_malla
    
    codigo_lote = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control','readonly': 'readonly'}))
    codigo_empleado = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}))
    operario_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}))
    supervisor_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}))
    ubicacion_lote = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'})) 
    apodo_variedad = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}))
    tipo_cultivo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'})) 
    calidad = forms.ChoiceField(choices=op_calidad,widget=forms.Select(attrs={'class': 'form-control'}))
    consistencia = forms.ChoiceField(choices=op_consistencia,widget=forms.Select(attrs={'class': 'form-control'}))
    ag_externos = forms.ChoiceField(choices=op_agexternos,widget=forms.Select(attrs={'class': 'form-control'}))
    fecha = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control','type': 'date'}))
    estructura = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}))  
    status = forms.ChoiceField(choices=op_status,widget=forms.Select(attrs={'class': 'form-control'}))
    observaciones = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))  

    class Meta:
    
        model = ccalidadpolen
        fields = ['codigo_lote','codigo_empleado','operario_name','supervisor_name','ubicacion_lote','apodo_variedad','calidad','consistencia','ag_externos','fecha','estructura','status','observaciones']
    
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        
        self.fields['calidad'].required = False
        self.fields['consistencia'].required = False
        self.fields['agentesexternos'].required = False
        self.fields['observaciones'].required = False
        self.fields['codigo_empleado'].required = False
        self.fields['operario_name'].required = False

class indexpolinizacionForm(forms.ModelForm):

    op_ubicacion = [('','-'),('SL','SL'),('CIP','CIP'),('Cecilio', 'Cecilio'),('Bella Vista', 'Bella Vista')]
    op_modulo = [('','-'),('Modulo 1','Modulo 1'),('Modulo 2','Modulo 2'),('Modulo 3', 'Modulo 3'),('Modulo 4','Modulo 4'),('Modulo 5','Modulo 5'),('Modulo 6', 'Modulo 6'),('Modulo 7','Modulo 7'),('Modulo 8','Modulo 8'),('Modulo 9', 'Modulo 9'),('Modulo 10','Modulo 10'),('Modulo 11','Modulo 11')]
    op_invernadero = [('','-'),('Invernadero 1','Invernadero 1'),('Invernadero 2','Invernadero 2'),('Invernadero 3', 'Invernadero 3'),('Invernadero 4','Invernadero 4'),('Invernadero 5','Invernadero 5'),('Invernadero 6', 'Invernadero 6'),('Invernadero 7','Invernadero 7'),('Invernadero 8','Invernadero 8'),('Invernadero 9', 'Invernadero 9'),('Invernadero 10','Invernadero 10'),('Invernadero 11','Invernadero 11')]
    op_malla = [('','-'),('Casa Malla','Casa Malla')]
    op_cultivo = [('','-'),('Chile','Chile'),('Tomtate','Tomate')]
    op_status = [('','-'),('Inicio','Inicio'),('Fin','Fin')]
    op_dias = [('','-'),('Lunes','Lunes'),('Martes','Martes'),('Miércoles','Miércoles'),('Jueves','Jueves'),('Viernes','Viernes'),('Sábado','Sábado'),('Domingo','Domingo')]
    op_colores= [('','-'),('Rojo','Rojo'),('Verde','Verde'),('Azul','Azul'),('Negro','Negro'),('Blanco','Blanco'),('Amarillo','Amarillo'),('Anaranjado','Anaranjado'),('Celeste','Celeste'),('Morado','Morado')]
    op_estructura = op_invernadero + op_modulo + op_malla
    op_index = [('','-'),('Index 1','Index 1'),('Index 2','Index 2'),('Index 3','Index 3'),('Index 4','Index 4'),('Index 5','Index 5'),('Ninguno','Ninguno')]
    codigo_lote = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control','readonly': 'readonly'}))
    codigo_empleado = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}))
    operario_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}))
    supervisor_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}))
    ubicacion_lote = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'})) 
    apodo_variedad = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}))
    tipo_cultivo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'})) 
    color_lana = forms.ChoiceField(choices=op_colores,widget=forms.Select(attrs={'class': 'form-control'}))
    diasemana = forms.ChoiceField(choices=op_dias,widget=forms.Select(attrs={'class': 'form-control'}))
    cantidad_camas=forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    cantidad_index=forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    cama1=forms.ChoiceField(choices=op_index,widget=forms.Select(attrs={'class': 'form-control'}))
    cama2=forms.ChoiceField(choices=op_index,widget=forms.Select(attrs={'class': 'form-control'}))
    cama3=forms.ChoiceField(choices=op_index,widget=forms.Select(attrs={'class': 'form-control'}))
    cama4=forms.ChoiceField(choices=op_index,widget=forms.Select(attrs={'class': 'form-control'}))
    cama5=forms.ChoiceField(choices=op_index,widget=forms.Select(attrs={'class': 'form-control'}))
    media=forms.ChoiceField(choices=op_index,widget=forms.Select(attrs={'class': 'form-control'}))
    total_index = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    fecha = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control','type': 'date'}))
    estructura = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}))
    status = forms.ChoiceField(choices=op_status,widget=forms.Select(attrs={'class': 'form-control'}))
    observaciones = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))  

    class Meta:
    
        model = indexpolinizacion
        fields = ['codigo_lote','codigo_empleado','operario_name','supervisor_name','ubicacion_lote','apodo_variedad','tipo_cultivo','color_lana','diasemana','cantidad_camas','cantidad_index','media','cama1','cama2','cama3','cama4','cama5','total_index','fecha','estructura','status','observaciones']
    
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        
        self.fields['cama1'].required = False
        self.fields['cama2'].required = False
        self.fields['cama3'].required = False
        self.fields['cama4'].required = False
        self.fields['cama5'].required = False
        self.fields['media'].required = False
        self.fields['total_index'].required = False
        self.fields['cantidad_index'].required = False
        self.fields['cantidad_camas'].required = False
        self.fields['observaciones'].required = False
        self.fields['codigo_empleado'].required = False
        self.fields['operario_name'].required = False

class conteofloresForm(forms.ModelForm):

    op_ubicacion = [('','-'),('SL','SL'),('CIP','CIP'),('Cecilio', 'Cecilio'),('Bella Vista', 'Bella Vista')]
    op_modulo = [('','-'),('Modulo 1','Modulo 1'),('Modulo 2','Modulo 2'),('Modulo 3', 'Modulo 3'),('Modulo 4','Modulo 4'),('Modulo 5','Modulo 5'),('Modulo 6', 'Modulo 6'),('Modulo 7','Modulo 7'),('Modulo 8','Modulo 8'),('Modulo 9', 'Modulo 9'),('Modulo 10','Modulo 10'),('Modulo 11','Modulo 11')]
    op_invernadero = [('','-'),('Invernadero 1','Invernadero 1'),('Invernadero 2','Invernadero 2'),('Invernadero 3', 'Invernadero 3'),('Invernadero 4','Invernadero 4'),('Invernadero 5','Invernadero 5'),('Invernadero 6', 'Invernadero 6'),('Invernadero 7','Invernadero 7'),('Invernadero 8','Invernadero 8'),('Invernadero 9', 'Invernadero 9'),('Invernadero 10','Invernadero 10'),('Invernadero 11','Invernadero 11')]
    op_malla = [('','-'),('Casa Malla','Casa Malla')]
    op_cultivo = [('','-'),('Chile','Chile'),('Tomate','Tomate')]
    op_status = [('','-'),('Inicio','Inicio'),('Fin','Fin')]
    op_dias = [('','-'),('Lunes','Lunes'),('Martes','Martes'),('Miércoles','Miércoles'),('Jueves','Jueves'),('Viernes','Viernes'),('Sábado','Sábado'),('Domingo','Domingo')]
    op_estructura = op_invernadero + op_modulo + op_malla
    op_sel = [('','-'),('Si','Si'),('No','No')]
    op_semana = [('','-'),(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),(6,'6')]

    codigo_lote = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control','readonly': 'readonly'}))
    operario_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}))
    codigo_empleado = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}))
    supervisor_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}))
    ubicacion_lote = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'})) 
    apodo_variedad = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}))
    tipo_cultivo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'})) 
    diasemana = forms.ChoiceField(choices=op_dias,widget=forms.Select(attrs={'class': 'form-control'}))
    nsemana = forms.ChoiceField(choices=op_semana,widget=forms.Select(attrs={'class': 'form-control'}))
    flores_abiertas=forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    flores_anteras=forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    flores_polinizadas=forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    flores_sinpistilo=forms.ChoiceField(choices=op_sel,widget=forms.Select(attrs={'class': 'form-control'}))
    flores_viejas=forms.ChoiceField(choices=op_sel,widget=forms.Select(attrs={'class': 'form-control'}))
    boton_pequeño=forms.ChoiceField(choices=op_sel,widget=forms.Select(attrs={'class': 'form-control'}))
    
    fecha = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control','type': 'date'}))
    estructura = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}))  
    status = forms.ChoiceField(choices=op_status,widget=forms.Select(attrs={'class': 'form-control'}))
    observaciones = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))  

    class Meta:
    
        model = floresabiertas
        fields = ['codigo_lote','codigo_empleado','operario_name','supervisor_name','ubicacion_lote','apodo_variedad','tipo_cultivo','diasemana','nsemana','flores_abiertas','flores_anteras','flores_polinizadas','flores_sinpistilo','flores_viejas','boton_pequeño','fecha','estructura','status','observaciones']
    
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        
        self.fields['flores_abiertas'].required = False
        self.fields['flores_anteras'].required = False
        self.fields['flores_polinizadas'].required = False
        self.fields['flores_viejas'].required = False
        self.fields['boton_pequeño'].required = False
        self.fields['observaciones'].required = False
        self.fields['codigo_empleado'].required = False
        self.fields['operario_name'].required = False

class controlcosechaForm(forms.ModelForm):

    op_ubicacion = [('','-'),('SL','SL'),('CIP','CIP'),('Cecilio', 'Cecilio'),('Bella Vista', 'Bella Vista')]
    op_modulo = [('','-'),('Modulo 1','Modulo 1'),('Modulo 2','Modulo 2'),('Modulo 3', 'Modulo 3'),('Modulo 4','Modulo 4'),('Modulo 5','Modulo 5'),('Modulo 6', 'Modulo 6'),('Modulo 7','Modulo 7'),('Modulo 8','Modulo 8'),('Modulo 9', 'Modulo 9'),('Modulo 10','Modulo 10'),('Modulo 11','Modulo 11')]
    op_invernadero = [('','-'),('Invernadero 1','Invernadero 1'),('Invernadero 2','Invernadero 2'),('Invernadero 3', 'Invernadero 3'),('Invernadero 4','Invernadero 4'),('Invernadero 5','Invernadero 5'),('Invernadero 6', 'Invernadero 6'),('Invernadero 7','Invernadero 7'),('Invernadero 8','Invernadero 8'),('Invernadero 9', 'Invernadero 9'),('Invernadero 10','Invernadero 10'),('Invernadero 11','Invernadero 11')]
    op_malla = [('','-'),('Casa Malla','Casa Malla')]
    op_cultivo = [('','-'),('Chile','Chile'),('Tomtate','Tomate')]
    op_status = [('','-'),('Inicio','Inicio'),('Fin','Fin')]
    op_estructura = op_invernadero + op_modulo + op_malla
    op_sel = [('','-'),('Adecuado','Adecuado'),('Mejorar','Mejorar')]
    op_punto = [('','-'),('Maduro','Maduro'),('Verde','Verde'),('Camagua','Camagua')]
    
    codigo_lote = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control','readonly': 'readonly'}))
    operario_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}))
    codigo_empleado = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}))
    supervisor_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}))
    ubicacion_lote = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'})) 
    apodo_variedad = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}))
    tipo_cultivo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'})) 
    cajas_revisadas=forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    frutos_autopol=forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    frutos_sinmarca=forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    frutos_sinlana=forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    frutos_fueratipo=forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    llenado_caja=forms.ChoiceField(choices=op_sel,widget=forms.Select(attrs={'class': 'form-control'}))
    punto_maduracion=forms.ChoiceField(choices=op_punto,widget=forms.Select(attrs={'class': 'form-control'}))
    
    fecha = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control','type': 'date'}))
    estructura = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}))  
    status = forms.ChoiceField(choices=op_status,widget=forms.Select(attrs={'class': 'form-control'}))
    observaciones = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))  

    class Meta:
    
        model = controlcosecha
        fields = ['codigo_lote','codigo_empleado','operario_name','supervisor_name','ubicacion_lote','apodo_variedad','tipo_cultivo','cajas_revisadas','frutos_autopol','frutos_sinmarca','frutos_sinlana','frutos_fueratipo','llenado_caja','punto_maduracion','fecha','estructura','status','observaciones']
    
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        
        self.fields['frutos_autopol'].required = False
        self.fields['frutos_sinmarca'].required = False
        self.fields['frutos_sinlana'].required = False
        self.fields['frutos_fueratipo'].required = False
        self.fields['llenado_caja'].required = False
        self.fields['punto_maduracion'].required = False
        self.fields['observaciones'].required = False
        self.fields['codigo_empleado'].required = False
        self.fields['operario_name'].required = False

class operariosForm(forms.ModelForm):

    op_status = [('','-'),('Activo','Activo'),('Inactivo','Inactivo'),('Anulado','Anulado')]
    op_supervisores = [('','-'),('Astrid García','Astrid García'),('Adi Salazar','Adi Salazar'),('Fatima Franco','Fatima Franco'),('Marlon Aguilar','Marlon Aguilar')]
    
    codigo_empleado= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))  
    codigoevo = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    nombre_operario= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))  
    supervisor = forms.ChoiceField(choices=op_supervisores,widget=forms.Select(attrs={'class': 'form-control'}))  
    status = forms.ChoiceField(choices=op_status,widget=forms.Select(attrs={'class': 'form-control'}))
    codigo_lote = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control','readonly': 'readonly'}))
    
    class Meta:
    
        model = operariosApp
        fields = ['codigo_empleado','codigoevo','nombre_operario', 'supervisor','status','codigo_lote']
