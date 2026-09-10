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

# ==========================================================
# Personal
# ==========================================================

class personalForm(forms.ModelForm):

    ROLES = [
        ('', ''),
        ('Cliente', 'Cliente'),
        ('Responsable', 'Responsable'),
        ('Gestor', 'Gestor'),
        ('Admin', 'Administrador'),
    ]

    ESTADOS = [
        ('', ''),
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
        ('Anulado', 'Anulado'),
    ]

    correo = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }
        )
    )

    nombre = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo'
            }
        )
    )

    codigoevo = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese su código de evolution'
            }
        )
    )

    rol = forms.ChoiceField(
        required=False,
        choices=ROLES,
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        )
    )

    status = forms.ChoiceField(
        choices=ESTADOS,
        initial='Activo',
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        )
    )

    class Meta:

        model = Usuarios

        fields = [
            'correo',
            'nombre',
            'codigoevo',
            'rol',
            'status'
        ]

# ==========================================================
# Mantenimientos
# ==========================================================

class listaMantenimientosForm(forms.ModelForm):
    ESTADOS = [
        ('', ''),
        ('Vigente', 'Vigente'),
        ('No vigente', 'No vigente'),
        ('Anulada', 'Anulada'),
    ]

    descripcion = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la descripción del mantenimiento'
            }
        )
    )

    maquina = forms.ModelChoiceField(
        queryset=Maquina.objects.filter(
            status='Activa'
        ).order_by('nombre'),
        empty_label='Seleccione una máquina',
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        )
    )

    periodo = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ej. Mensual, Trimestral, Anual'
            }
        )
    )

    status = forms.ChoiceField(
        choices=ESTADOS,
        initial='Vigente',
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        )
    )


    class Meta:

        model = ListaMantenimientos

        fields = [
            'descripcion',
            'maquina',
            'periodo',
            'status'
        ]

# ==========================================================
# Distribucion METADATA
# ==========================================================

class distribucionMaquinasForm(forms.ModelForm):
    ESTADOS = [
        ('', ''),
        ('Activa', 'Activa'),
        ('Inactiva', 'Inactiva'),
        ('Anulada', 'Anulada'),
    ]


    ubicacion = forms.ModelChoiceField(
        queryset=Ubicacion.objects.filter(
            status='Abierta'
        ).order_by('nombre'),
        empty_label='Seleccione una ubicación',
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        )
    )


    maquina = forms.ModelChoiceField(
        queryset=Maquina.objects.filter(
            status='Activa'
        ).order_by('nombre'),
        empty_label='Seleccione una máquina',
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        )
    )


    status = forms.ChoiceField(
        choices=ESTADOS,
        initial='Activa',
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        )
    )


    serie = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el número de serie'
            }
        )
    )


    fecha_compra = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date'
            }
        )
    )


    centrodecosto = forms.ModelChoiceField(
        queryset=centrodecosto.objects.filter(
            status='Abierto'
        ).order_by('centrodecosto'),
        required=False,
        empty_label='Seleccione un centro de costo',
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        )
    )


    class Meta:

        model = DistribucionMaquinas

        fields = [
            'ubicacion',
            'maquina',
            'status',
            'serie',
            'fecha_compra',
            'centrodecosto',
        ]