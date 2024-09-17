from django.db import models

# Create your models here.
class usuariosAppFruta(models.Model):

    correo = models.CharField(primary_key=True,max_length=75, blank=True)
    encargado = models.CharField(max_length=30)
    finca = models.CharField(max_length=25)
    
    def __str__(self):
        return (self.finca + " | " + self.encargado)
    

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
    op_finca =  [('RIO','RIO'),('VALLE','VALLE')]
    op_variedad = [('DUNNE','DUNNE'),('IVORINO','IVORINO'),('KM 5512','KM 5512'),('NEBULA','NEBULA'),('ROJO','ROJO'),('AMARILLO','AMARILLO'),('ANARANJADO','ANARANJADO')]
    
    id = models.AutoField(primary_key=True)
    finca = models.CharField(max_length=35, choices=op_finca,blank=True)
    orden = models.CharField(max_length=30,blank=True)
    cultivo = models.CharField(max_length=35, choices=op_cultivo,blank=True)
    estructura = models.CharField(max_length=35, choices=op_estructura,blank=True)
    variedad = models.CharField(max_length=40, choices=op_estructura,blank=True)

    def __str__(self):
        return (str(self.finca) + " | " + str(self.orden) + " | " + str(self.estructura) + " | " + str(self.variedad)  )

class salidasFruta(models.Model):
    
    op_viajes = [('','-'),('Viaje 1','Viaje 1'),('Viaje 2','Viaje 2'),('Viaje 3', 'Viaje 3'),('Viaje 4','Viaje 4'),('Viaje 5','Viaje 5'),('Viaje 6','Viaje 6'),('Viaje 7','Viaje 7'),('Viaje 8','Viaje 8')]
    op_cultivo = [('CHERRY','CHERRY'),('MEDLEY','MEDLEY'),('GRAPE','GRAPE'),('GRAPE ORGANICO','GRAPE ORGANICO'),('CHERRY ORGANICO','CHERRY ORGANICO'),('BLOCKY','BLOCKY'),('BLOCKY ORGANICO','BLOCKY ORGANICO'),('MINI','MINI'),('MINI ORGANICO','MINI ORGANICO')]
    op_variedad = [('DUNNE','DUNNE'),('IVORINO','IVORINO'),('KM 5512','KM 5512'),('NEBULA','NEBULA'),('ROJO','ROJO'),('AMARILLO','AMARILLO'),('ANARANJADO','ANARANJADO')]
    op_encargado = [('Brandon Portillo','Brandon Portillo'),('Isaías García','Isaías García')]
    op_finca = [('VALLE','VALLE'),('RIO','RIO'),('CIP','CIP'),('FLE','FLE'),('FLA','FLA')]
    op_correo = [('cosecha.rio@popoyan.com.gt','cosecha.rio@popoyan.com.gt')]
    #op_orden = [('64202052','64202052'),('64206054','64206054'),('64206055','64206055'),('64206056','64206056')]
    #op_estructura = [('CM1','CM1'),('CM2','CM2'),('CM3','CM3'),('CM4','CM4'),('CM5','CM5'),('CM6','CM6'),('CM7','CM7')]
    
    id = models.AutoField(primary_key=True)
    fecha = models.DateField(blank=True, null=True)
    finca = models.CharField(max_length=25,choices=op_finca,null=True)
    viaje = models.CharField(max_length=20, choices=op_viajes,null=True)
    encargado = models.CharField(max_length=30,choices=op_encargado,null=True)
    #orden = models.CharField(max_length=20,choices=op_orden,null=True)
    cultivo = models.CharField(max_length=45,choices=op_cultivo,null=True)
    variedad = models.CharField(max_length=40,choices=op_variedad,null=True)
    cajas = models.IntegerField(blank=True, null=True)
    correo = models.CharField(max_length=75, blank=True,choices=op_correo,null=True)
    #estructura=models.CharField(max_length=40,choices=op_estructura,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (str(self.finca)+ " | " + str(self.encargado) + " | " + str(self.viaje)+ " | " + str(self.cultivo))

