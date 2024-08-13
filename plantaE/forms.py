from django import forms
from .models import salidasFruta, usuariosAppFruta, datosProduccion, detallesProduccion
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Div
class salidasFrutaForm(forms.ModelForm):
    
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
                    )
                )
            )