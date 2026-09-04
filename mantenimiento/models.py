from datetime import timedelta

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone


# ---------------------------------------------------------------------------
# Catálogos
# ---------------------------------------------------------------------------
class Area(models.Model):
    """Finca / área donde están instaladas las máquinas (Cecilio, CIP, Valle...)."""

    nombre = models.CharField(max_length=60, unique=True)
    responsable = models.CharField(max_length=120, blank=True)
    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Área"
        verbose_name_plural = "Áreas"

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse("area_list")

    # --- indicadores para el tablero -------------------------------------
    @property
    def maquinas_activas(self):
        return self.maquinas.filter(activa=True)


class Maquina(models.Model):
    TIPO_PRIVA = "PRIVA"
    TIPO_VIALUX = "VIALUX"
    TIPOS = [(TIPO_PRIVA, "Priva"), (TIPO_VIALUX, "Vialux")]

    CONTROLADORES = [
        ("Conext", "Conext"),
        ("Intégro", "Intégro"),
        ("Compact", "Compact"),
    ]

    area = models.ForeignKey(Area, on_delete=models.PROTECT, related_name="maquinas")
    tipo = models.CharField(max_length=10, choices=TIPOS, default=TIPO_PRIVA)
    nombre = models.CharField(
        max_length=40,
        help_text="Identificador dentro del área. Ej. 'Priva 2', 'Vialux'.",
    )
    controlador = models.CharField(max_length=20, choices=CONTROLADORES)
    codigo = models.CharField(
        max_length=40, unique=True, blank=True,
        help_text="Código interno. Si se deja vacío se genera automáticamente.",
    )
    ubicacion = models.CharField(max_length=150, blank=True)
    fecha_instalacion = models.DateField(null=True, blank=True)
    activa = models.BooleanField(default=True)
    notas = models.TextField(blank=True)

    class Meta:
        ordering = ["area__nombre", "tipo", "nombre"]
        verbose_name = "Máquina"
        verbose_name_plural = "Máquinas"

    def __str__(self):
        return f"{self.area} · {self.nombre} ({self.controlador})"

    def save(self, *args, **kwargs):
        if not self.codigo:
            base = f"{self.area.nombre[:3].upper()}-{self.nombre.upper().replace(' ', '')}"
            codigo, n = base, 1
            while Maquina.objects.filter(codigo=codigo).exclude(pk=self.pk).exists():
                n += 1
                codigo = f"{base}-{n}"
            self.codigo = codigo
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("maquina_detail", args=[self.pk])

    # --- semáforo agregado de la máquina ---------------------------------
    @property
    def estado(self):
        """Peor estado entre todos sus programas activos."""
        estados = [p.estado for p in self.programas.filter(activo=True)]
        for critico in (Programa.VENCIDO, Programa.PROXIMO, Programa.AL_DIA):
            if critico in estados:
                return critico
        return Programa.AL_DIA

    @property
    def programas_vencidos(self):
        return [p for p in self.programas.filter(activo=True) if p.estado == Programa.VENCIDO]


class Actividad(models.Model):
    """Actividad del plan de mantenimiento preventivo (ficha técnica)."""

    DIARIO = "DIARIO"
    SEMANAL = "SEMANAL"
    MENSUAL = "MENSUAL"
    TRIMESTRAL = "TRIMESTRAL"
    SEMESTRAL = "SEMESTRAL"
    ANUAL = "ANUAL"

    FRECUENCIAS = [
        (DIARIO, "Diario"),
        (SEMANAL, "Semanal"),
        (MENSUAL, "Mensual"),
        (TRIMESTRAL, "Trimestral"),
        (SEMESTRAL, "Semestral"),
        (ANUAL, "Anual"),
    ]

    # días entre servicios por frecuencia
    DIAS = {
        DIARIO: 1,
        SEMANAL: 7,
        MENSUAL: 30,
        TRIMESTRAL: 91,
        SEMESTRAL: 182,
        ANUAL: 365,
    }

    # días de anticipación con que se avisa "próximo a vencer"
    ALERTA = {
        DIARIO: 0,
        SEMANAL: 2,
        MENSUAL: 5,
        TRIMESTRAL: 10,
        SEMESTRAL: 15,
        ANUAL: 30,
    }

    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(
        blank=True, help_text="Procedimiento paso a paso que debe seguir el técnico."
    )
    frecuencia = models.CharField(max_length=12, choices=FRECUENCIAS, default=MENSUAL)
    aplica_a = models.CharField(
        max_length=10,
        choices=[("TODAS", "Todas")] + Maquina.TIPOS,
        default="TODAS",
    )
    requiere_evidencia = models.BooleanField(
        default=False, help_text="Exige foto antes/después al cerrar el servicio."
    )
    duracion_estimada_min = models.PositiveIntegerField(
        default=30, validators=[MinValueValidator(1)], verbose_name="Duración estimada (min)"
    )
    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ["frecuencia", "nombre"]
        verbose_name = "Actividad"
        verbose_name_plural = "Actividades"

    def __str__(self):
        return f"[{self.get_frecuencia_display()}] {self.nombre[:70]}"

    def get_absolute_url(self):
        return reverse("actividad_list")

    @property
    def dias_ciclo(self):
        return self.DIAS[self.frecuencia]

    @property
    def dias_alerta(self):
        return self.ALERTA[self.frecuencia]


