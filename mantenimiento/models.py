from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UsuarioMantenimiento(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="mantenimiento"
    )

    puede_acceder = models.BooleanField(
        default=False
    )

    departamento = models.CharField(
        max_length=100,
        blank=True
    )

    cargo = models.CharField(
        max_length=100,
        blank=True
    )

    activo = models.BooleanField(
        default=True
    )
