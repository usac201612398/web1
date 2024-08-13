from django import forms
from .models import salidasFruta, usuariosAppFruta, datosProduccion, detallesProduccion
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset
class salidasFrutaForm(forms.ModelForm):
    
    class Meta:
    
        model = salidasFruta
        fields = ['viaje', 'cajas', 'finca', 'encargado', 'correo', 'orden', 'cultivo', 'variedad']
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.add_input(Submit('submit','Guardar'))
            self.helper.layout = Layout(
                Fieldset(
                    'viaje',
                    'finca',
                    'encargado',
                    'correo',
                    'orden',
                    'cultivo',
                    'variedad'
                    Div('cajas', css_class='col-md-6')
                )
            )