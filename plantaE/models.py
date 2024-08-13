from django.db import models

# Create your models here.
class usuariosAppFruta(models.Model):

    correo = models.CharField(primary_key=True,max_length=75, blank=True)
    encargado = models.CharField(max_length=30)
    finca = models.CharField(max_length=25)
    
    def __str__(self):
        return (self.finca + " | " + self.encargado)
    
class salidasFruta(models.Model):
    
    op_viajes = [('Viaje 1','Viaje 1'),('Viaje 2','Viaje 2'),('Viaje 3', 'Viaje 3'),('Viaje 4','Viaje 4'),('Viaje 5','Viaje 5'),('Viaje 6','Viaje 6')]
    op_cultivo = [('CHERRY','CHERRY'),('MEDLEY','MEDLEY'),('GRAPE','GRAPE'),('GRAPE ORGANICO','GRAPE ORGANICO'),('CHERRY ORGANICO','CHERRY ORGANICO'),('BLOCKY','BLOCKY'),('BLOCKY ORGANICO','BLOCKY ORGANICO'),('MINI','MINI'),('MINI ORGANICO','MINI ORGANICO')]
    op_variedad = [('BAMANO','BAMANO'),('DUNNE','DUNNE'),('IVORINO','IVORINO'),('KM 5512','KM 5512'),('NEBULA','NEBULA'),('ROJO','ROJO'),('AMARILLO','AMARILLO'),('ANARANJADO','ANARANJADO')]
    op_encargado = [('Brandon Portillo','Brandon Portillo'),('Isaías García','Isaías García')]
    op_finca = [('VALLE','VALLE'),('RIO','RIO'),('CIP','CIP'),('FLE','FLE'),('FLA','FLA')]
    op_correo = [('brandon.portillo@popoyan.com.gt','brandon.portillo@popoyan.com.gt')]
    op_orden = [('60202046','60202046'),('60206054','60206054'),('60206055','60206055'),('60206056','60206056')]
    
    id = models.AutoField(primary_key=True)
    finca = models.CharField(max_length=25,choices=op_finca,null=True)
    viaje = models.CharField(max_length=20, choices=op_viajes,null=True)
    encargado = models.CharField(max_length=30,choices=op_encargado,null=True)
    orden = models.CharField(max_length=20,choices=op_orden,null=True)
    cultivo = models.CharField(max_length=45,choices=op_cultivo,null=True)
    variedad = models.CharField(max_length=40,choices=op_variedad,null=True)
    cajas = models.IntegerField(blank=True, null=True)
    correo = models.CharField(max_length=75, blank=True,choices=op_correo,null=True)
    estructura=models.CharField(max_length=40,choices=op_variedad,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (str(self.finca)+ " | " + str(self.encargado) + " | " + str(self.viaje)+ " | " + str(self.orden))

class datosProduccion(models.Model):

    op_finca = [('VALLE','VALLE'),('RIO','RIO'),('CIP', 'CIP'),('FLE','FLE'),('PASTORIA','PASTORIA')]
    op_cultivo = [('CHERRY','CHERRY'),('MEDLEY','MEDLEY'),('GRAPE','GRAPE'),('GRAPE ORGANICO','GRAPE ORGANICO'),('CHERRY ORGANICO','CHERRY ORGANICO'),('BLOCKY','BLOCKY'),('BLOCKY ORGANICO','BLOCKY ORGANICO'),('MINI','MINI'),('MINI ORGANICO','MINI ORGANICO')]
    op_status = [('Abierta','Abierta'),('Cerrada','Cerrada')]
    op_temporada = [('Temp 2023-2024','Temp 2023-2024'),('Temp 2024-2025','Temp 2024-2025')]
    id = models.AutoField(primary_key=True)
    finca = models.CharField(max_length=25,choices=op_finca,blank=True)
    orden = models.CharField(max_length=30,blank=True)
    cultivo = models.CharField(max_length=35, choices=op_cultivo,blank=True)
    area = models.FloatField(blank=True, null=True)
    temporada = models.CharField(max_length=45, choices=op_temporada,blank=True)
    status = models.CharField(max_length=35, choices=op_status,blank=True)

    
    def __str__(self):
        return (str(self.finca) + " | " + str(self.orden)+ " | " + str(self.temporada)+ " | " + str(self.status) )
    
class detallesProduccion(models.Model):

    op_cultivo = [('CHERRY','CHERRY'),('MEDLEY','MEDLEY'),('GRAPE','GRAPE'),('GRAPE ORGANICO','GRAPE ORGANICO'),('CHERRY ORGANICO','CHERRY ORGANICO'),('BLOCKY','BLOCKY'),('BLOCKY ORGANICO','BLOCKY ORGANICO'),('MINI','MINI'),('MINI ORGANICO','MINI ORGANICO')]
    
    id = models.AutoField(primary_key=True)
    cultivo = models.CharField(max_length=35, choices=op_cultivo,blank=True)
    variedad = models.CharField(max_length=35, blank=True)
    
    def __str__(self):
        return (str(self.cultivo) + " | " + str(self.variedad) )
    

class detallesEstructuras(models.Model):

    op_cultivo = [('CHERRY','CHERRY'),('MEDLEY','MEDLEY'),('GRAPE','GRAPE'),('GRAPE ORGANICO','GRAPE ORGANICO'),('CHERRY ORGANICO','CHERRY ORGANICO'),('BLOCKY','BLOCKY'),('BLOCKY ORGANICO','BLOCKY ORGANICO'),('MINI','MINI'),('MINI ORGANICO','MINI ORGANICO')]
    op_estructura = [('CM1','CM1'),('CM2','CM2'),('CM3','CM3'),('CM4','CM4'),('CM5','CM5'),('CM6','CM6'),('CM7','CM7')]
    id = models.AutoField(primary_key=True)
    orden = models.CharField(max_length=30,blank=True)
    cultivo = models.CharField(max_length=35, choices=op_cultivo,blank=True)
    estructura = models.CharField(max_length=35, choices=op_estructura,blank=True)

    def __str__(self):
        return (str(self.orden) + " | " + str(self.estructura) )