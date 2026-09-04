from django.contrib import admin
from django.utils.html import format_html

from .models import Actividad, Area, Evidencia, Maquina, Programa, Servicio


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "responsable", "activa")
    list_filter = ("activa",)
    search_fields = ("nombre", "responsable")


class ProgramaInline(admin.TabularInline):
    model = Programa
    extra = 0
    autocomplete_fields = ("actividad",)


@admin.register(Maquina)
class MaquinaAdmin(admin.ModelAdmin):
    list_display = ("codigo", "area", "tipo", "nombre", "controlador", "activa")
    list_filter = ("area", "tipo", "controlador", "activa")
    search_fields = ("nombre", "codigo", "controlador")
    inlines = [ProgramaInline]


@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    list_display = ("nombre_corto", "frecuencia", "aplica_a", "requiere_evidencia", "activa")
    list_filter = ("frecuencia", "aplica_a", "activa")
    search_fields = ("nombre", "descripcion")

    @admin.display(description="Actividad")
    def nombre_corto(self, obj):
        return obj.nombre[:80]


@admin.register(Programa)
class ProgramaAdmin(admin.ModelAdmin):
    list_display = ("maquina", "actividad", "proxima", "estado_col", "activo")
    list_filter = ("activo", "actividad__frecuencia", "maquina__area")
    autocomplete_fields = ("maquina", "actividad")

    @admin.display(description="Próxima")
    def proxima(self, obj):
        return obj.proxima_fecha

    @admin.display(description="Estado")
    def estado_col(self, obj):
        colores = {"AL_DIA": "green", "PROXIMO": "orange", "VENCIDO": "red"}
        return format_html(
            '<b style="color:{}">{}</b>', colores[obj.estado], obj.estado_label
        )


class EvidenciaInline(admin.TabularInline):
    model = Evidencia
    extra = 1


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ("fecha", "programa", "estado", "atendido_por", "requiere_seguimiento")
    list_filter = ("estado", "fecha", "requiere_seguimiento", "programa__maquina__area")
    search_fields = ("observaciones", "hallazgos", "tecnico_externo")
    date_hierarchy = "fecha"
    inlines = [EvidenciaInline]
