from django import forms
from django.forms import inlineformset_factory

from .models import Actividad, Area, Evidencia, Maquina, Programa, Servicio


class BootstrapMixin:
    """Agrega clases CSS a todos los widgets."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            w = field.widget
            if isinstance(w, forms.CheckboxInput):
                w.attrs.setdefault("class", "chk")
            elif isinstance(w, (forms.Select, forms.SelectMultiple)):
                w.attrs.setdefault("class", "inp")
            else:
                w.attrs.setdefault("class", "inp")


class AreaForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Area
        fields = ["nombre", "responsable", "activa"]


class MaquinaForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Maquina
        fields = [
            "area", "tipo", "nombre", "controlador", "codigo",
            "ubicacion", "fecha_instalacion", "activa", "notas",
        ]
        widgets = {
            "fecha_instalacion": forms.DateInput(attrs={"type": "date"}),
            "notas": forms.Textarea(attrs={"rows": 3}),
        }


class ActividadForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Actividad
        fields = [
            "nombre", "descripcion", "frecuencia", "aplica_a",
            "requiere_evidencia", "duracion_estimada_min", "activa",
        ]
        widgets = {"descripcion": forms.Textarea(attrs={"rows": 5})}


class ProgramaForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Programa
        fields = ["maquina", "actividad", "fecha_base", "responsable", "activo"]
        widgets = {"fecha_base": forms.DateInput(attrs={"type": "date"})}

    def clean(self):
        data = super().clean()
        maquina, actividad = data.get("maquina"), data.get("actividad")
        if maquina and actividad and actividad.aplica_a != "TODAS" \
                and actividad.aplica_a != maquina.tipo:
            raise forms.ValidationError(
                f"La actividad aplica solo a máquinas tipo {actividad.get_aplica_a_display()}."
            )
        return data


class ServicioForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Servicio
        fields = [
            "programa", "fecha", "estado", "realizado_por", "tecnico_externo",
            "duracion_min", "hallazgos", "observaciones", "requiere_seguimiento",
            "foto_antes", "foto_despues",
        ]
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date"}),
            "hallazgos": forms.Textarea(attrs={"rows": 3}),
            "observaciones": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["programa"].queryset = (
            Programa.objects.filter(activo=True)
            .select_related("maquina__area", "actividad")
        )

    def clean(self):
        data = super().clean()
        programa = data.get("programa")
        if (
            programa
            and data.get("estado") == Servicio.REALIZADO
            and programa.actividad.requiere_evidencia
            and not (data.get("foto_antes") or data.get("foto_despues"))
        ):
            raise forms.ValidationError(
                "Esta actividad exige evidencia fotográfica (antes y/o después)."
            )
        return data


class EvidenciaForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Evidencia
        fields = ["tipo", "archivo", "descripcion"]


EvidenciaFormSet = inlineformset_factory(
    Servicio, Evidencia, form=EvidenciaForm, extra=2, can_delete=True
)