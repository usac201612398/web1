from django.contrib import admin
from .models import UsuarioMantenimiento


@admin.register(UsuarioMantenimiento)
class UsuarioMantenimientoAdmin(admin.ModelAdmin):

    list_display = (
        "usuario",
        "departamento",
        "cargo",
        "puede_acceder",
        "activo",
    )

    list_filter = (
        "puede_acceder",
        "activo",
        "departamento",
    )

    search_fields = (
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
    )

    list_editable = (
        "puede_acceder",
        "activo",
    )

    def usuario(self, obj):
        return (
            obj.user.get_full_name()
            or obj.user.email
            or obj.user.username
        )

    usuario.short_description = "Usuario"