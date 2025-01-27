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