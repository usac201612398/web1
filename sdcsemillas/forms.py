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
    ubicacion = forms.ChoiceField(choices=op_ubicacion, widget=forms.Select(attrs={'class': 'form-control'}))
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
    as_per_SDCMale = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    as_per_SDCFemale = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = lotes
        fields = [
            'lote_code', 'variedad_code', 'apodo_variedad', 'cultivo',
            'ubicacion', 'estructura', 'plantas_padre', 'plantas_madre',
            'harvest_code', 'status', 'siembra_madre', 'metodo_prod',
            'target', 'surface', 'observaciones','shipment_hub','as_per_SDCMale','as_per_SDCFemale'
        ]

    def __init__(self, *args, **kwargs):
        super(lotesForm, self).__init__(*args, **kwargs)
        variedades_qs = variedades.objects.all()
        self.fields['variedad_code'].choices = [('', '-')] + [(v.variedad_code, v.variedad_code) for v in variedades_qs]
        self.fields['apodo_variedad'].choices = [('', '-')] + [(v.apodo_variedad, v.apodo_variedad) for v in variedades_qs]

class variedadesForm(forms.ModelForm):

    op_cultivo = [('','-'),('Chile','Chile'),('Tomate','Tomate')]
    
    #op_status = [('','-'),('En proceso','En proceso'),('Finalizado','Finalizado'),('Anulado','Anulado')]

    variedad_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input'}))  
    apodo_variedad = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input'}))
    cultivo = forms.ChoiceField(choices=op_cultivo,widget=forms.Select(attrs={'class': 'my-input'})) 
    cod_padre = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input'}))  
    cod_madre = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input'})) 
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

    operario_name = forms.ChoiceField(widget=forms.TextInput(attrs={'class': 'my-input'}))
    supervisor_name = forms.ChoiceField(widget=forms.TextInput(attrs={'class': 'my-input'}))
    ubicacion_lote = forms.ChoiceField(choices=op_ubicacion,widget=forms.TextInput(attrs={'class': 'my-input'})) 
    apodo_variedad = forms.ChoiceField(widget=forms.TextInput(attrs={'class': 'my-input'}))
    tipo_cultivo = forms.ChoiceField(choices=op_cultivo,widget=forms.Select(attrs={'class': 'my-input'})) 
    codigo_planta = forms.ChoiceField(widget=forms.TextInput(attrs={'class': 'my-input'}))  
    codigo_madre = forms.ChoiceField(widget=forms.TextInput(attrs={'class': 'my-input'})) 
    plantas_activas = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'})) 
    plantas_faltantes = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'})) 
    fecha = forms.DateField(widget=forms.DateInput(attrs={'class': 'my-input'}))
    camas_completas = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'})) 
    camas_incompletas = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'})) 
    cocosxcamaincompletas = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'})) 
    estructura = forms.ChoiceField(choices=op_estructura, widget=forms.TextInput(attrs={'class': 'my-input'}))  
    status = forms.ChoiceField(choices=op_status,widget=forms.Select(attrs={'class': 'my-input'}))
    evento = forms.ChoiceField(choices=op_eventos,widget=forms.Select(attrs={'class': 'my-input'}))
    observaciones = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input'}))  

    class Meta:
    
        model = conteoplantas
        fields = ['operario_name','supervisor_name','ubicacion_lote','apodo_variedad','tipo_cultivo','codigo_planta','codigo_madre','plantas_activas','plantas_faltantes','fecha','camas_completas','camas_incompletas','cocosxcamaincompletas', 'estructura', 'status','evento','observaciones']

