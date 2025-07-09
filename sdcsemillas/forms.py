from django import forms
from .models import *

class lotesForm(forms.ModelForm):

    op_ubicacion = [('','-'),('SL','SL'),('CIP','CIP'),('Cecilio', 'Cecilio')]
    op_modulo = [('','-'),('Modulo 1','Modulo 1'),('Modulo 2','Modulo 2'),('Modulo 3', 'Modulo 3'),('Modulo 4','Modulo 4'),('Modulo 5','Modulo 5'),('Modulo 6', 'Modulo 6'),('Modulo 7','Modulo 7'),('Modulo 8','Modulo 8'),('Modulo 9', 'Modulo 9'),('Modulo 10','Modulo 10'),('Modulo 11','Modulo 11')]
    op_invernadero = [('','-'),('Invernadero 1','Invernadero 1'),('Invernadero 2','Invernadero 2'),('Invernadero 3', 'Invernadero 3'),('Invernadero 4','Invernadero 4'),('Invernadero 5','Invernadero 5'),('Invernadero 6', 'Invernadero 6'),('Invernadero 7','Invernadero 7'),('Invernadero 8','Invernadero 8'),('Invernadero 9', 'Invernadero 9'),('Invernadero 10','Invernadero 10'),('Invernadero 11','Invernadero 11')]
    op_malla = [('Casa Malla','Casa Malla')]
    op_cultivo = [('Chile','Tomate')]
    op_estructura = op_invernadero + op_modulo + op_malla
    
    op_metodos = [('Greenhouse','Greenhouse'),('Macrotunel','Macrotunel'),('Nethouse','Nethouse')]

    fecha_pl = forms.DateField(widget=forms.DateInput(attrs={'class': 'my-input'}))
    lote_code = forms.CharField(widget=forms.Select(attrs={'class': 'my-input'}))  # Campo de correo electrónico
    variedad_code = forms.CharField(widget=forms.Select(attrs={'class': 'my-input'}))  # Campo de correo electrónico
    #variedad_name = forms.CharField(widget=forms.Select(attrs={'class': 'my-input'}))  # Campo de texto
    apodo_variedad = forms.CharField(widget=forms.Select(attrs={'class': 'my-input'}))  # Campo de texto
    cultivo = forms.ChoiceField(widget=forms.Select(attrs={'class': 'my-input'}))  # Campo de texto
    ubicacion = forms.CharField(choices=op_ubicacion,widget=forms.Select(attrs={'class': 'my-input'}))  # Campo de texto
    estructura = forms.CharField(choices=op_estructura, widget=forms.NumberInput(attrs={'class': 'my-input'}))  # Campo numérico
    plantas_padre = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'}))  # Campo de texto
    plantas_madre = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'})) 
    harvest_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'my-input'})) 
    status = forms.ChoiceField(widget=forms.Select(attrs={'class': 'my-input'}))
    siembra_madre = forms.DateField(widget=forms.DateInput(attrs={'class': 'my-input'}))
    metodo_prod = forms.ChoiceField(choices=op_metodos,widget=forms.Select(attrs={'class': 'my-input'}))
    target = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'})) 
    surface = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'my-input'}))


    class Meta:
    
        model = lotes
        fields = ['fecha_pl','lote_code','variedad_code','apodo_variedad','cultivo', 'ubicacion', 'estructura', 'plantas_padre','plantas_madre','harvest_code','status','siembra_madre','metodo_prod','target','surface']