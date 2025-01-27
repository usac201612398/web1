from django.db import models

# Create your models here.
class scorepersonal(models.Model):
    id = models.BigAutoField(primary_key=True)
    finca = models.CharField(max_length=20, blank=True, null=True)
    encargado =models.CharField(max_length=20, blank=True, null=True)
    cuadrilla = models.CharField(max_length=20, blank=True, null=True)
    codigop = models.BigIntegerField(blank=True, null=True)
    nombrep = models.CharField(max_length=75, blank=True, null=True)
    estructura = models.CharField(max_length=20, blank=True, null=True)
    area = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return str(self.nombrep)
    
class scoremanejo(models.Model):
    id = models.BigAutoField(primary_key=True)
    finca = models.CharField(max_length=20, blank=True, null=True)
    encargado =models.CharField(max_length=20, blank=True, null=True)
    cuadrilla = models.CharField(max_length=20, blank=True, null=True)
    codigop = models.BigIntegerField(blank=True, null=True)
    nombrep = models.CharField(max_length=75, blank=True, null=True)
    estructura = models.CharField(max_length=20, blank=True, null=True)
    area = models.CharField(max_length=20, blank=True, null=True)
    
    fecha = models.DateField(blank=True, null=True)
    semana = models.BigIntegerField(blank=True, null=True)
    año = models.BigIntegerField(blank=True, null=True)
    bajado = models.BigIntegerField(blank=True, null=True)
    distri_ejes = models.BigIntegerField(blank=True, null=True)
    deshije = models.BigIntegerField(blank=True, null=True)
    guiado = models.BigIntegerField(blank=True, null=True)
    hil_ban_rec_ejes = models.BigIntegerField(blank=True, null=True)
    orden_limpieza = models.BigIntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.nombrep)
    
class scorecosecha(models.Model):
    id = models.BigAutoField(primary_key=True)
    finca = models.CharField(max_length=20, blank=True, null=True)
    encargado =models.CharField(max_length=20, blank=True, null=True)
    cuadrilla = models.CharField(max_length=20, blank=True, null=True)
    codigop = models.BigIntegerField(blank=True, null=True)
    nombrep = models.CharField(max_length=75, blank=True, null=True)
    estructura = models.CharField(max_length=20, blank=True, null=True)
    area = models.CharField(max_length=20, blank=True, null=True)
    
    fecha = models.DateField(blank=True, null=True)
    semana = models.BigIntegerField(blank=True, null=True)
    año = models.BigIntegerField(blank=True, null=True)
    grado_mad = models.BigIntegerField(blank=True, null=True)
    deshoje = models.BigIntegerField(blank=True, null=True)
    descoronado = models.BigIntegerField(blank=True, null=True)
    orden_limpieza = models.BigIntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.nombrep)