class conteosemillasForm(forms.ModelForm):

    op_ubicacion = [('','-'),('SL','SL'),('CIP','CIP'),('Cecilio', 'Cecilio'),('Bella Vista', 'Bella Vista')]
    op_modulo = [('','-'),('Modulo 1','Modulo 1'),('Modulo 2','Modulo 2'),('Modulo 3', 'Modulo 3'),('Modulo 4','Modulo 4'),('Modulo 5','Modulo 5'),('Modulo 6', 'Modulo 6'),('Modulo 7','Modulo 7'),('Modulo 8','Modulo 8'),('Modulo 9', 'Modulo 9'),('Modulo 10','Modulo 10'),('Modulo 11','Modulo 11')]
    op_invernadero = [('','-'),('Invernadero 1','Invernadero 1'),('Invernadero 2','Invernadero 2'),('Invernadero 3', 'Invernadero 3'),('Invernadero 4','Invernadero 4'),('Invernadero 5','Invernadero 5'),('Invernadero 6', 'Invernadero 6'),('Invernadero 7','Invernadero 7'),('Invernadero 8','Invernadero 8'),('Invernadero 9', 'Invernadero 9'),('Invernadero 10','Invernadero 10'),('Invernadero 11','Invernadero 11')]
    op_malla = [('','-'),('Casa Malla','Casa Malla')]
    op_cultivo = [('','-'),('Chile','Chile'),('Tomtate','Tomate')]
    op_status = [('','-'),('En proceso','En proceso'),('Finalizado','Finalizado')]
    op_estructura = op_invernadero + op_modulo + op_malla
    
    op_clasificacion = [('','-'),('Fruto maduro','Fruto maduro'),('Fruto verde','Fruto verde')]

    operario_name = forms.ChoiceField(widget=forms.TextInput(attrs={'class': 'my-input'}))
    supervisor_name = forms.ChoiceField(widget=forms.TextInput(attrs={'class': 'my-input'}))
    ubicacion_lote = forms.ChoiceField(choices=op_ubicacion,widget=forms.TextInput(attrs={'class': 'my-input'})) 
    apodo_variedad = forms.ChoiceField(widget=forms.TextInput(attrs={'class': 'my-input'}))
    tipo_cultivo = forms.ChoiceField(choices=op_cultivo,widget=forms.Select(attrs={'class': 'my-input'})) 
    cantidad_frutos = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'})) 
    semillasxfruto= forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'})) 
    prom_semillasxfruto = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'})) 
    nsemana = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'})) 
    fecha = forms.DateField(widget=forms.DateInput(attrs={'class': 'my-input'}))
    estructura = forms.ChoiceField(choices=op_estructura, widget=forms.TextInput(attrs={'class': 'my-input'}))  
    status = forms.ChoiceField(choices=op_status,widget=forms.Select(attrs={'class': 'my-input'}))
    clasificacion = forms.ChoiceField(choices=op_clasificacion,widget=forms.Select(attrs={'class': 'my-input'}))
    observaciones = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input'}))  

    class Meta:
    
        model = conteosemillas
        fields = ['operario_name','supervisor_name','ubicacion_lote','apodo_variedad','tipo_cultivo','cantidad_frutos','semillasxfruto','prom_semillasxfruto','nsemana','fecha','estructura','status','clasificacion','observaciones']

