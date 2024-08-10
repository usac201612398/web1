from django.db import models

# Create your models here.
class usuariosAppFruta(models.Model):
    correo = models.CharField(primary_key=True,max_length=75, blank=True)
    encargado = models.CharField(max_length=30)
    finca = models.CharField(max_length=25)
    
    def __str__(self):
        return self.correo
    
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
    correo = models.CharField(max_length=75, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id

class datosProduccion(models.Model):

    op_finca = [('VALLE','VALLE'),('RIO','RIO'),('CIP', 'CIP'),('FLE','FLE'),('PASTORIA','PASTORIA')]
    op_cultivo = [('CHERRY','CHERRY'),('MEDLEY','MEDLEY'),('GRAPE','GRAPE'),('GRAPE ORGANICO','GRAPE ORGANICO'),('CHERRY ORGANICO','CHERRY ORGANICO'),('BLOCKY','BLOCKY'),('BLOCKY ORGANICO','BLOCKY ORGANICO'),('MINI','MINI'),('MINI ORGANICO','MINI ORGANICO')]
    op_status = [('Abierta','Abierta'),('Cerrada','Cerrada')]
    op_temporada = [('Temp 2023-2024','Temp 2023-2024'),('Temp 2024-2025','Temp 2024-2025')]
    id = models.AutoField(primary_key=True)
    finca = models.CharField(max_length=25,choices=op_finca)
    orden = models.CharField(max_length=30)
    cultivo = models.CharField(max_length=35, choices=op_cultivo)
    area = models.FloatField(blank=True, null=True)
    temporada = models.CharField(max_length=45, choices=op_temporada)
    status = models.CharField(max_length=35, choices=op_status)

    
    def __str__(self):
        return self.id