# ---------------------------------------------------------------------------
# Programación: qué actividad le toca a qué máquina
# ---------------------------------------------------------------------------
class Programa(models.Model):
    """Asignación Máquina ↔ Actividad. Es lo que define 'cuándo toca'."""

    AL_DIA = "AL_DIA"
    PROXIMO = "PROXIMO"
    VENCIDO = "VENCIDO"

    ESTADO_LABEL = {
        AL_DIA: "Al día",
        PROXIMO: "Por vencer",
        VENCIDO: "Vencido",
    }
    ESTADO_CSS = {AL_DIA: "ok", PROXIMO: "warn", VENCIDO: "bad"}

    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE, related_name="programas")
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE, related_name="programas")
    fecha_base = models.DateField(
        default=timezone.localdate,
        help_text="Fecha desde la que empieza a contar el ciclo si aún no hay servicios.",
    )
    responsable = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="programas",
    )
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["maquina", "actividad"]
        constraints = [
            models.UniqueConstraint(fields=["maquina", "actividad"], name="uniq_maquina_actividad")
        ]
        verbose_name = "Programa"
        verbose_name_plural = "Programación"

    def __str__(self):
        return f"{self.maquina} → {self.actividad.nombre[:50]}"

    def get_absolute_url(self):
        return reverse("maquina_detail", args=[self.maquina_id])

    # --- lógica de vencimiento -------------------------------------------
    @property
    def ultimo_servicio(self):
        return self.servicios.filter(estado=Servicio.REALIZADO).order_by("-fecha").first()

    @property
    def ultima_fecha(self):
        s = self.ultimo_servicio
        return s.fecha if s else None

    @property
    def proxima_fecha(self):
        base = self.ultima_fecha or self.fecha_base
        return base + timedelta(days=self.actividad.dias_ciclo)

    @property
    def dias_restantes(self):
        return (self.proxima_fecha - timezone.localdate()).days

    @property
    def estado(self):
        d = self.dias_restantes
        if d < 0:
            return self.VENCIDO
        if d <= self.actividad.dias_alerta:
            return self.PROXIMO
        return self.AL_DIA

    @property
    def estado_label(self):
        return self.ESTADO_LABEL[self.estado]

    @property
    def estado_css(self):
        return self.ESTADO_CSS[self.estado]


# ---------------------------------------------------------------------------
# Historial de servicios
# ---------------------------------------------------------------------------
class Servicio(models.Model):
    """Registro histórico de un mantenimiento ejecutado (o programado/omitido)."""

    REALIZADO = "REALIZADO"
    PROGRAMADO = "PROGRAMADO"
    OMITIDO = "OMITIDO"
    ESTADOS = [
        (PROGRAMADO, "Programado"),
        (REALIZADO, "Realizado"),
        (OMITIDO, "Omitido / No aplica"),
    ]

    programa = models.ForeignKey(Programa, on_delete=models.CASCADE, related_name="servicios")
    fecha = models.DateField(default=timezone.localdate, verbose_name="Fecha de atención")
    estado = models.CharField(max_length=12, choices=ESTADOS, default=REALIZADO)
    realizado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="servicios",
    )
    tecnico_externo = models.CharField(
        max_length=120, blank=True,
        help_text="Usar solo si quien atendió no tiene usuario en el sistema.",
    )
    duracion_min = models.PositiveIntegerField(null=True, blank=True, verbose_name="Duración (min)")
    hallazgos = models.TextField(blank=True, help_text="Qué se encontró (fugas, ruidos, lecturas).")
    observaciones = models.TextField(blank=True)
    requiere_seguimiento = models.BooleanField(default=False)
    foto_antes = models.ImageField(upload_to="servicios/antes/", blank=True, null=True)
    foto_despues = models.ImageField(upload_to="servicios/despues/", blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-fecha", "-id"]
        verbose_name = "Servicio"
        verbose_name_plural = "Historial de servicios"
        indexes = [models.Index(fields=["fecha", "estado"])]

    def __str__(self):
        return f"{self.fecha} · {self.programa.actividad.nombre[:40]} · {self.programa.maquina}"

    def get_absolute_url(self):
        return reverse("servicio_detail", args=[self.pk])

    @property
    def atendido_por(self):
        if self.realizado_por:
            return self.realizado_por.get_full_name() or self.realizado_por.username
        return self.tecnico_externo or "—"

    @property
    def tiene_evidencia(self):
        return bool(self.foto_antes or self.foto_despues or self.evidencias.exists())


class Evidencia(models.Model):
    """Fotos u otros archivos adicionales del servicio."""

    TIPOS = [("ANTES", "Antes"), ("DESPUES", "Después"), ("OTRO", "Otro")]

    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name="evidencias")
    tipo = models.CharField(max_length=10, choices=TIPOS, default="OTRO")
    archivo = models.FileField(upload_to="evidencias/%Y/%m/")
    descripcion = models.CharField(max_length=200, blank=True)
    subido_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["tipo", "id"]
        verbose_name = "Evidencia"
        verbose_name_plural = "Evidencias"

    def __str__(self):
        return f"{self.get_tipo_display()} · {self.servicio_id}"