class conteofrutosForm(forms.ModelForm):

    op_ubicacion = [('','-'),('SL','SL'),('CIP','CIP'),('Cecilio', 'Cecilio'),('Bella Vista', 'Bella Vista')]
    op_modulo = [('','-'),('Modulo 1','Modulo 1'),('Modulo 2','Modulo 2'),('Modulo 3', 'Modulo 3'),('Modulo 4','Modulo 4'),('Modulo 5','Modulo 5'),('Modulo 6', 'Modulo 6'),('Modulo 7','Modulo 7'),('Modulo 8','Modulo 8'),('Modulo 9', 'Modulo 9'),('Modulo 10','Modulo 10'),('Modulo 11','Modulo 11')]
    op_invernadero = [('','-'),('Invernadero 1','Invernadero 1'),('Invernadero 2','Invernadero 2'),('Invernadero 3', 'Invernadero 3'),('Invernadero 4','Invernadero 4'),('Invernadero 5','Invernadero 5'),('Invernadero 6', 'Invernadero 6'),('Invernadero 7','Invernadero 7'),('Invernadero 8','Invernadero 8'),('Invernadero 9', 'Invernadero 9'),('Invernadero 10','Invernadero 10'),('Invernadero 11','Invernadero 11')]
    op_malla = [('','-'),('Casa Malla','Casa Malla')]
    op_cultivo = [('','-'),('Chile','Chile'),('Tomtate','Tomate')]
    op_status = [('','-'),('En proceso','En proceso'),('Finalizado','Finalizado')]
    op_estructura = op_invernadero + op_modulo + op_malla
    
    op_clasificacion = [('','-'),('Autopolinizado','Autopolinizado'),('Postpolinizado','Postpolinizado'),('General','General')]

    operario_name = forms.ChoiceField(widget=forms.TextInput(attrs={'class': 'my-input'}))
    supervisor_name = forms.ChoiceField(widget=forms.TextInput(attrs={'class': 'my-input'}))
    ubicacion_lote = forms.ChoiceField(choices=op_ubicacion,widget=forms.TextInput(attrs={'class': 'my-input'})) 
    apodo_variedad = forms.ChoiceField(widget=forms.TextInput(attrs={'class': 'my-input'}))
    tipo_cultivo = forms.ChoiceField(choices=op_cultivo,widget=forms.Select(attrs={'class': 'my-input'})) 
    
    prom_autopolinizados = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'my-input'}))
    prom_foresabiertas= forms.FloatField(widget=forms.NumberInput(attrs={'class': 'my-input'})) 
    prom_polinizados = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'my-input'})) 
    prom_cama = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'my-input'})) 
    prom_area = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'my-input'})) 
    prom_general = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'my-input'})) 
    nsemana = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'})) 
    fecha = forms.DateField(widget=forms.DateInput(attrs={'class': 'my-input'}))
    estructura = forms.ChoiceField(choices=op_estructura, widget=forms.TextInput(attrs={'class': 'my-input'}))  
    status = forms.ChoiceField(choices=op_status,widget=forms.Select(attrs={'class': 'my-input'}))
    evento = forms.ChoiceField(choices=op_clasificacion,widget=forms.Select(attrs={'class': 'my-input'}))
    observaciones = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input'}))  

    class Meta:
    
        model = conteofrutos
        fields = ['operario_name','supervisor_name','ubicacion_lote','apodo_variedad','tipo_cultivo','prom_autopolinizados','prom_floresabiertas','prom_polinizados','prom_cama','prom_area','prom_general','nsemana','fecha','estructura','status','evento','observaciones']

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
    codigo_lote = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input','readonly': 'readonly'}))
    supervisor_name = forms.ChoiceField(widget=forms.TextInput(attrs={'class': 'my-input','readonly': 'readonly'}))
    ubicacion_lote = forms.ChoiceField(choices=op_ubicacion,widget=forms.TextInput(attrs={'class': 'my-input','readonly': 'readonly'})) 
    apodo_variedad = forms.ChoiceField(widget=forms.TextInput(attrs={'class': 'my-input','readonly': 'readonly'}))
    tipo_cultivo = forms.ChoiceField(choices=op_cultivo,widget=forms.Select(attrs={'class': 'my-input','readonly': 'readonly'})) 
    codigo_madre = forms.ChoiceField(widget=forms.TextInput(attrs={'class': 'my-input'})) 
    codigo_padre = forms.ChoiceField(widget=forms.TextInput(attrs={'class': 'my-input'})) 
    fecha = forms.DateField(widget=forms.DateInput(attrs={'class': 'my-input','type': 'date'}))
    estructura = forms.ChoiceField(choices=op_estructura, widget=forms.TextInput(attrs={'class': 'my-input','readonly': 'readonly'}))  
    status = forms.ChoiceField(choices=op_status,widget=forms.Select(attrs={'class': 'my-input'}))
    evento = forms.ChoiceField(choices=op_clasificacion,widget=forms.Select(attrs={'class': 'my-input'}))
    observaciones = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input'}))  

    class Meta:
    
        model = etapasdelote
        fields = ['codigo_lote','supervisor_name','ubicacion_lote','apodo_variedad','tipo_cultivo','codigo_madre','codigo_padre','fecha','estructura','status','evento','observaciones']

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
    
   
    operario_name = forms.ChoiceField(widget=forms.TextInput(attrs={'class': 'my-input'}))
    supervisor_name = forms.ChoiceField(widget=forms.TextInput(attrs={'class': 'my-input'}))
    ubicacion_lote = forms.ChoiceField(choices=op_ubicacion,widget=forms.TextInput(attrs={'class': 'my-input'})) 
    apodo_variedad = forms.ChoiceField(widget=forms.TextInput(attrs={'class': 'my-input'}))
    tipo_cultivo = forms.ChoiceField(choices=op_cultivo,widget=forms.Select(attrs={'class': 'my-input'})) 
    calidad = forms.ChoiceField(choices=op_calidad,widget=forms.Select(attrs={'class': 'my-input'}))
    cosistencia = forms.ChoiceField(choices=op_consistencia,widget=forms.Select(attrs={'class': 'my-input'}))
    ag_externos=forms.ChoiceField(choices=op_agexternos,widget=forms.Select(attrs={'class': 'my-input'}))
    fecha = forms.DateField(widget=forms.DateInput(attrs={'class': 'my-input'}))
    estructura = forms.ChoiceField(choices=op_estructura, widget=forms.TextInput(attrs={'class': 'my-input'}))  
    status = forms.ChoiceField(choices=op_status,widget=forms.Select(attrs={'class': 'my-input'}))
    observaciones = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input'}))  

    class Meta:
    
        model = ccalidadpolen
        fields = ['operario_name','supervisor_name','ubicacion_lote','apodo_variedad','calidad','consistencia','ag_externos','fecha','estructura','status','observaciones']


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
    
   
    operario_name = forms.ChoiceField(widget=forms.TextInput(attrs={'class': 'my-input'}))
    supervisor_name = forms.ChoiceField(widget=forms.TextInput(attrs={'class': 'my-input'}))
    ubicacion_lote = forms.ChoiceField(choices=op_ubicacion,widget=forms.TextInput(attrs={'class': 'my-input'})) 
    apodo_variedad = forms.ChoiceField(widget=forms.TextInput(attrs={'class': 'my-input'}))
    tipo_cultivo = forms.ChoiceField(choices=op_cultivo,widget=forms.Select(attrs={'class': 'my-input'})) 
    color_lana = forms.ChoiceField(choices=op_colores,widget=forms.Select(attrs={'class': 'my-input'}))
    diasemana = forms.ChoiceField(choices=op_dias,widget=forms.Select(attrs={'class': 'my-input'}))
    cantidad_camas=forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'}))
    cantidad_index=forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'}))
    promedio=forms.FloatField(widget=forms.NumberInput(attrs={'class': 'my-input'}))
    fecha = forms.DateField(widget=forms.DateInput(attrs={'class': 'my-input'}))
    estructura = forms.ChoiceField(choices=op_estructura, widget=forms.TextInput(attrs={'class': 'my-input'}))  
    status = forms.ChoiceField(choices=op_status,widget=forms.Select(attrs={'class': 'my-input'}))
    observaciones = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input'}))  

    class Meta:
    
        model = indexpolinizacion
        fields = ['operario_name','supervisor_name','ubicacion_lote','apodo_variedad','tipo_cultivo','color_lana','diasemana','cantidad_camas','cantidad_index','promedio','fecha','estructura','status','observaciones']

