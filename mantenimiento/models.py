from django.db import models
from django.contrib.auth.models import User

class UsuarioMantenimiento(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="mantenimiento"
    )

    puede_acceder = models.BooleanField(
        default=False,
        verbose_name="Puede acceder"
    )

    departamento = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Departamento"
    )

    cargo = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Cargo"
    )

    activo = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )

    def __str__(self):
        return self.user.get_full_name() or self.user.username
