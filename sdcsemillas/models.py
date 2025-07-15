from django.db import models

# Create your models here.
# Lotes
class usuariosApp(models.Model):
    
    correo = models.CharField(primary_key=True,max_length=75, blank=True)
    encargado = models.CharField(max_length=30)
    codigoEvo = models.BigIntegerField(blank = True, null =  True)
    finca = models.CharField(max_length=30, blank = True, null =  True)
    
    def __str__(self):
        return (str(self.codigoEvo) + " | " + self.encargado)
    
class operariosApp(models.Model):

    id = models.BigAutoField(primary_key=True)
    codigo_empleado = models.CharField(max_length=75, blank=True)
    codigoEvo = models.BigIntegerField(blank = True, null =  True)
    nombre_operario = models.CharField(max_length=75, blank=True)
    codigo_lote = models.BigIntegerField(blank=True,null=True)
    supervisor = models.CharField(max_length=30)
    status = models.CharField(max_length= 30, blank = True, null =  True)
    
    def __str__(self):
        return (str(self.codigo_empleado) + " | " + self.nombre_operario)
    
class lotes(models.Model):
    #op_status = [('Pendiente','-'),('En proceso','En proceso'),('Cerrado','Cerrado')]
    id = models.BigAutoField(primary_key=True)
    lote_code = models.CharField(max_length= 50, blank = True, null =  True)
    variedad_code = models.CharField(max_length= 50, blank = True, null =  True)
   # variedad_name = models.CharField(max_length= 50, blank = True, null =  True)
    apodo_variedad = models.CharField(max_length= 50, blank = True, null =  True)
    cultivo = models.CharField(max_length= 50, blank = True, null =  True)
    ubicación = models.CharField(max_length= 50, blank = True, null =  True)
    estructura = models.CharField(max_length= 50, blank = True, null =  True)
    plantas_padre = models.FloatField(blank = True, null =  True)
    plantas_madre = models.FloatField(blank = True, null =  True)
    harvest_code = models.CharField(max_length= 50, blank = True, null =  True)
    status = models.CharField(max_length= 50, blank = True, null =  True)
    siembra_madre = models.DateField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    metodo_prod = models.CharField(max_length= 50, blank = True, null =  True)
    target = models.IntegerField(blank = True, null = True)
    surface = models.FloatField(blank = True, null = True)
    observaciones = models.CharField(max_length= 75, blank = True, null =  True)
    shipment_hub = models.CharField(max_length= 50, blank = True, null =  True)
    as_per_SDCMale = models.FloatField(blank = True, null =  True)
    as_per_SDCFemale = models.FloatField(blank = True, null =  True)

#Variedades
class variedades(models.Model):
    #op_status = [('Pendiente','-'),('En proceso','En proceso'),('Cerrado','Cerrado')]
    id = models.BigAutoField(primary_key=True)
    variedad_code = models.CharField(max_length= 50, blank = True, null =  True)
