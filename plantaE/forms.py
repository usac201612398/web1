from django import forms
from .models import salidasFruta, usuariosAppFruta, datosProduccion, detallesProduccion
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Div
class salidasFrutaForm(forms.ModelForm):
    op_viajes = [('Viaje 1','Viaje 1'),('Viaje 2','Viaje 2'),('Viaje 3', 'Viaje 3'),('Viaje 4','Viaje 4'),('Viaje 5','Viaje 5'),('Viaje 6','Viaje 6')]
    
    correo = forms.ChoiceField(widget=forms.Select(attrs={'class': 'my-input'}))  # Campo de correo electrónico
    encargado = forms.ChoiceField(widget=forms.Select(attrs={'class': 'my-input'}))  # Campo de texto
    finca = forms.ChoiceField(widget=forms.Select(attrs={'class': 'my-input'}))  # Campo de texto
    viaje = forms.ChoiceField(choices=op_viajes,widget=forms.Select(attrs={'class': 'my-input'}))  # Campo de texto
    cajas = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'}))  # Campo numérico
    orden = forms.ChoiceField(widget=forms.Select(attrs={'class': 'my-input'}))  # Campo de texto
    cultivo = forms.ChoiceField(widget=forms.Select(attrs={'class': 'my-input'}))  # Campo de texto
    variedad = forms.ChoiceField(widget=forms.Select(attrs={'class': 'my-input'}))  # Campo de texto

    class Meta:
    
        model = salidasFruta
        fields = ['correo','viaje','encargado',  'finca', 'cajas',  'orden', 'cultivo', 'variedad']
        
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
        