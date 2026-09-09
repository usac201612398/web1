from django.db import models
from django.core.exceptions import ValidationError

class Maquina(models.Model):

    ESTADOS = [
        ('', ''),
        ('Activa', 'Activa'),
        ('Inactiva', 'Inactiva'),
        ('Averiada', 'Averiada'),
        ('Anulada', 'Anulada'),
    ]

    registro = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    tipo = models.CharField(max_length=100, blank=True, null=True)
    
    status = models.CharField(
        max_length=15,
        choices=ESTADOS,
        default='Activa'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.registro} | {self.nombre}"

class Ubicacion(models.Model):

    ESTADOS = [
        ('', ''),
        ('Abierta', 'Abierta'),
        ('Cerrada', 'Cerrada'),
        ('Anulada', 'Anulada'),
    ]

    registro = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(
        max_length=15,
        choices=ESTADOS,
        default='Abierta'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.registro} | {self.nombre}"

class centrodecosto(models.Model):

    ESTADOS = [
        ('', ''),
        ('Abierto', 'Abierto'),
        ('Cerrado', 'Cerrado'),
        ('Anulado', 'Anulado'),
    ]

    registro = models.BigAutoField(primary_key=True)
    centrodecosto = models.CharField(max_length=100, blank=True, null=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(
        max_length=15,
        choices=ESTADOS,
        default='Abierto'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.centrodecosto} | {self.nombre}"

class DistribucionMaquinas(models.Model):

    ESTADOS = [
        ('', ''),
        ('Activa', 'Activa'),
        ('Inactiva', 'Inactiva'),
        ('Anulada', 'Anulada'),
    ]

    registro = models.BigAutoField(primary_key=True)
    ubicacion = models.ForeignKey(
        Ubicacion,
        on_delete=models.PROTECT
    )
    maquina = models.ForeignKey(
        Maquina,
        on_delete=models.PROTECT
    )
    status = models.CharField(
        max_length=15,
        choices=ESTADOS,
        default='Activa'
    )
    serie = models.CharField(max_length=100, blank=True, null=True)
    fecha_compra = models.DateField(blank=True, null=True)
    centrodecosto = models.ForeignKey(
        centrocosto,
        on_delete=models.PROTECT, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.registro} | {self.ubicacion.nombre} | {self.maquina.nombre} | {self.serie}"

class ListaMantenimientos(models.Model):

    ESTADOS = [
        ('', ''),
        ('Vigente', 'Vigente'),
        ('No vigente', 'No vigente'),
        ('Anulada', 'Anulada'),
    ]

    registro = models.BigAutoField(primary_key=True)
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    maquina = models.ForeignKey(
        Maquina,
        on_delete=models.PROTECT
    )
    periodo = models.CharField(max_length=30, blank=True, null=True)
    status = models.CharField(
        max_length=15,
        choices=ESTADOS,
        default='Vigente'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return f"{self.descripcion} | {self.maquina.nombre}"

class Usuarios(models.Model):

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

    registro = models.BigAutoField(primary_key=True)

    correo = models.EmailField(unique=True)

    nombre = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    codigoevo = models.BigIntegerField(blank=True, null=True)

    rol = models.CharField(
        max_length=20,
        choices=ROLES, blank=True, null=True
    )

    status = models.CharField(
        max_length=15,
        choices=ESTADOS,
        default='Activo'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.registro} | {self.nombre} ({self.rol})"

class SolicitarOperacion(models.Model):

    ESTADOS = [
        ('', ''),
        ('Activa', 'Activa'),
        ('Atendida', 'Atendida'),
        ('Vencida', 'Vencida'),
        ('Anulada', 'Anulada'),
    ]

    registro = models.BigAutoField(primary_key=True)

    mantenimiento = models.ForeignKey(
        ListaMantenimientos,
        on_delete=models.PROTECT
    )

    ubicacion = models.ForeignKey(
        Ubicacion,
        on_delete=models.PROTECT
    )

    solicita = models.ForeignKey(
        Usuarios,
        on_delete=models.PROTECT,
        related_name='solicitudes_creadas'
    )

    atiende = models.ForeignKey(
        Usuarios,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='solicitudes_atendidas'
    )

    maquina = models.ForeignKey(
        Maquina,
        on_delete=models.PROTECT
    )

    fecha_solicitud = models.DateField(blank=True, null=True)

    status = models.CharField(
        max_length=15,
        choices=ESTADOS,
        default='Activa'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    observaciones = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    def clean(self):
        if self.mantenimiento and self.maquina:
            if self.mantenimiento.maquina != self.maquina:
                raise ValidationError(
                    "El mantenimiento no pertenece a la máquina seleccionada."
                )

    def __str__(self):
        return (
            f"{self.registro} | "
            f"{self.mantenimiento.descripcion} | "
            f"{self.maquina.nombre} | "
            f"{self.ubicacion.nombre}"
        )

class MantenimientoRealizado(models.Model):

    ESTADOS = [
        ('', ''),
        ('Activo', 'Activo'),
        ('Atendido', 'Atendido'),
        ('Vencido', 'Vencido'),
        ('Anulado', 'Anulado'),
    ]

    operacion = models.ForeignKey(
        SolicitarOperacion,
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    maquina = models.ForeignKey(
        Maquina,
        on_delete=models.PROTECT
    )

    ubicacion = models.ForeignKey(
        Ubicacion,
        on_delete=models.PROTECT
    )

    mantenimiento = models.ForeignKey(
        ListaMantenimientos,
        on_delete=models.PROTECT
    )

    atiende = models.ForeignKey(
        Usuarios,
        on_delete=models.PROTECT
    )

    fecha_mantenimiento = models.DateField(
        blank=True,
        null=True
    )

    fecha_proximo_mantenimiento = models.DateField(
        blank=True,
        null=True
    )

    origen = models.CharField(
        max_length=20,
        choices=[
            ('Solicitud', 'Solicitud'),
            ('Preventivo', 'Preventivo'),
            ('Supervisor', 'Supervisor'),
            ('Emergencia', 'Emergencia'),
        ]
    )
    status = models.CharField(
        max_length=15,
        choices=ESTADOS,
        default='Activo'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"{self.operacion} | "
            f"{self.mantenimiento.descripcion} | "
            f"{self.maquina.nombre} | "
            f"{self.ubicacion.nombre}"
        )