class conteofloresForm(forms.ModelForm):

    op_ubicacion = [('','-'),('SL','SL'),('CIP','CIP'),('Cecilio', 'Cecilio'),('Bella Vista', 'Bella Vista')]
    op_modulo = [('','-'),('Modulo 1','Modulo 1'),('Modulo 2','Modulo 2'),('Modulo 3', 'Modulo 3'),('Modulo 4','Modulo 4'),('Modulo 5','Modulo 5'),('Modulo 6', 'Modulo 6'),('Modulo 7','Modulo 7'),('Modulo 8','Modulo 8'),('Modulo 9', 'Modulo 9'),('Modulo 10','Modulo 10'),('Modulo 11','Modulo 11')]
    op_invernadero = [('','-'),('Invernadero 1','Invernadero 1'),('Invernadero 2','Invernadero 2'),('Invernadero 3', 'Invernadero 3'),('Invernadero 4','Invernadero 4'),('Invernadero 5','Invernadero 5'),('Invernadero 6', 'Invernadero 6'),('Invernadero 7','Invernadero 7'),('Invernadero 8','Invernadero 8'),('Invernadero 9', 'Invernadero 9'),('Invernadero 10','Invernadero 10'),('Invernadero 11','Invernadero 11')]
    op_malla = [('','-'),('Casa Malla','Casa Malla')]
    op_cultivo = [('','-'),('Chile','Chile'),('Tomtate','Tomate')]
    op_status = [('','-'),('Inicio','Inicio'),('Fin','Fin')]
    op_dias = [('','-'),('Lunes','Lunes'),('Martes','Martes'),('Miércoles','Miércoles'),('Jueves','Jueves'),('Viernes','Viernes'),('Sábado','Sábado'),('Domingo','Domingo')]
    op_estructura = op_invernadero + op_modulo + op_malla
    op_sel = [('','-'),('Si','Si'),('No','No')]

    operario_name = forms.ChoiceField(widget=forms.TextInput(attrs={'class': 'my-input'}))
    supervisor_name = forms.ChoiceField(widget=forms.TextInput(attrs={'class': 'my-input'}))
    ubicacion_lote = forms.ChoiceField(choices=op_ubicacion,widget=forms.TextInput(attrs={'class': 'my-input'})) 
    apodo_variedad = forms.ChoiceField(widget=forms.TextInput(attrs={'class': 'my-input'}))
    tipo_cultivo = forms.ChoiceField(choices=op_cultivo,widget=forms.Select(attrs={'class': 'my-input'})) 
    diasemana = forms.ChoiceField(choices=op_dias,widget=forms.Select(attrs={'class': 'my-input'}))
    nsemana = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'}))
    
    flores_abiertas=forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'}))
    flores_antenas=forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'}))
    flores_polinizadas=forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'}))
    flores_enmasculadas=forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'}))
    flores_sinpistilo=forms.ChoiceField(choices=op_sel,widget=forms.Select(attrs={'class': 'my-input'}))
    flores_viejas=forms.ChoiceField(choices=op_sel,widget=forms.Select(attrs={'class': 'my-input'}))
    lastimado=forms.ChoiceField(choices=op_sel,widget=forms.Select(attrs={'class': 'my-input'}))
    boton_pequeño=forms.ChoiceField(choices=op_sel,widget=forms.Select(attrs={'class': 'my-input'}))
    
    fecha = forms.DateField(widget=forms.DateInput(attrs={'class': 'my-input'}))
    estructura = forms.ChoiceField(choices=op_estructura, widget=forms.TextInput(attrs={'class': 'my-input'}))  
    status = forms.ChoiceField(choices=op_status,widget=forms.Select(attrs={'class': 'my-input'}))
    observaciones = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input'}))  

    class Meta:
    
        model = floresabiertas
        fields = ['operario_name','supervisor_name','ubicacion_lote','apodo_variedad','tipo_cultivo','diasemana','nsemana','flores_abiertas','flores_antenas','flores_polinizadas','flores_enmasculadas','flores_sinpistilo','flores_viejas','lastimado','boton_pequeño','fecha','estructura','status','observaciones']

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
    

    operario_name = forms.ChoiceField(widget=forms.TextInput(attrs={'class': 'my-input'}))
    supervisor_name = forms.ChoiceField(widget=forms.TextInput(attrs={'class': 'my-input'}))
    ubicacion_lote = forms.ChoiceField(choices=op_ubicacion,widget=forms.TextInput(attrs={'class': 'my-input'})) 
    apodo_variedad = forms.ChoiceField(widget=forms.TextInput(attrs={'class': 'my-input'}))
    tipo_cultivo = forms.ChoiceField(choices=op_cultivo,widget=forms.Select(attrs={'class': 'my-input'})) 
   
    cajas_revisadas=forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'}))
    frutos_autopol=forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'}))
    frutos_sinmarca=forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'}))
    frutos_sinlana=forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'}))
    frutos_fueratipo=forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'}))
    llenado_caja=forms.ChoiceField(choices=op_sel,widget=forms.Select(attrs={'class': 'my-input'}))
    punto_maduracion=forms.ChoiceField(choices=op_punto,widget=forms.Select(attrs={'class': 'my-input'}))
    
    fecha = forms.DateField(widget=forms.DateInput(attrs={'class': 'my-input'}))
    estructura = forms.ChoiceField(choices=op_estructura, widget=forms.TextInput(attrs={'class': 'my-input'}))  
    status = forms.ChoiceField(choices=op_status,widget=forms.Select(attrs={'class': 'my-input'}))
    observaciones = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input'}))  

    class Meta:
    
        model = controlcosecha
        fields = ['operario_name','supervisor_name','ubicacion_lote','apodo_variedad','tipo_cultivo','cajas_revisadas','frutos_autopol','frutos_sinmarca','frutos_sinlana','frutos_fueratipo','llenado_caja','punto_maduracion','fecha','estructura','status','observaciones']

class operariosForm(forms.ModelForm):

    op_status = [('','-'),('Activo','Activo'),('Inactivo','Inactivo'),('Anulado','Anulado')]
    op_supervisores = [('','-'),('A','A'),('B','B'),('C','C')]
    
    codigo_empleado= forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input'}))  
    codigoEvo = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'}))
    nombreo_perario = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input'})) 
    supervisor = forms.ChoiceField(choices=op_supervisores,widget=forms.TextInput(attrs={'class': 'my-input'}))  
    status = forms.ChoiceField(choices=op_status,widget=forms.Select(attrs={'class': 'my-input'}))
    codigo_lote = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input','readonly': 'readonly'}))
    
    class Meta:
    
        model = operariosApp
        fields = ['codigo_empleado','codigoEvo','nombre_operario', 'supervisor','status','codigo_lote']