#    variedad_name = models.CharField(max_length= 50, blank = True, null =  True)
    apodo_variedad = models.CharField(max_length= 50, blank = True, null =  True)
    cultivo = models.CharField(max_length= 50, blank = True, null =  True)
    cod_padre = models.CharField(max_length= 50, blank = True, null =  True)
    cod_madre = models.CharField(max_length= 50, blank = True, null =  True)
    status = models.CharField(max_length= 50, blank = True, null =  True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

#Conteo de plantas al transplante, polinización, cosecha
class conteoplantas(models.Model):
    #op_status = [('Pendiente','-'),('En proceso','En proceso'),('Cerrado','Cerrado')]
    id = models.BigAutoField(primary_key=True)
    operario_name = models.CharField(max_length= 50, blank = True, null =  True)
    supervisor_name = models.CharField(max_length= 50, blank = True, null =  True)
    ubicacion_lote = models.CharField(max_length= 50, blank = True, null =  True)
    estructura = models.CharField(max_length= 50, blank = True, null =  True)
    apodo_variedad = models.CharField(max_length= 50, blank = True, null =  True)
    tipo_cultivo = models.CharField(max_length= 20, blank = True, null =  True)
    codigo_madre = models.CharField(max_length= 30, blank = True, null =  True)
    codigo_planta = models.CharField(max_length= 30, blank = True, null =  True)
    plantas_activas= models.IntegerField(blank = True, null = True)
    plantas_faltantes = models.IntegerField(blank = True, null = True)
    fecha = models.DateField(blank=True, null=True)
    camas_completas = models.IntegerField(blank = True, null = True)
    camas_incompletas = models.IntegerField(blank = True, null = True)
    cocosxcamaincompleta = models.IntegerField(blank = True, null = True)
    observaciones = models.CharField(max_length= 75, blank = True, null =  True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    evento = models.TextField(max_length= 30, blank = True, null =  True) #AL TRANSPLANTE, POLINIZADO Y COSECHA
    status = models.TextField(max_length= 30, blank = True, null =  True)

#Conteo de semillas 
class conteosemillas(models.Model):
    #op_status = [('Pendiente','-'),('En proceso','En proceso'),('Cerrado','Cerrado')]
    id = models.BigAutoField(primary_key=True)
    fecha = models.DateField(blank=True, null=True)
    supervisor_name = models.CharField(max_length= 50, blank = True, null =  True)
    operario_name = models.CharField(max_length= 50, blank = True, null =  True)
    ubicacion_lote = models.CharField(max_length= 50, blank = True, null =  True)
    estructura = models.CharField(max_length= 50, blank = True, null =  True)
    apodo_variedad = models.CharField(max_length= 50, blank = True, null =  True)
    tipo_cultivo = models.CharField(max_length= 20, blank = True, null =  True)
    cantidad_frutos = models.IntegerField(blank = True, null = True)
    semillasxfruto = models.IntegerField(blank = True, null = True)
    prom_semillasxfruto = models.FloatField(blank = True, null = True)
    nsemana = models.IntegerField(blank = True, null = True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    clasificacion = models.TextField(max_length= 75, blank = True, null =  True) #FRUTO MADURO / FRUTO VERDE
    observaciones = models.CharField(max_length= 75, blank = True, null =  True)
    status = models.TextField(max_length= 30, blank = True, null =  True)

#Conteo de frutos general
class conteofrutos(models.Model):
    #op_status = [('Pendiente','-'),('En proceso','En proceso'),('Cerrado','Cerrado')]
    id = models.BigAutoField(primary_key=True)
    fecha = models.DateField(blank=True, null=True)
    supervisor_name = models.CharField(max_length= 50, blank = True, null =  True)
    operario_name = models.CharField(max_length= 50, blank = True, null =  True)
    ubicacion_lote = models.CharField(max_length= 50, blank = True, null =  True)
    apodo_variedad = models.CharField(max_length= 50, blank = True, null =  True)
    tipo_cultivo = models.CharField(max_length= 20, blank = True, null =  True)

    prom_autopolinizados = models.FloatField(blank = True, null = True) # Frutos/planta
    prom_floresabiertas = models.FloatField(blank = True, null = True) # Frores/planta
    
    prom_polinizados = models.FloatField(blank = True, null = True) # Frutos/planta
    estructura = models.CharField(max_length= 50, blank = True, null =  True)
    prom_cama = models.FloatField(blank = True, null = True) # Frutos/planta
    prom_area = models.FloatField(blank = True, null = True) # Frutos/planta
    prom_general = models.FloatField(blank = True, null = True) # Frutos/planta
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    observaciones = models.CharField(max_length= 75, blank = True, null =  True)
    nsemana = models.IntegerField(blank = True, null = True)
    evento = models.TextField(max_length= 30, blank = True, null =  True) #AUTOPOLINIZADO, POST-POLINIZADO, GENERAL
    status = models.TextField(max_length= 30, blank = True, null =  True)

#Cosecha y polinización por lote proyecto-semillas
class etapasdelote(models.Model):
    #op_status = [('Pendiente','-'),('En proceso','En proceso'),('Cerrado','Cerrado')]
    id = models.BigAutoField(primary_key=True)
    fecha = models.DateField(blank=True, null=True)
    codigo_lote = models.BigIntegerField(blank=True, null=True)
    supervisor_name = models.CharField(max_length= 50, blank = True, null =  True)
    operario_name = models.CharField(max_length= 50, blank = True, null =  True)
    ubicacion_lote = models.CharField(max_length= 50, blank = True, null =  True)
    apodo_variedad = models.CharField(max_length= 50, blank = True, null =  True)
    tipo_cultivo = models.CharField(max_length= 20, blank = True, null =  True)
    codigo_madre = models.CharField(max_length= 30, blank = True, null =  True)
    codigo_padre = models.CharField(max_length= 30, blank = True, null =  True)
    status = models.CharField(max_length= 30, blank = True, null =  True) #Inicia y Termina
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    observaciones = models.CharField(max_length= 75, blank = True, null =  True)
    evento = models.CharField(max_length= 75, blank = True, null =  True) #Cosecha y polinización
    estructura = models.CharField(max_length= 50, blank = True, null =  True)

#Revisión de polen
class ccalidadpolen(models.Model):
    #op_status = [('Pendiente','-'),('En proceso','En proceso'),('Cerrado','Cerrado')]
    id = models.BigAutoField(primary_key=True)
    fecha = models.DateField(blank=True, null=True)
    supervisor_name = models.CharField(max_length= 50, blank = True, null =  True)
    operario_name = models.CharField(max_length= 50, blank = True, null =  True)
    ubicacion_lote = models.CharField(max_length= 50, blank = True, null =  True)
    apodo_variedad = models.CharField(max_length= 50, blank = True, null =  True)
    tipo_cultivo = models.CharField(max_length= 20, blank = True, null =  True)
    calidad = models.CharField(max_length= 30, blank = True, null =  True) #Calidad del polen (Buena, Mala)
    consistencia = models.CharField(max_length= 30, blank = True, null =  True) #Consistencia del polen (Normal, Grumosa)
    ag_externos = models.CharField(max_length= 30, blank = True, null =  True) #Agentes externos presentes en el polen (Insectos, Restos de vegetales, etc.)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    observaciones = models.CharField(max_length= 75, blank = True, null =  True)
    estructura = models.CharField(max_length= 50, blank = True, null =  True)
    status = models.CharField(max_length= 30, blank = True, null =  True)
    
#Registro de index de polinización
class indexpolinizacion(models.Model):
    #op_status = [('Pendiente','-'),('En proceso','En proceso'),('Cerrado','Cerrado')]
    id = models.BigAutoField(primary_key=True)
    fecha = models.DateField(blank=True, null=True)
    diasemana= models.CharField(max_length= 50, blank = True, null =  True)
    supervisor_name = models.CharField(max_length= 50, blank = True, null =  True)
    operario_name = models.CharField(max_length= 50, blank = True, null =  True)
    ubicacion_lote = models.CharField(max_length= 50, blank = True, null =  True)
    apodo_variedad = models.CharField(max_length= 50, blank = True, null =  True)
    tipo_cultivo = models.CharField(max_length= 20, blank = True, null =  True)
    color_lana= models.CharField(max_length= 20, blank = True, null =  True)
    cantidad_camas = models.IntegerField(blank = True, null = True)
    cantidad_index = models.IntegerField(blank = True, null = True) #Index por cama colocados
    promedio  = models.FloatField(blank = True, null = True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    observaciones = models.CharField(max_length= 75, blank = True, null =  True)
    status = models.CharField(max_length= 30, blank = True, null =  True)
    estructura = models.CharField(max_length= 50, blank = True, null =  True)

#Control de flores abiertas
class floresabiertas(models.Model):
    #op_status = [('Pendiente','-'),('En proceso','En proceso'),('Cerrado','Cerrado')]
    id = models.BigAutoField(primary_key=True)
    fecha = models.DateField(blank=True, null=True)
    diasemana= models.CharField(max_length= 50, blank = True, null =  True)
    supervisor_name = models.CharField(max_length= 50, blank = True, null =  True)
    operario_name = models.CharField(max_length= 50, blank = True, null =  True)
    ubicacion_lote = models.CharField(max_length= 50, blank = True, null =  True)
    apodo_variedad = models.CharField(max_length= 50, blank = True, null =  True)
    tipo_cultivo = models.CharField(max_length= 20, blank = True, null =  True)
    nsemana = models.IntegerField(blank = True, null = True)
    flores_abiertas = models.IntegerField(blank = True, null = True)
    flores_antenas = models.IntegerField(blank = True, null = True) #Index por caja
    flores_polinizadas = models.IntegerField(blank = True, null = True)
    flores_enmasculadas = models.IntegerField(blank = True, null = True) #Index por caja
    flores_sinpistilo =models.CharField(max_length= 20, blank = True, null =  True)
    flores_viejas = models.CharField(max_length= 20, blank = True, null =  True)
    lastimado  =models.CharField(max_length= 20, blank = True, null =  True)
    boton_pequeño = models.CharField(max_length= 20, blank = True, null =  True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    observaciones = models.CharField(max_length= 75, blank = True, null =  True)
    status = models.CharField(max_length= 30, blank = True, null =  True) 
    estructura = models.CharField(max_length= 50, blank = True, null =  True)

#Control de cosecha tomate y chile 
class controlcosecha(models.Model):
    #op_status = [('Pendiente','-'),('En proceso','En proceso'),('Cerrado','Cerrado')]
    id = models.BigAutoField(primary_key=True)
    fecha = models.DateField(blank=True, null=True)
    supervisor_name = models.CharField(max_length= 50, blank = True, null =  True)
    operario_name = models.CharField(max_length= 50, blank = True, null =  True)
    ubicacion_lote = models.CharField(max_length= 50, blank = True, null =  True)
    apodo_variedad = models.CharField(max_length= 50, blank = True, null =  True)
    tipo_cultivo = models.CharField(max_length= 20, blank = True, null =  True)
    cajas_revisadas = models.IntegerField(blank = True, null = True)
    frutos_autopol = models.IntegerField(blank = True, null = True) #frutos autopolinizados
    frutos_sinmarca = models.IntegerField(blank = True, null = True) #frutos sin marca
    frutos_sinlana = models.IntegerField(blank = True, null = True) #frutos sin lana
    frutos_fueratipo = models.IntegerField(blank = True, null = True) 
    llenado_caja =  models.CharField(max_length= 20, blank = True, null =  True) # Adecuado, Mejorar
    punto_maduracion =  models.CharField(max_length= 20, blank = True, null =  True) # Maduro, Camagua, Verde, Mezclado, Mala Maduración
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    observaciones = models.CharField(max_length= 75, blank = True, null =  True)
    status = models.CharField(max_length= 30, blank = True, null =  True)
    estructura = models.CharField(max_length= 50, blank = True, null =  True)