class AcumFruta(models.Model):
    
    op_cultivo = [('CHERRY','CHERRY'),('MEDLEY','MEDLEY'),('GRAPE','GRAPE'),('GRAPE ORGANICO','GRAPE ORGANICO'),('CHERRY ORGANICO','CHERRY ORGANICO'),('BLOCKY','BLOCKY'),('BLOCKY ORGANICO','BLOCKY ORGANICO'),('MINI','MINI'),('MINI ORGANICO','MINI ORGANICO')]
    op_variedad = [('DUNNE','DUNNE'),('IVORINO','IVORINO'),('KM 5512','KM 5512'),('NEBULA','NEBULA'),('ROJO','ROJO'),('AMARILLO','AMARILLO'),('ANARANJADO','ANARANJADO')]
    op_finca = [('VALLE','VALLE'),('RIO','RIO'),('CIP','CIP'),('FLE','FLE'),('FLA','FLA')]
    op_correo = [('cosecha.rio@popoyan.com.gt','cosecha.rio@popoyan.com.gt')]
    op_orden = [('64202052','64202052'),('64206054','64206054'),('64206055','64206055'),('64206056','64206056')]
    op_estructura = [('CM1','CM1'),('CM2','CM2'),('CM3','CM3'),('CM4','CM4'),('CM5','CM5'),('CM6','CM6'),('CM7','CM7')]
    
    id = models.AutoField(primary_key=True)
    fecha = models.DateField(blank=True, null=True)
    finca = models.CharField(max_length=25,choices=op_finca,null=True)
    orden = models.CharField(max_length=20,choices=op_orden,null=True)
    cultivo = models.CharField(max_length=45,choices=op_cultivo,null=True)
    variedad = models.CharField(max_length=40,choices=op_variedad,null=True)
    cajas = models.IntegerField(blank=True, null=True)
    correo = models.CharField(max_length=75, blank=True,choices=op_correo,null=True)
    estructura=models.CharField(max_length=40,choices=op_estructura,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (str(self.finca)+ " | " + str(self.cultivo) + " | " + str(self.variedad)+ " | " + str(self.estructura))

class enviosFrutaPlantilla(models.Model):
    op_viajes = [('','-'),('Viaje 1','Viaje 1'),('Viaje 2','Viaje 2'),('Viaje 3', 'Viaje 3'),('Viaje 4','Viaje 4'),('Viaje 5','Viaje 5'),('Viaje 6','Viaje 6'),('Viaje 7','Viaje 7'),('Viaje 8','Viaje 8')]
    op_encargado = [('Brandon Portillo','Brandon Portillo'),('Isaías García','Isaías García')]
    op_cultivo = [('CHERRY','CHERRY'),('MEDLEY','MEDLEY'),('GRAPE','GRAPE'),('GRAPE ORGANICO','GRAPE ORGANICO'),('CHERRY ORGANICO','CHERRY ORGANICO'),('BLOCKY','BLOCKY'),('BLOCKY ORGANICO','BLOCKY ORGANICO'),('MINI','MINI'),('MINI ORGANICO','MINI ORGANICO')]
    op_finca = [('VALLE','VALLE'),('RIO','RIO'),('CIP','CIP'),('FLE','FLE'),('FLA','FLA')]
    op_correo = [('cosecha.rio@popoyan.com.gt','cosecha.rio@popoyan.com.gt')]
    op_orden = [('64202052','64202052'),('64206054','64206054'),('64206055','64206055'),('64206056','64206056')]
    op_estructura = [('CM1','CM1'),('CM2','CM2'),('CM3','CM3'),('CM4','CM4'),('CM5','CM5'),('CM6','CM6'),('CM7','CM7')]
    
    id = models.AutoField(primary_key=True)
    fecha = models.DateField(blank=True, null=True)
    finca = models.CharField(max_length=25,choices=op_finca,null=True)
    viaje = models.CharField(max_length=20, choices=op_viajes,null=True)
    encargado = models.CharField(max_length=30,choices=op_encargado,null=True)
    orden = models.CharField(max_length=20,choices=op_orden,null=True)
    cultivo = models.CharField(max_length=45,choices=op_cultivo,null=True)
    estructura=models.CharField(max_length=40,choices=op_estructura,null=True)
    cajas = models.IntegerField(blank=True, null=True)
    correo = models.CharField(max_length=75, blank=True,choices=op_correo,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (str(self.finca)+ " | " + str(self.cultivo) + " | " + str(self.viaje)+ " | " + str(self.estructura))


class cultivoxFinca(models.Model):
    
    op_cultivo = [('CHERRY','CHERRY'),('MEDLEY','MEDLEY'),('GRAPE','GRAPE'),('GRAPE ORGANICO','GRAPE ORGANICO'),('CHERRY ORGANICO','CHERRY ORGANICO'),('BLOCKY','BLOCKY'),('BLOCKY ORGANICO','BLOCKY ORGANICO'),('MINI','MINI'),('MINI ORGANICO','MINI ORGANICO')]
    op_variedad = [('BAMANO','BAMANO'),('DUNNE','DUNNE'),('IVORINO','IVORINO'),('KM 5512','KM 5512'),('NEBULA','NEBULA'),('ROJO','ROJO'),('AMARILLO','AMARILLO'),('ANARANJADO','ANARANJADO')]
    op_finca = [('VALLE','VALLE'),('RIO','RIO'),('CIP','CIP'),('FLE','FLE'),('FLA','FLA')]

    id = models.AutoField(primary_key=True)
    finca = models.CharField(max_length=25,choices=op_finca,null=True)
    cultivo = models.CharField(max_length=45,choices=op_cultivo,null=True)
    variedad = models.CharField(max_length=40,choices=op_variedad,null=True)

    def __str__(self):
        return (str(self.finca)+ " | " + str(self.cultivo) + " | " + str(self.variedad))
    
class Actpeso(models.Model):

    registro = models.BigAutoField(primary_key=True)
    recepcion = models.BigIntegerField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    llave = models.CharField(max_length=200, blank=True, null=True)
    finca = models.CharField(max_length=75, blank=True, null=True)
    tarimas = models.BigIntegerField(blank=True, null=True)
    cajas = models.BigIntegerField(blank=True, null=True)
    libras = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cultivo = models.CharField(max_length=50, blank=True, null=True)
    tipodecaja = models.CharField(max_length=85, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    variedad = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'actpeso'

class Boletas(models.Model):

    registro = models.BigAutoField(primary_key=True)
    recepcion = models.BigIntegerField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    finca = models.CharField(max_length=75, blank=True, null=True)
    orden = models.CharField(max_length=30, blank=True, null=True)
    estructura = models.CharField(max_length=50, blank=True, null=True)
    variedad = models.CharField(max_length=50, blank=True, null=True)
    proveedor = models.CharField(max_length=150, blank=True, null=True)
    cultivo = models.CharField(max_length=50, blank=True, null=True)
    calidad1 = models.CharField(max_length=200, blank=True, null=True)
    calidad = models.CharField(max_length=50, blank=True, null=True)
    cajas = models.BigIntegerField(blank=True, null=True)
    librasxcaja = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    libras = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True,blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'boletas'

class Ccalidad(models.Model):
    op_status2 = [('Pendiente','-'),('Inspeccionado','Inspeccionado')]

    registro = models.BigAutoField(primary_key=True)
    recepcion = models.BigIntegerField(blank=True, null=True)
    causarechazo = models.CharField(max_length=100, blank=True, null=True)
    porcentaje = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    llave = models.CharField(max_length=200, blank=True, null=True)
    status2 = models.CharField(max_length=25, choices=op_status2,blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    observaciones = models.CharField(max_length=125, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ccalidad'

class Recepciones(models.Model):
    op_status = [('Pendiente','-'),('En proceso','En proceso')]
    
    registro = models.BigAutoField(primary_key=True)
    recepcion = models.BigIntegerField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    llave = models.CharField(max_length=200, blank=True, null=True)
    finca = models.CharField(max_length=75, blank=True, null=True)
    variedad = models.CharField(max_length=50, blank=True, null=True)
    cajas = models.BigIntegerField(blank=True, null=True)
    libras = models.FloatField(blank=True, null=True)
    observaciones = models.CharField(max_length=125, blank=True, null=True)
    cultivo = models.CharField(max_length=50, blank=True, null=True)
    llave2 = models.CharField(max_length=200, blank=True, null=True)
    criterio = models.CharField(max_length=85, blank=True, null=True)
    status = models.CharField(max_length=25, choices=op_status,blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    classorigen = models.CharField(max_length=35, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)
    enviofruta = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recepciones'

class causasRechazo(models.Model):
    
    registro = models.BigAutoField(primary_key=True)
    causa = models.CharField(max_length=75, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)

    def __str__(self):
        return str(self.registro)

class inventarioProdTerm(models.Model):
    
    op_proveedor = [('','-'),('RIO','RIO'),('VALLE','VALLE'),('CIP','CIP'),('PASTORIA','PASTORIA')]
    op_cultivo = [('','-'),('CHERRY','CHERRY'),('MEDLEY','MEDLEY'),('GRAPE','GRAPE'),('GRAPE ORGANICO','GRAPE ORGANICO'),('CHERRY ORGANICO','CHERRY ORGANICO'),('BLOCKY','BLOCKY'),('BLOCKY ORGANICO','BLOCKY ORGANICO'),('MINI','MINI'),('MINI ORGANICO','MINI ORGANICO')]
    op_categoria = [('','-'),('Mastronardi','Mastronardi'),('Carreta','Carreta'),('Cenma','Cenma'),('Devolucion','Devolucion')]
    op_empaque = [('Cajas','Cajas'),('Libras','Libras')]
    registro = models.BigAutoField(primary_key=True)
    fecha = models.DateField(blank=True, null=True)
    categoria = models.CharField(max_length=50, choices=op_categoria, blank=True, null=True)
    cultivo = models.CharField(max_length=50, choices=op_cultivo, blank=True, null=True)
    proveedor = models.CharField(max_length=75, choices=op_proveedor,blank=True, null=True)
    empaque = models.CharField(max_length=75, choices=op_empaque,blank=True, null=True)
    calidad1 = models.CharField(max_length=200, blank=True, null=True)
    cantidad = models.BigIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)

    def __str__(self):
        return str(str(self.proveedor)+ " | " + str(self.calidad1))

class productoTerm(models.Model):
    op_cultivo = [('CHERRY','CHERRY'),('MEDLEY','MEDLEY'),('GRAPE','GRAPE'),('GRAPE ORGANICO','GRAPE ORGANICO'),('CHERRY ORGANICO','CHERRY ORGANICO'),('BLOCKY','BLOCKY'),('BLOCKY ORGANICO','BLOCKY ORGANICO'),('MINI','MINI'),('MINI ORGANICO','MINI ORGANICO')]
    op_categoria = [('Mastronardi','Mastronardi'),('Carreta','Carreta'),('Cenma','Cenma'),('Devolucion','Devolucion')]
    registro = models.BigAutoField(primary_key=True)
    cultivo = models.CharField(max_length=50, choices=op_cultivo, blank=True, null=True)
    calidad1 = models.CharField(max_length=200, blank=True, null=True)
    categoria = models.CharField(max_length=50, choices=op_categoria, blank=True, null=True)
    librasxcaja = models.FloatField(blank=True, null=True)
    tipo = models.CharField(max_length=50, choices=op_cultivo, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)

    def __str__(self):
        return str(str(self.cultivo)+ " | " + str(self.calidad1))

class tipoCajas(models.Model):
    registro = models.BigAutoField(primary_key=True)
    tcaja = models.CharField(max_length=75, blank=True, null=True)
    peso =  models.FloatField(blank=True, null=True)
    

    def __str__(self):
        return str(self.tcaja)

class productores(models.Model):
    registro = models.BigAutoField(primary_key=True)
    productor = models.CharField(max_length=75, blank=True, null=True)
    
    def __str__(self):
        return str(self.productor)

class cultivos(models.Model):
    registro = models.BigAutoField(primary_key=True)
    cultivo = models.CharField(max_length=75, blank=True, null=True)
    
    def __str__(self):
        return str(self.cultivo)
    
   
class detallerec(models.Model):
    op_status = [('Pendiente','-'),('En proceso','En proceso')]
    registro = models.BigAutoField(primary_key=True)
    recepcion = models.BigIntegerField(blank=True, null = True)
    fecha = models.DateField(blank=True, null=True)
    llave = models.CharField(max_length=200, blank = True, null = True)
    finca = models.CharField(max_length= 75, blank = True, null =  True)
    cajas = models.BigIntegerField(blank = True, null = True)
    libras = models.FloatField(blank=True, null = True)
    observaciones = models.CharField(max_length=125,blank=True, null = True)
    cultivo = models.CharField(max_length=50, blank = True, null = True)
    criterio = models.CharField(max_length=85, blank = True, null = True)
    status = models.CharField(max_length=25, choices=op_status,blank=True,null = True)
    created = models.DateTimeField(auto_now=True, blank=True,null = True)
    classorigen = models.CharField(max_length=35, blank= True, null = True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    enviofruta = models.BigIntegerField(blank=True, null=True)

