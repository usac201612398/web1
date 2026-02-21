from django.db import models

# Create your models here.

class m1Sensoresdata(models.Model):
    registro = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    planta_id = models.CharField(max_length=50)
    temperatura = models.FloatField()
    humedad_aire = models.FloatField()
    humedad_suelo = models.FloatField()
    peso = models.FloatField()

    def __str__(self):
        return f"{self.planta_id} - {self.temperatura}°C / {self.humedad_aire}% - {self.humedad_suelo}% - {self.peso}kg"

class m2Sensoresdata(models.Model):
    registro = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    tanque_id = models.CharField(max_length=50)
    temperatura = models.FloatField()
    caudal = models.FloatField()
    porcentaje_llenado = models.FloatField()
    nivel = models.FloatField()

    def __str__(self):
        return f"{self.tanque_id} - {self.temperatura}°C / {self.caudal}L/min - {self.porcentaje_llenado}%  - {self.nivel}cm"
    
class riegoRegistro(models.Model):
    registro = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(auto_now_add=True)
    zona = models.IntegerField()
    accion = models.CharField(max_length=10)  # ON / OFF
    tiempo_segundos = models.IntegerField()
    temp_amb = models.FloatField(null=True, blank=True)
    hum_amb = models.FloatField(null=True, blank=True)
    hum_suelo = models.FloatField(null=True, blank=True)
    peso = models.FloatField(null=True, blank=True)
    modo = models.CharField(max_length=15)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"Riego zona {self.zona} - {self.accion} - {self.fecha}"