from django.db import models

# Create your models here.

class m1Sensoresdata(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    planta_id = models.CharField(max_length=50)
    temperatura = models.FloatField()
    humedad_aire = models.FloatField()
    humedad_suelo = models.FloatField()
    peso = models.FloatField()

    def __str__(self):
        return f"{self.device_id} - {self.temperatura}°C / {self.humedad_aire}% - {self.humedad_suelo}% - {self.peso}g"