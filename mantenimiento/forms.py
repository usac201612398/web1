from django import forms
from .models import *

# ==========================================================
# UBICACIONES
# ==========================================================

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
# CENTRO DE COSTO
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
# USUARIOS
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
# LISTA DE ELEMENTOS DE MANTENIMIENTO
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
# DISTRIBUCION DE MAQUINAS - METADATA
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

# ==========================================================
# SOLICITAR MANTENIMIENTO FORM
# ==========================================================

class SolicitarOperacionForm(forms.ModelForm):

    class Meta:
        model = SolicitarOperacion

        fields = [
            'ubicacion',
            'maquina',
            'mantenimiento',
            'fecha_solicitud',
            'observaciones',
        ]

        widgets = {
            'ubicacion': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),

            'maquina': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),

            'mantenimiento': forms.HiddenInput(),

            'fecha_solicitud': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                }
            ),

            'observaciones': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'maxlength': 100,
                    'placeholder': 'Describe algún detalle de la solicitud...'
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['ubicacion'].empty_label = 'Selecciona una ubicación'
        self.fields['maquina'].empty_label = 'Selecciona una máquina'

        # Inicialmente no mostramos máquinas.
        self.fields['maquina'].queryset = (
            self.fields['maquina'].queryset.none()
        )

        if self.data.get('ubicacion'):

            ubicacion_id = self.data.get('ubicacion')

            from .models import Maquina

            self.fields['maquina'].queryset = (
                Maquina.objects
                .filter(
                    distribucionmaquinas__ubicacion_id=ubicacion_id,
                    distribucionmaquinas__status='Activa'
                )
                .distinct()
                .order_by('nombre')
            )

        elif self.instance.pk:

            self.fields['maquina'].queryset = (
                Maquina.objects
                .filter(pk=self.instance.maquina_id)
            )

    def clean(self):

        cleaned_data = super().clean()

        ubicacion = cleaned_data.get('ubicacion')
        maquina = cleaned_data.get('maquina')
        mantenimiento = cleaned_data.get('mantenimiento')

        if ubicacion and maquina:

            existe = DistribucionMaquinas.objects.filter(
                ubicacion=ubicacion,
                maquina=maquina,
                status='Activa'
            ).exists()

            if not existe:

                raise forms.ValidationError(
                    'La máquina seleccionada no está activa en la '
                    'ubicación seleccionada.'
                )

        if mantenimiento and maquina:

            if mantenimiento.maquina_id != maquina.id:

                self.add_error(
                    'mantenimiento',
                    'El mantenimiento no pertenece a la máquina seleccionada.'
                )

        return cleaned_data
