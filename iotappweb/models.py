from django.db import models
from django.utils import timezone


class VaporSaturacion(models.Model):
    temperatura = models.DecimalField(max_digits=4, decimal_places=1, unique=True)
    presion_hpa = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.temperatura}°C → {self.presion_hpa} hPa"

class SensorDetalles(models.Model):
    id_sensor= models.BigAutoField(primary_key=True)
    sensor = models.CharField(max_length=100, unique = True)
    nombrearanet = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20)  # "peso" o "temperatura", "etc"
    priva = models.CharField(max_length=20)  
    estructura = models.CharField(max_length=25)  
    finca = models.CharField(max_length=30)
    set_point = models.FloatField(default=23)
    umbral_min = models.FloatField(default=9)
    umbral_max = models.FloatField(default=-9)
    status = models.CharField(max_length= 30, blank = True, null =  True)
    
    def __str__(self):
        return f"{self.nombrearanet} ({self.sensor})"

class SensorData(models.Model):

    sensor = models.ForeignKey(
        SensorDetalles,
        on_delete=models.CASCADE
    )
    metric = models.CharField(max_length=50)
    value = models.FloatField()
    unit = models.CharField(max_length=20, null=True, blank=True)
    timestamp = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sensor} - {self.metric} - {self.value}"

class SensorAlert(models.Model):
    sensor = models.CharField(max_length=50)
    tipo = models.CharField(max_length=20)  # "riego" o "exceso"
    porcentaje_perdida = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    mensaje = models.TextField()



class m1Sensoresdata(models.Model):
    registro = models.BigAutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    planta_id = models.CharField(max_length=50)
    temperatura = models.FloatField()
    humedad_aire = models.FloatField()
    humedad_suelo = models.FloatField()
    peso = models.FloatField()

    def __str__(self):
        return f"Reg: {self.registro} - {self.timestamp} - {self.planta_id} - {self.temperatura}°C / {self.humedad_aire}% - {self.humedad_suelo}% - {self.peso}kg"

class m2Sensoresdata(models.Model):
    registro = models.BigAutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    tanque_id = models.CharField(max_length=50)
    temperatura = models.FloatField()
    caudal = models.FloatField()
    porcentaje_llenado = models.FloatField()
    nivel = models.FloatField()

    def __str__(self):
        return f"Reg: {self.registro} - {self.timestamp} - {self.tanque_id} - {self.temperatura}°C / {self.caudal}L/min - {self.porcentaje_llenado}%  - {self.nivel}cm"
    
class riegoRegistro(models.Model):
    registro = models.BigAutoField(primary_key=True)
    fecha = models.DateTimeField(auto_now_add=True)
    zona = models.IntegerField()
    accion = models.CharField(max_length=10)  # ON / OFF
    tiempo_segundos = models.IntegerField()
    planta_reg = models.ForeignKey(m1Sensoresdata, on_delete=models.SET_NULL, null=True)
    tanque_reg = models.ForeignKey(m2Sensoresdata, on_delete=models.SET_NULL, null=True)
    modo = models.CharField(max_length=15)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"Reg: {self.registro} - {self.fecha} - Riego zona {self.zona} - {self.accion} "

class riegoResumen(models.Model):
    registro = models.BigAutoField(primary_key=True)
    fecha = models.DateTimeField(auto_now_add=True)

    riego = models.OneToOneField(
        riegoRegistro,
        on_delete=models.CASCADE,
        related_name="resumen"
    )

    litros_usados = models.FloatField()

    def _str_(self):
        return f"Reg: {self.registro} - {self.feha} - Resumen zona {self.riego.zona} - {self.litros_usados} L"