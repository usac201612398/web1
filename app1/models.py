# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class TCategorias(models.Model):
    categoría_código = models.AutoField(primary_key=True)
    categoría_centro = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_categorias'


class TCentros(models.Model):
    centro = models.CharField(primary_key=True, max_length=15)
    descripción = models.CharField(max_length=125, blank=True, null=True)
    categoría_código = models.ForeignKey(TCategorias, models.DO_NOTHING, db_column='categoría_código')
    responsable = models.CharField(max_length=50, blank=True, null=True)
    area_field = models.DecimalField(db_column='area_', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 't_centros'


class TDespachos(models.Model):
    pedido = models.AutoField(primary_key=True)
    mtemporal = models.DateTimeField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    envio = models.BigIntegerField(blank=True, null=True)
    origen = models.CharField(max_length=50, blank=True, null=True)
    rubro = models.CharField(max_length=15, blank=True, null=True)
    citem = models.CharField(max_length=15, blank=True, null=True)
    cantidad = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    ccentro = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_despachos'


class Ingresop(models.Model):
    id = models.BigAutoField(primary_key=True)
    codigop = models.BigIntegerField(blank=True, null=True)
    nombrep = models.CharField(max_length=50, blank=True, null=True)
    marcat = models.DateTimeField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    origen = models.CharField(max_length=30, blank=True, null=True)
    evento = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ingresop'


class Listapersonal(models.Model):
    id = models.BigAutoField(primary_key=True)
    codigop = models.BigIntegerField(blank=True, null=True)
    nombrep = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'listapersonal'
