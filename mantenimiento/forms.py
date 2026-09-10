from django import forms
from .models import *


class ubicacionesForm(forms.ModelForm):

    ESTADOS = [
        ('Abierta', 'Abierta'),
        ('Cerrada', 'Cerrada'),
        ('Anulada', 'Anulada'),
    ]

    nombre = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej. Bodega principal'
        })
    )

    status = forms.ChoiceField(
        choices=ESTADOS,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    class Meta:
        model = Ubicacion
        fields = ['nombre', 'status']


# ==========================================================
# MAQUINA
# ==========================================================

class MaquinaForm(forms.ModelForm):

    ESTADOS = [
        ('Activa', 'Activa'),
        ('Inactiva', 'Inactiva'),
        ('Averiada', 'Averiada'),
        ('Anulada', 'Anulada'),
    ]

    nombre = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej. Excavadora CAT 320'
        })
    )

    tipo = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej. Excavadora'
        })
    )

    status = forms.ChoiceField(
        choices=ESTADOS,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    class Meta:

        model = Maquina

        fields = [
            'nombre',
            'tipo',
            'status',
        ]

# ==========================================================
# Centro de costo
# ==========================================================

class centrodecostoForm(forms.ModelForm):

    ESTADOS = [
        ('', ''),
        ('Abierto', 'Abierto'),
        ('Cerrado', 'Cerrado'),
        ('Anulado', 'Anulado'),
    ]

    centrodecosto = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el código del centro de costo'
            }
        )
    )

    nombre = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre'
            }
        )
    )

    status = forms.ChoiceField(
        choices=ESTADOS,
        initial="Abierto",
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        )
    )

    class Meta:

        model = centrodecosto

        fields = [
            'centrodecosto',
            'nombre',
            'status'
        ]
        