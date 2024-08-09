from django.db import models

# Create your models here.
class salidasFruta(models.Model):

    id = models.AutoField(primary_key=True)
    finca = models.CharField(max_length=25)
    viaje = models.CharField(max_length=20)
    encargado = models.CharField(max_length=30)
    orden = models.CharField(max_length=20)
    cultivo = models.CharField(max_length=45)
    variedad = models.CharField(max_length=40)
    cajas = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title