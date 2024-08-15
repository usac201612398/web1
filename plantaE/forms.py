from django import forms
from .models import salidasFruta, Recepciones, Ccalidad
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Div

class salidasFrutaForm(forms.ModelForm):
    op_viajes = [('Viaje 1','Viaje 1'),('Viaje 2','Viaje 2'),('Viaje 3', 'Viaje 3'),('Viaje 4','Viaje 4'),('Viaje 5','Viaje 5'),('Viaje 6','Viaje 6')]
    
    correo = forms.CharField(widget=forms.Select(attrs={'class': 'my-input'}))  # Campo de correo electrónico
    encargado = forms.CharField(widget=forms.Select(attrs={'class': 'my-input'}))  # Campo de texto
    finca = forms.CharField(widget=forms.Select(attrs={'class': 'my-input'}))  # Campo de texto
    viaje = forms.ChoiceField(choices=op_viajes,widget=forms.Select(attrs={'class': 'my-input'}))  # Campo de texto
    cajas = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'}))  # Campo numérico
    orden = forms.CharField(widget=forms.Select(attrs={'class': 'my-input'}))  # Campo de texto
    cultivo = forms.CharField(widget=forms.Select(attrs={'class': 'my-input'}))  # Campo de texto
    variedad = forms.CharField(widget=forms.Select(attrs={'class': 'my-input'}))  # Campo de texto
    estructura = forms.CharField(widget=forms.Select(attrs={'class': 'my-input'}))  # Campo de texto
    
    class Meta:
    
        model = salidasFruta
        fields = ['correo','viaje','encargado',  'finca', 'cajas',  'orden', 'cultivo','estructura', 'variedad']
        
        def __init__(self, *args, **kwargs):

            super().__init__(*args, **kwargs)
            
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.add_input(Submit('submit','Guardar'))

            self.helper.layout = Layout(
                Fieldset(
                    'Información de Salida',
                    Div(
                        Div('viaje', css_class='form-group col-md-6'),
                        Div('finca', css_class='form-group col-md-6'),
                        css_class='row'
                    ),
                    Div(
                        Div('encargado', css_class='form-group col-md-6'),
                        Div('correo', css_class='form-group col-md-6'),
                        css_class='row'
                    ),
                    Div(
                        Div('orden', css_class='form-group col-md-6'),
                        Div('cultivo', css_class='form-group col-md-6'),
                        css_class='row'
                    ),
                    Div(
                        Div('variedad', css_class='form-group col-md-6'),
                        Div('cajas', css_class='form-group col-md-6'),
                        css_class='row'
                    ),
                    css_class='container' 
                )
            )

class recepcionesForm(forms.ModelForm):
    op_status = [('Pendiente',''),('En proceso','En proceso')]

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
    op_status2 = [('Pendiente',''),('','Inspeccionado')]

    recepcion = forms.CharField(widget=forms.Select(attrs={'class': 'my-input'}))
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type':'date','class': 'my-input'}))
    porcentaje= forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'my-input'}))  # Campo numérico
    status2 = forms.ChoiceField(choices=op_status2,widget=forms.Select(attrs={'class': 'my-input'}))
    llave = forms.CharField(widget=forms.Select(attrs={'class': 'my-input'}))
    causarechazo = forms.CharField(widget=forms.Select(attrs={'class': 'my-input'}))
    observaciones = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input'}))

    class Meta:
    
        model = Ccalidad
        fields = ['recepcion','fecha','porcentaje', 'status2', 'llave', 'causarechazo','observaciones']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['observaciones'].required = False                