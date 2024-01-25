from django.db import models

# Create your models here.
class Sensor(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=30)
    tipo = models.CharField(max_length=25)

    def __str__(self):
        return f'Sensor: {self.name} tipo: {self.tipo}'

class Measure(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    value = models.FloatField(default=0)
    sensor = models.ForeignKey(Sensor,on_delete=models.CASCADE)

    def __str__(self):
        return f'Medición: {self.value} | Sensor: {self.sensor.name}'
    
class MqttLog(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    message = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.message}'
    
class TCategorias(models.Model):
    categoría_código = models.BigAutoField(db_column='Categoría_Código', primary_key=True)  # Field name made lowercase.
    categoría_centro = models.CharField(db_column='Categoría_Centro', max_length=15, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 't_categorias'


class TCentros(models.Model):
    centro = models.CharField(db_column='Centro', primary_key=True, max_length=15)  # Field name made lowercase.
    descripción = models.CharField(db_column='Descripción', max_length=125, blank=True, null=True)  # Field name made lowercase.
    categoría_código = models.ForeignKey(TCategorias, models.DO_NOTHING, db_column='Categoría_Código', blank=True, null=True)  # Field name made lowercase.
    responsable = models.CharField(db_column='Responsable', max_length=50, blank=True, null=True)  # Field name made lowercase.
    area_field = models.FloatField(db_column='Area_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 't_centros'


class TDespachos(models.Model):
    pedido = models.BigAutoField(db_column='Pedido', primary_key=True)  # Field name made lowercase.
    mtemporal = models.DateTimeField(db_column='mTemporal', blank=True, null=True)  # Field name made lowercase.
    fecha = models.DateField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    envio = models.BigIntegerField(db_column='Envio', blank=True, null=True)  # Field name made lowercase.
    origen = models.CharField(db_column='Origen', max_length=50, blank=True, null=True)  # Field name made lowercase.
    rubro = models.CharField(db_column='Rubro', max_length=15, blank=True, null=True)  # Field name made lowercase.
    citem = models.CharField(db_column='cItem', max_length=15, blank=True, null=True)  # Field name made lowercase.
    cantidad = models.FloatField(blank=True, null=True)
    ccentro = models.CharField(db_column='cCentro', max_length=15, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 't_despachos'


class TItems(models.Model):
    código_articulo = models.CharField(db_column='Código_Articulo', primary_key=True, max_length=15)  # Field name made lowercase.
    artículo = models.CharField(db_column='Artículo', max_length=125, blank=True, null=True)  # Field name made lowercase.
    unidad_medida = models.CharField(db_column='Unidad_Medida', max_length=15, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 't_items'
    
