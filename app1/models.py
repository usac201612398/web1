# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class ingresoP(models.Model):
    
    codigoP = models.BigIntegerField(blank=True, null=True)
    nombreP = models.CharField(max_length=50)
    marcaT = models.DateTimeField()
    fecha = models.DateField(blank=True, null=True)
    origen = models.CharField(max_length=30)
    evento = models.CharField(max_length=20)

    class Meta:
        managed = True
        db_table = 't_ingresop'

class listaPersonal(models.Model):
    
    codigoP = models.BigIntegerField(blank=True, null=True)
    nombreP = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 't_listapersonal'

class App1Measure(models.Model):
    id = models.BigAutoField(primary_key=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    value = models.FloatField()
    sensor = models.ForeignKey('App1Sensor', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'app1_measure'


class App1Mqttlog(models.Model):
    id = models.BigAutoField(primary_key=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    message = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'app1_mqttlog'


class App1Sensor(models.Model):
    id = models.BigAutoField(primary_key=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    name = models.CharField(max_length=30)
    tipo = models.CharField(max_length=25)

    class Meta:
        managed = False
        db_table = 'app1_sensor'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class EjemploEjemplomedicion(models.Model):
    id = models.BigAutoField(primary_key=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    valor = models.FloatField()

    class Meta:
        managed = False
        db_table = 'ejemplo_ejemplomedicion'


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


class TItem(models.Model):
    código_articulo = models.CharField(primary_key=True, max_length=15)
    artículo = models.CharField(max_length=125, blank=True, null=True)
    unidad_medida = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_item'
