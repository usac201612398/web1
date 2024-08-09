from django.db import models

# Create your models here.
class usuariosAppFruta(models.Model):
    correo = models.CharField(primary_key=True,max_length=75, blank=False)
    encargado = models.CharField(max_length=30)
    finca = models.CharField(max_length=25)
    
    def __str__(self):
        return self.title
    
class salidasFruta(models.Model):
    
    op_viajes = [('Viaje 1','Viaje 1'),('Viaje 2','Viaje 2'),('Viaje 3', 'Viaje 3'),('Viaje 4','Viaje 4'),('Viaje 5','Viaje 5'),('Viaje 6','Viaje 6')]
    
    id = models.AutoField(primary_key=True)
    finca = models.CharField(max_length=25)
    viaje = models.CharField(max_length=20, choices=op_viajes)
    encargado = models.CharField(max_length=30)
    orden = models.CharField(max_length=20)
    cultivo = models.CharField(max_length=45)
    variedad = models.CharField(max_length=40)
    cajas = models.IntegerField(blank=True, null=True)
    correo = models.ForeignKey(usuariosAppFruta, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

