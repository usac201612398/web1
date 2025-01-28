from django import forms
from .models import scoremanejo, scorecosecha, scorepersonal

class scoremanejoForm(forms.ModelForm):

    fecha = forms.DateField(widget=forms.DateInput(attrs={'class': 'my-input'}))
    nombre = forms.CharField(widget=forms.Select(attrs={'class': 'my-input'}))  # Campo de correo electrónico
    estructura = forms.CharField(widget=forms.Select(attrs={'class': 'my-input'}))  # Campo de texto
    bajado = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'}))  # Campo numérico
    distri_ejes = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'}))  # Campo numérico
    deshije = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'}))  # Campo numérico
    guiado = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'}))  # Campo numérico
    hil_ban_rec_ejes = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'}))  # Campo numérico
    orden_limpieza = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'}))  # Campo numérico

    class Meta:
    
        model = scoremanejo
        fields = ['fecha','nombrep','estructura','bajado',  'distri_ejes', 'deshije', 'gruiado','hil_ban_rec_ejes','orden_limpieza']

class scorecosechaForm(forms.ModelForm):

    fecha = forms.DateField(widget=forms.DateInput(attrs={'class': 'my-input'}))
    nombre = forms.CharField(widget=forms.Select(attrs={'class': 'my-input'}))  # Campo de nombre
    estructura = forms.CharField(widget=forms.Select(attrs={'class': 'my-input'}))  # Campo de texto
    grado_mad = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'}))  # Campo numérico
    deshoje= forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'}))  # Campo numérico
    descoronado = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'}))  # Campo numérico
    orden_limpieza = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'}))  # Campo numérico

    class Meta:
    
        model = scoremanejo
        fields = ['fecha','nombrep','estructura','grado_mad',  'deshoje', 'descoronado', 'orden_limpieza']

class scorepersonalForm(forms.ModelForm):

    finca = forms.CharField(widget=forms.Select(attrs={'class': 'my-input'}))  # Campo de texto
    encargado = forms.CharField(widget=forms.Select(attrs={'class': 'my-input'}))  # Campo de texto
    cuadrilla = forms.CharField(widget=forms.Select(attrs={'class': 'my-input'}))  # Campo de texto
    codigo =  forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'my-input'}))  # Campo numérico   
    nombre = forms.CharField(widget=forms.Select(attrs={'class': 'my-input'}))  # Campo de nombre
    estructura = forms.CharField(widget=forms.Select(attrs={'class': 'my-input'}))  # Campo de texto
    area = forms.CharField(widget=forms.Select(attrs={'class': 'my-input'}))  # Campo de texto

    class Meta:
    
        model = scorepersonal
        fields = ['fecha','encargado','cuadrilla','codigop','nombrep','estructura','area']