from django.db import models

# Create your models here.
class usuariosAppFruta(models.Model):
    
    correo = models.CharField(primary_key=True,max_length=75, blank=True)
    encargado = models.CharField(max_length=30)
    finca = models.CharField(max_length=25)
    
    def __str__(self):
        return (self.finca + " | " + self.encargado)

class proyecciones(models.Model):

    #op_finca = [('VALLE','VALLE'),('RIO','RIO'),('CIP', 'CIP'),('FLE','FLE'),('PRODUCTOS DEL VALLE, S.A.','PRODUCTOS DEL VALLE, S.A.')]
    #op_cultivo = [('AGUACATE','AGUACATE'),('PEPINO','PEPINO'),('CHERRY','CHERRY'),('ROMA','ROMA'),('MEDLEY','MEDLEY'),('BEEF','BEEF'),('SALADETTE','SALADETTE'),('GRAPE','GRAPE'),('GRAPE ORGANICO','GRAPE ORGANICO'),('CHERRY ORGANICO','CHERRY ORGANICO'),('BLOCKY','BLOCKY'),('BLOCKY ORGANICO','BLOCKY ORGANICO'),('MINI','MINI'),('MINI ORGANICO','MINI ORGANICO')]
    #op_status = [('Abierta','Abierta'),('Cerrada','Cerrada')]
    #op_temporada = [('Temp 2023-2024','Temp 2023-2024'),('Temp 2024-2025','Temp 2024-2025')]
    id = models.AutoField(primary_key=True)
    fecha = models.DateField(blank=True, null=True)
    semana = models.IntegerField(blank=True, null=True)
    año = models.IntegerField(blank=True, null=True)
    semanacosecha = models.IntegerField(blank=True, null=True)
    finca = models.CharField(max_length=25,blank=True)
    orden = models.CharField(max_length=30,blank=True)
    cultivo = models.CharField(max_length=35, blank=True)
    kgm2 = models.FloatField(blank=True, null=True)
    temporada = models.CharField(max_length=45,blank=True)
    status = models.CharField(max_length=35, blank=True)
    
    def __str__(self):
        return (str(self.semanacosecha) + " | " + str(self.orden)+ " | " + str(self.cultivo)+ " | " + str(self.finca) )
     
class datosProduccion(models.Model):

    #op_finca = [('VALLE','VALLE'),('RIO','RIO'),('CIP', 'CIP'),('FLE','FLE'),('PRODUCTOS DEL VALLE, S.A.','PRODUCTOS DEL VALLE, S.A.')]
    #op_cultivo = [('AGUACATE','AGUACATE'),('PEPINO','PEPINO'),('CHERRY','CHERRY'),('ROMA','ROMA'),('MEDLEY','MEDLEY'),('BEEF','BEEF'),('SALADETTE','SALADETTE'),('GRAPE','GRAPE'),('GRAPE ORGANICO','GRAPE ORGANICO'),('CHERRY ORGANICO','CHERRY ORGANICO'),('BLOCKY','BLOCKY'),('BLOCKY ORGANICO','BLOCKY ORGANICO'),('MINI','MINI'),('MINI ORGANICO','MINI ORGANICO')]
    #op_status = [('Abierta','Abierta'),('Cerrada','Cerrada')]
    #op_temporada = [('Temp 2023-2024','Temp 2023-2024'),('Temp 2024-2025','Temp 2024-2025')]
    id = models.AutoField(primary_key=True)
    finca = models.CharField(max_length=25,blank=True)
    orden = models.CharField(max_length=30,blank=True)
    cultivo = models.CharField(max_length=35, blank=True)
    area = models.FloatField(blank=True, null=True)
    temporada = models.CharField(max_length=45,blank=True)
    status = models.CharField(max_length=35, blank=True)
    
    def __str__(self):
        return (str(self.finca) + " | " + str(self.orden)+ " | " + str(self.temporada)+ " | " + str(self.status) )
    
class detallesProduccion(models.Model):

    #op_cultivo = [('CHERRY','CHERRY'),('AGUACATE','AGUACATE'),('PEPINO','PEPINO'),('ROMA','ROMA'),('MEDLEY','MEDLEY'),('BEEF','BEEF'),('SALADETTE','SALADETTE'),('GRAPE','GRAPE'),('GRAPE ORGANICO','GRAPE ORGANICO'),('CHERRY ORGANICO','CHERRY ORGANICO'),('BLOCKY','BLOCKY'),('BLOCKY ORGANICO','BLOCKY ORGANICO'),('MINI','MINI'),('MINI ORGANICO','MINI ORGANICO')]
    
    id = models.AutoField(primary_key=True)
    cultivo = models.CharField(max_length=35, blank=True)
    variedad = models.CharField(max_length=35, blank=True)
    
    def __str__(self):
        return (str(self.cultivo) + " | " + str(self.variedad) )
    
class detallesEstructuras(models.Model):

    #op_cultivo = [('CHERRY','CHERRY'),('PEPINO','PEPINO'),('AGUACATE','AGUACATE'),('ROMA','ROMA'),('MEDLEY','MEDLEY'),('BEEF','BEEF'),('SALADETTE','SALADETTE'),('GRAPE','GRAPE'),('GRAPE ORGANICO','GRAPE ORGANICO'),('CHERRY ORGANICO','CHERRY ORGANICO'),('BLOCKY','BLOCKY'),('BLOCKY ORGANICO','BLOCKY ORGANICO'),('MINI','MINI'),('MINI ORGANICO','MINI ORGANICO')]
    #op_estructura = [('CM1','CM1'),('FLE','FLE'),('MODULOS','MODULOS'),('CM2','CM2'),('CM3','CM3'),('CM4','CM4'),('CM5','CM5'),('CM6','CM6'),('CM6A','CM6A'),('CM6B','CM6B'),('CM7','CM7'),('INV1','INV1'),('INV2','INV2'),('CM8','CM8')]
    #op_finca =  [('RIO','RIO'),('VALLE','VALLE'),('FLE','FLE'),('CIP','CIP'),('PRODUCTOS DEL VALLE, S.A.','PRODUCTOS DEL VALLE, S.A.')]
    #op_variedad = [('TOMATAZO','TOMATAZO'),('P52','P52'),('KRASHIF','KRASHIF'),('DELTASTAR','DELTASTAR'),('HASS','HASS'),('TYRAL','TYRAL'),('HATENO','HATENO'),('SICYBELLE','SICYBELLE'),('EMYELLE','EMYELLE'),('ADORELLE','ADORELLE'),('CRYSTELLE','CRYSTELLE'),('LEE PETIT','LEE PETIT'),('LUAN','LUAN'),('FLAVUS','FLAVUS'),('LUMMEN','LUMMEN'),('ALANI','ALANI'),('T311457R','T311457R'),('319384','319384'),('CASCADE','CASCADE'),('EXTRADENA','EXTRADENA'),('TL152633','TL152633'),('TL162715','TL152715'),('8B16453','8B16453'),('8B19B091','8B19B091'),('DIONISIO','DIONISIO'),('TORERO','TORERO'),('VINCITORI','VINCITORI'),('MONTELIMAR','MONTELIMAR'),('SWEET MAX','SWEET MAX'),('PICOLO','PICOLO'),('HYRULE','HYRULE'),('DORMA','DORMA'),('BAMANO','BAMANO'),('TT 764','TT 764'),('TT 864','TT 864'),('CHOCOSTAR','CHOCOSTAR'),('DUNNE','DUNNE'),('IVORINO','IVORINO'),('KM 5512','KM 5512'),('NEBULA','NEBULA'),('ROJO','ROJO'),('AMARILLO','AMARILLO'),('ANARANJADO','ANARANJADO')]
    #op_encargado = [('Vicente Martin','Vicente Martin'),('Brandon Portillo','Brandon Portillo'),('Carlos Hernández','Carlos Hernández'),('Nolberto Morales','Nolberto Morales'),('Rita Florian','Rita Florian'),('Ariel Parada','Ariel Parada')]
    
    id = models.AutoField(primary_key=True)
    finca = models.CharField(max_length=35, blank=True)
    orden = models.CharField(max_length=30,blank=True)
    cultivo = models.CharField(max_length=35, blank=True)
    estructura = models.CharField(max_length=35, blank=True)
    area =  models.FloatField(blank=True, null=True)
    variedad = models.CharField(max_length=40,blank=True)
    encargado = models.CharField(max_length=40, blank=True)

    def __str__(self):
        return (str(self.finca) + " | " + str(self.orden) + " | " + str(self.estructura) + " | " + str(self.variedad)  )

class AcumFruta(models.Model):
    
    #op_cultivo = [('ROMA','ROMA'),('PEPINO','PEPINO'),('AGUACATE','AGUACATE'),('ARANDANO','ARANDANO'),('CHERRY','CHERRY'),('MEDLEY','MEDLEY'),('BEEF','BEEF'),('SALADETTE','SALADETTE'),('GRAPE','GRAPE'),('GRAPE ORGANICO','GRAPE ORGANICO'),('CHERRY ORGANICO','CHERRY ORGANICO'),('BLOCKY','BLOCKY'),('BLOCKY ORGANICO','BLOCKY ORGANICO'),('MINI','MINI'),('MINI ORGANICO','MINI ORGANICO')]
    #op_variedad = [('HASS','HASS'),('P52','P52'),('KRASHIF','KRASHIF'),('DELTASTAR','DELTASTAR'),('BILOXI','BILOXI'),('TOMATAZO','TOMATAZO'),('TYRAL','TYRAL'),('HATENO','HATENO'),('SICYBELLE','SICYBELLE'),('EMYELLE','EMYELLE'),('ADORELLE','ADORELLE'),('CRYSTELLE','CRYSTELLE'),('LEE PETIT','LEE PETIT'),('LUAN','LUAN'),('FLAVUS','FLAVUS'),('LUMMEN','LUMMEN'),('ALANI','ALANI'),('T311457R','T311457R'),('319384','319384'),('CASCADE','CASCADE'),('EXTRADENA','EXTRADENA'),('TL152633','TL152633'),('TL162715','TL152715'),('8B16453','8B16453'),('8B19B091','8B19B091'),('DIONISIO','DIONISIO'),('TORERO','TORERO'),('VINCITORI','VINCITORI'),('MONTELIMAR','MONTELIMAR'),('SWEET MAX','SWEET MAX'),('PICOLO','PICOLO'),('HYRULE','HYRULE'),('DORMA','DORMA'),('BAMANO','BAMANO'),('TT 764','TT 764'),('TT 864','TT 864'),('CHOCOSTAR','CHOCOSTAR'),('DUNNE','DUNNE'),('IVORINO','IVORINO'),('KM 5512','KM 5512'),('NEBULA','NEBULA'),('ROJO','ROJO'),('AMARILLO','AMARILLO'),('ANARANJADO','ANARANJADO')]
    #op_finca = [('VALLE','VALLE'),('RIO','RIO'),('CIP','CIP'),('FLE','FLE'),('FLA','FLA'),('PRODUCTOS DEL VALLE, S.A.','PRODUCTOS DEL VALLE, S.A.'),]
    #op_correo = [('otroscultivos@popoyan.com.gt','otroscultivos@popoyan.com.gt'),('cosecha.cip@popoyan.com.gt','cosecha.cip@popoyan.com.gt'),('cosecha.rio@popoyan.com.gt','cosecha.rio@popoyan.com.gt'),('provalle@popoyan.com.gt','provalle@popoyan.com.gt'),('cosecha.valle@popoyan.com.gt','cosecha.valle@popoyan.com.gt'),('cosecha.valle2@popoyan.com.gt','cosecha.valle2@popoyan.com.gt')]
    #op_orden = [('PCIPT20242025','PCIPT20242025'),('64204019','64204019'),('60200040','60200040'),('64200000','64200000'),('310100052','310100052'),('60000019','60000019'),('60000020','60000020'),('PCIPB20242025','PCIPB20242025'),('PCIPMINI20242025','PCIPMINI20242025'),('PT20242025','PT20242025'),('PP20242025','PP20242025'),('60200039','60200039'),('64202052','64202052'),('64202053','64202053'),('64202052','64202052'),('64206054','64206054'),('64206055','64206055'),('64206056','64206056'),('64202048','64202048'),('64202049','64202049'),('64202050','64202050'),('64202051','64202051')]
    #op_estructura = [('PASTORIA','PASTORIA'),('PARCELA','PARCELA'),('FASE 4','FASE 4'),('PANTE 10','PANTE 10'),('FASE 3','FASE 3'),('FASE 3.1','FASE 3.1'),('FASE 1','FASE 1'),('FASE 2','FASE 2'),('FASE 5','FASE 5.1'),('FASE 5.1','FASE 5.1'),('CM1','CM1'),('FLE','FLE'),('MODULOS','MODULOS'),('CM2','CM2'),('CM3','CM3'),('CM4','CM4'),('CM5','CM5'),('CM6','CM6'),('CM6A','CM6A'),('CM6B','CM6B'),('CM7','CM7'),('INV1','INV1'),('INV2','INV2'),('CM8','CM8')]
    #op_status = [('Pendiente','-'),('Cargado','Cargado')]

    id = models.AutoField(primary_key=True)
    fecha = models.DateField(blank=True, null=True)
    finca = models.CharField(max_length=50,blank=True,null=True)
    orden = models.CharField(max_length=20,blank=True,null=True)
    cultivo = models.CharField(max_length=45,blank=True,null=True)
    variedad = models.CharField(max_length=40,blank=True,null=True)
    cajas = models.IntegerField(blank=True, null=True)
    correo = models.CharField(max_length=75, blank=True,null=True)
    encargado = models.CharField(max_length=30,blank=True, null=True)
    estructura=models.CharField(max_length=40,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    libras = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=25, blank=True, null=True)
    op_sap = models.CharField(max_length=20,blank=True, null=True)
    recepcion = models.BigIntegerField(blank=True, null=True)
    viaje = models.CharField(max_length=30,null=True,blank=True)
    nsalidafruta = models.BigIntegerField(blank=True, null=True)

    def __str__(self):
        return (str(self.id) + " | " + str(self.fecha) + " | " + str(self.finca)+ " | " + str(self.cultivo) + " | " + str(self.variedad)+ " | " + str(self.estructura)+ " | " + str(self.viaje))

class AcumFrutaaux(models.Model):
    
    #op_cultivo = [('ROMA','ROMA'),('PEPINO','PEPINO'),('AGUACATE','AGUACATE'),('ARANDANO','ARANDANO'),('CHERRY','CHERRY'),('MEDLEY','MEDLEY'),('BEEF','BEEF'),('SALADETTE','SALADETTE'),('GRAPE','GRAPE'),('GRAPE ORGANICO','GRAPE ORGANICO'),('CHERRY ORGANICO','CHERRY ORGANICO'),('BLOCKY','BLOCKY'),('BLOCKY ORGANICO','BLOCKY ORGANICO'),('MINI','MINI'),('MINI ORGANICO','MINI ORGANICO')]
    #op_variedad = [('HASS','HASS'),('P52','P52'),('KRASHIF','KRASHIF'),('DELTASTAR','DELTASTAR'),('BILOXI','BILOXI'),('TOMATAZO','TOMATAZO'),('TYRAL','TYRAL'),('HATENO','HATENO'),('SICYBELLE','SICYBELLE'),('EMYELLE','EMYELLE'),('ADORELLE','ADORELLE'),('CRYSTELLE','CRYSTELLE'),('LEE PETIT','LEE PETIT'),('LUAN','LUAN'),('FLAVUS','FLAVUS'),('LUMMEN','LUMMEN'),('ALANI','ALANI'),('T311457R','T311457R'),('319384','319384'),('CASCADE','CASCADE'),('EXTRADENA','EXTRADENA'),('TL152633','TL152633'),('TL162715','TL152715'),('8B16453','8B16453'),('8B19B091','8B19B091'),('DIONISIO','DIONISIO'),('TORERO','TORERO'),('VINCITORI','VINCITORI'),('MONTELIMAR','MONTELIMAR'),('SWEET MAX','SWEET MAX'),('PICOLO','PICOLO'),('HYRULE','HYRULE'),('DORMA','DORMA'),('BAMANO','BAMANO'),('TT 764','TT 764'),('TT 864','TT 864'),('CHOCOSTAR','CHOCOSTAR'),('DUNNE','DUNNE'),('IVORINO','IVORINO'),('KM 5512','KM 5512'),('NEBULA','NEBULA'),('ROJO','ROJO'),('AMARILLO','AMARILLO'),('ANARANJADO','ANARANJADO')]
    #op_finca = [('VALLE','VALLE'),('RIO','RIO'),('CIP','CIP'),('FLE','FLE'),('FLA','FLA'),('PRODUCTOS DEL VALLE, S.A.','PRODUCTOS DEL VALLE, S.A.'),]
    #op_correo = [('otroscultivos@popoyan.com.gt','otroscultivos@popoyan.com.gt'),('cosecha.cip@popoyan.com.gt','cosecha.cip@popoyan.com.gt'),('cosecha.rio@popoyan.com.gt','cosecha.rio@popoyan.com.gt'),('provalle@popoyan.com.gt','provalle@popoyan.com.gt'),('cosecha.valle@popoyan.com.gt','cosecha.valle@popoyan.com.gt'),('cosecha.valle2@popoyan.com.gt','cosecha.valle2@popoyan.com.gt')]
    #op_orden = [('PCIPT20242025','PCIPT20242025'),('64204019','64204019'),('60200040','60200040'),('64200000','64200000'),('310100052','310100052'),('60000019','60000019'),('60000020','60000020'),('PCIPB20242025','PCIPB20242025'),('PCIPMINI20242025','PCIPMINI20242025'),('PT20242025','PT20242025'),('PP20242025','PP20242025'),('60200039','60200039'),('64202052','64202052'),('64202053','64202053'),('64202052','64202052'),('64206054','64206054'),('64206055','64206055'),('64206056','64206056'),('64202048','64202048'),('64202049','64202049'),('64202050','64202050'),('64202051','64202051')]
    #op_estructura = [('PASTORIA','PASTORIA'),('PARCELA','PARCELA'),('FASE 4','FASE 4'),('PANTE 10','PANTE 10'),('FASE 3','FASE 3'),('FASE 3.1','FASE 3.1'),('FASE 1','FASE 1'),('FASE 2','FASE 2'),('FASE 5','FASE 5.1'),('FASE 5.1','FASE 5.1'),('CM1','CM1'),('FLE','FLE'),('MODULOS','MODULOS'),('CM2','CM2'),('CM3','CM3'),('CM4','CM4'),('CM5','CM5'),('CM6','CM6'),('CM6A','CM6A'),('CM6B','CM6B'),('CM7','CM7'),('INV1','INV1'),('INV2','INV2'),('CM8','CM8')]
    #op_status = [('Pendiente','-'),('Cargado','Cargado')]

    id = models.AutoField(primary_key=True)
    acumfrutaid = models.BigIntegerField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    finca = models.CharField(max_length=50,blank=True,null=True)
    orden = models.CharField(max_length=20,blank=True,null=True)
    cultivo = models.CharField(max_length=45,blank=True,null=True)
    variedad = models.CharField(max_length=40,blank=True,null=True)
    cajas = models.IntegerField(blank=True, null=True)
    correo = models.CharField(max_length=75, blank=True,null=True)
    estructura=models.CharField(max_length=40,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    libras = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=25, blank=True, null=True)
    op_sap = models.CharField(max_length=20,blank=True, null=True)
    recepcion = models.BigIntegerField(blank=True, null=True)
    viaje = models.CharField(max_length=30,null=True,blank=True)
    nsalidafruta = models.BigIntegerField(blank=True, null=True)
    boleta = models.BigIntegerField(blank=True, null=True)
    encargado = models.CharField(max_length=30,blank=True, null=True)

    def __str__(self):
        return (str(self.id) + " | " + str(self.fecha) + " | " + str(self.finca)+ " | " + str(self.cultivo) + " | " + str(self.variedad)+ " | " + str(self.estructura)+ " | " + str(self.viaje))

class salidasFruta(models.Model):

    #op_viajes = [('','-'),('Viaje 1','Viaje 1'),('Viaje 2','Viaje 2'),('Viaje 3', 'Viaje 3'),('Viaje 4','Viaje 4'),('Viaje 5','Viaje 5'),('Viaje 6','Viaje 6'),('Viaje 7','Viaje 7'),('Viaje 8','Viaje 8'),('Viaje 9','Viaje 9'),('Viaje 10','Viaje 10')]
    #op_cultivo = [('ROMA','ROMA'),('PEPINO','PEPINO'),('AGUACATE','AGUACATE'),('CHERRY','CHERRY'),('MEDLEY','MEDLEY'),('BEEF','BEEF'),('SALADETTE','SALADETTE'),('GRAPE','GRAPE'),('GRAPE ORGANICO','GRAPE ORGANICO'),('CHERRY ORGANICO','CHERRY ORGANICO'),('BLOCKY','BLOCKY'),('BLOCKY ORGANICO','BLOCKY ORGANICO'),('MINI','MINI'),('MINI ORGANICO','MINI ORGANICO')]
    #op_variedad = [('TOMATAZO','TOMATAZO'),('P52','P52'),('HASS','HASS'),('KRASHIF','KRASHIF'),('DELTASTAR','DELTASTAR'),('TYRAL','TYRAL'),('HATENO','HATENO'),('SICYBELLE','SICYBELLE'),('EMYELLE','EMYELLE'),('ADORELLE','ADORELLE'),('CRYSTELLE','CRYSTELLE'),('LEE PETIT','LEE PETIT'),('LUAN','LUAN'),('FLAVUS','FLAVUS'),('LUMMEN','LUMMEN'),('ALANI','ALANI'),('T311457R','T311457R'),('319384','319384'),('CASCADE','CASCADE'),('EXTRADENA','EXTRADENA'),('TL152633','TL152633'),('TL162715','TL152715'),('8B16453','8B16453'),('8B19B091','8B19B091'),('DIONISIO','DIONISIO'),('TORERO','TORERO'),('VINCITORI','VINCITORI'),('MONTELIMAR','MONTELIMAR'),('SWEET MAX','SWEET MAX'),('PICOLO','PICOLO'),('HYRULE','HYRULE'),('DORMA','DORMA'),('BAMANO','BAMANO'),('TT 764','TT 764'),('TT 864','TT 864'),('CHOCOSTAR','CHOCOSTAR'),('DUNNE','DUNNE'),('IVORINO','IVORINO'),('KM 5512','KM 5512'),('NEBULA','NEBULA'),('ROJO','ROJO'),('AMARILLO','AMARILLO'),('ANARANJADO','ANARANJADO')]
    #op_encargado = [('Brandon Portillo','Brandon Portillo'),('Vicente Martin','Vicente Martin'),('Ariel Parada','Ariel Parada'),('Carlos Hernández','Carlos Hernández'),('Rita Florian','Rita Florian'),('Nolberto Morales','Nolberto Morales')]
    #op_finca = [('VALLE','VALLE'),('RIO','RIO'),('FLE','FLE'),('CIP','CIP'),('FLE','FLE'),('FLA','FLA'),('PRODUCTOS DEL VALLE, S.A.','PRODUCTOS DEL VALLE, S.A.')]
    #op_correo = [('cosecha.cip@popoyan.com.gt','cosecha.cip@popoyan.com.gt'),('cosecha.rio@popoyan.com.gt','cosecha.rio@popoyan.com.gt'),('provalle@popoyan.com.gt','provalle@popoyan.com.gt'),('cosecha.valle@popoyan.com.gt','cosecha.valle@popoyan.com.gt'),('cosecha.valle2@popoyan.com.gt','cosecha.valle2@popoyan.com.gt')]
    #op_orden = [('PCIPT20242025','PCIPT20242025'),('60000019','60000019'),('64204019','64204019'),('60200040','60200040'),('64202053','64202053'),('60000020','60000020'),('PCIPB20242025','PCIPB20242025'),('PCIPMINI20242025','PCIPMINI20242025'),('PT20242025','PT20242025'),('PP20242025','PP20242025'),('64202052','64202052'),('60200039','60200039'),('64206054','64206054'),('64206055','64206055'),('64206056','64206056'),('64202048','64202048'),('64202049','64202049'),('64202050','64202050'),('64202051','64202051')]
    #op_estructura = [('CM1','CM1'),('FLE','FLE'),('MODULOS','MODULOS'),('CM2','CM2'),('CM3','CM3'),('CM4','CM4'),('CM5','CM5'),('CM6','CM6'),('CM6A','CM6A'),('CM6B','CM6B'),('CM7','CM7'),('INV1','INV1'),('INV2','INV2'),('CM8','CM8')]
    #op_status = [('Pendiente','-'),('Cerrado','Cerrado')]
    #acumFruta = models.ForeignKey(AcumFruta, null=True, blank=True, on_delete=models.CASCADE)

    id = models.AutoField(primary_key=True)
    fecha = models.DateField(blank=True, null=True)
    finca = models.CharField(max_length=25,null=True)
    viaje = models.CharField(max_length=20, blank=True, null=True)
    encargado = models.CharField(max_length=30,blank=True, null=True)
    cultivo = models.CharField(max_length=45, blank=True, null=True)
    variedad = models.CharField(max_length=40, blank=True, null=True)
    cajas = models.IntegerField(blank=True, null=True)
    orden = models.CharField(max_length=20, blank=True, null=True)
    libras = models.FloatField(blank=True, null=True)
    recepcion = models.BigIntegerField(blank=True, null=True)
    correo = models.CharField(max_length=75, blank=True,  null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return (str(self.id)+ " | " + str(self.fecha) + " | " + str(self.finca)+ " | " + str(self.encargado) + " | " + str(self.viaje)+ " | " + str(self.cultivo)+ " | " + str(self.variedad))

class enviosFrutaPlantilla(models.Model):
    #op_viajes = [('','-'),('Viaje 1','Viaje 1'),('Viaje 2','Viaje 2'),('Viaje 3', 'Viaje 3'),('Viaje 4','Viaje 4'),('Viaje 5','Viaje 5'),('Viaje 6','Viaje 6'),('Viaje 7','Viaje 7'),('Viaje 8','Viaje 8')]
    #op_encargado = [('Brandon Portillo','Brandon Portillo'),('Vicente Martin','Vicente Martin'),('Ariel Parada','Ariel Parada'),('Carlos Hernández','Carlos Hernández'),('Nolberto Morales','Nolberto Morales'),('Rita Florian','Rita Florian')]
    #op_cultivo = [('ROMA','ROMA'),('CHERRY','CHERRY'),('AGUACATE','AGUACATE'),('PEPINO','PEPINO'),('MEDLEY','MEDLEY'),('SICYBELLE','SICYBELLE'),('EMYELLE','EMYELLE'),('ADORELLE','ADORELLE'),('CRYSTELLE','CRYSTELLE'),('LEE PETIT','LEE PETIT'),('LUAN','LUAN'),('FLAVUS','FLAVUS'),('LUMMEN','LUMMEN'),('ALANI','ALANI'),('ALANI','ALANI'),('T311457R','T311457R'),('319384','319384'),('CASCADE','CASCADE'),('EXTRADENA','EXTRADENA'),('TL152633','TL152633'),('TL162715','TL152715'),('TL162715','TL152715'),('8B19B091','8B19B091'),('DIONISIO','DIONISIO'),('TORERO','TORERO'),('VINCITORI','VINCITORI'),('MONTELIMAR','MONTELIMAR'),('BEEF','BEEF'),('SALADETTE','SALADETTE'),('GRAPE','GRAPE'),('GRAPE ORGANICO','GRAPE ORGANICO'),('CHERRY ORGANICO','CHERRY ORGANICO'),('BLOCKY','BLOCKY'),('BLOCKY ORGANICO','BLOCKY ORGANICO'),('MINI','MINI'),('MINI ORGANICO','MINI ORGANICO')]
    #op_finca = [('VALLE','VALLE'),('RIO','RIO'),('CIP','CIP'),('FLE','FLE'),('FLA','FLA'),('PRODUCTOS DEL VALLE, S.A.','PRODUCTOS DEL VALLE, S.A.')]
    #op_correo = [('cosecha.cip@popoyan.com.gt','cosecha.cip@popoyan.com.gt'),('cosecha.rio@popoyan.com.gt','cosecha.rio@popoyan.com.gt'),('provalle@popoyan.com.gt','provalle@popoyan.com.gt'),('cosecha.valle@popoyan.com.gt','cosecha.valle@popoyan.com.gt'),('cosecha.valle2@popoyan.com.gt','cosecha.valle2@popoyan.com.gt')]
    #op_orden = [('PCIPT20242025','PCIPT20242025'),('60000019','60000019'),('60200040','60200040'),('64204019','64204019'),('60000020','60000020'),('PCIPB20242025','PCIPB20242025'),('PCIPMINI20242025','PCIPMINI20242025'),('60200039','60200039'),('64202052','64202052'),('PT20242025','PT20242025'),('PP20242025','PP20242025'),('64206054','64206054'),('64206055','64206055'),('64206056','64206056'),('64202048','64202048'),('64202049','64202049'),('64202050','64202050'),('64202051','64202051')]
    #op_estructura = [('CM1','CM1'),('FLE','FLE'),('MODULOS','MODULOS'),('CM2','CM2'),('CM3','CM3'),('CM4','CM4'),('CM5','CM5'),('CM6','CM6'),('CM6A','CM6A'),('CM6B','CM6B'),('CM7','CM7'),('INV1','INV1'),('INV2','INV2'),('CM8','CM8')]
    
    id = models.AutoField(primary_key=True)
    fecha = models.DateField(blank=True, null=True)
    finca = models.CharField(max_length=25,null=True)
    viaje = models.CharField(max_length=20, null=True)
    encargado = models.CharField(max_length=30,null=True)
    orden = models.CharField(max_length=20,null=True)
    cultivo = models.CharField(max_length=45,null=True)
    estructura=models.CharField(max_length=40,null=True)
    cajas = models.IntegerField(blank=True, null=True)
    correo = models.CharField(max_length=75, blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return (str(self.finca)+ " | " + str(self.cultivo) + " | " + str(self.viaje)+ " | " + str(self.estructura))


class cultivoxFinca(models.Model):
    
    #op_cultivo = [('ROMA','ROMA'),('AGUACATE','AGUACATE'),('PEPINO','PEPINO'),('CHERRY','CHERRY'),('MEDLEY','MEDLEY'),('BEEF','BEEF'),('SALADETTE','SALADETTE'),('GRAPE','GRAPE'),('GRAPE ORGANICO','GRAPE ORGANICO'),('CHERRY ORGANICO','CHERRY ORGANICO'),('BLOCKY','BLOCKY'),('BLOCKY ORGANICO','BLOCKY ORGANICO'),('MINI','MINI'),('MINI ORGANICO','MINI ORGANICO')]
    #op_variedad = [('TOMATAZO','TOMATAZO'),('KRASHIF','KRASHIF'),('DELTASTAR','DELTASTAR'),('TYRAL','TYRAL'),('HASS','HASS'),('HATENO','HATENO'),('SICYBELLE','SICYBELLE'),('EMYELLE','EMYELLE'),('ADORELLE','ADORELLE'),('CRYSTELLE','CRYSTELLE'),('LEE PETIT','LEE PETIT'),('LUAN','LUAN'),('FLAVUS','FLAVUS'),('LUMMEN','LUMMEN'),('ALANI','ALANI'),('T311457R','T311457R'),('319384','319384'),('CASCADE','CASCADE'),('EXTRADENA','EXTRADENA'),('TL152633','TL152633'),('TL162715','TL152715'),('8B16453','8B16453'),('8B19B091','8B19B091'),('DIONISIO','DIONISIO'),('TORERO','TORERO'),('VINCITORI','VINCITORI'),('MONTELIMAR','MONTELIMAR'),('SWEET MAX','SWEET MAX'),('PICOLO','PICOLO'),('HYRULE','HYRULE'),('DORMA','DORMA'),('BAMANO','BAMANO'),('TT 764','TT 764'),('TT 864','TT 864'),('CHOCOSTAR','CHOCOSTAR'),('DUNNE','DUNNE'),('IVORINO','IVORINO'),('KM 5512','KM 5512'),('NEBULA','NEBULA'),('ROJO','ROJO'),('AMARILLO','AMARILLO'),('ANARANJADO','ANARANJADO')]
    #op_finca = [('VALLE','VALLE'),('RIO','RIO'),('CIP','CIP'),('FLE','FLE'),('FLA','FLA'),('PRODUCTOS DEL VALLE, S.A.','PRODUCTOS DEL VALLE, S.A.')]

    id = models.AutoField(primary_key=True)
    finca = models.CharField(max_length=25,null=True)
    cultivo = models.CharField(max_length=45,null=True)
    variedad = models.CharField(max_length=40,null=True)

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
    libras = models.FloatField(blank=True, null=True)
    cultivo = models.CharField(max_length=50, blank=True, null=True)
    tipodecaja = models.CharField(max_length=85, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    viaje = models.CharField(max_length=30, blank=True, null=True)
    encargado = models.CharField(max_length=50, blank=True, null=True)
    variedad = models.CharField(max_length=30, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    fechasalidafruta = models.DateField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'actpeso'

class Boletas(models.Model):

    #op_status = [('Pendiente','-'),('Cerrado','Cerrado')]
    registro = models.BigAutoField(primary_key=True)
    boleta = models.BigIntegerField(blank=True, null=True)
    idcontable = models.BigIntegerField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    finca = models.CharField(max_length=75, blank=True, null=True)
    orden = models.CharField(max_length=30, blank=True, null=True)
    proveedor = models.CharField(max_length=150, blank=True, null=True)
    cultivo = models.CharField(max_length=50, blank=True, null=True)
    calidad1 = models.CharField(max_length=200, blank=True, null=True)
    itemsapcode = models.CharField(max_length=30, blank=True, null=True)
    itemsapname= models.CharField(max_length=125, blank=True, null=True)
    calidad = models.CharField(max_length=50, blank=True, null=True)
    cajas = models.BigIntegerField(blank=True, null=True)
    librasxcaja = models.FloatField(blank=True, null=True)
    libras = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=25, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    ordenfinca = models.CharField(max_length=30, blank=True, null=True)
    opsap = models.CharField(max_length=20, blank=True, null=True)
    categoria = models.CharField(max_length=30, blank=True, null=True)
    idpedido = models.BigIntegerField(blank=True, null=True)
    itemsapcodelibra = models.CharField(max_length=30, blank=True, null=True)
    emisiones = models.CharField(max_length=30, blank=True, null=True)
    comentario = models.CharField(max_length=150, blank=True, null=True)
    observaciones = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'boletas'

class Ccalidad(models.Model):

    registro = models.BigAutoField(primary_key=True)
    causarechazo = models.CharField(max_length=100, blank=True, null=True)
    porcentaje = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    llave = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    observaciones = models.CharField(max_length=125, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ccalidad'

class Recepciones(models.Model):
    #op_status = [('Pendiente','-'),('En proceso','En proceso')]
    
    registro = models.BigAutoField(primary_key=True)
    recepcion = models.BigIntegerField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    fechasalidafruta = models.DateField(blank=True, null=True)
    llave = models.CharField(max_length=200, blank=True, null=True)
    finca = models.CharField(max_length=75, blank=True, null=True)
    variedad = models.CharField(max_length=50, blank=True, null=True)
    cajas = models.BigIntegerField(blank=True, null=True)
    libras = models.FloatField(blank=True, null=True)
    observaciones = models.CharField(max_length=125, blank=True, null=True)
    cultivo = models.CharField(max_length=50, blank=True, null=True)
    llave2 = models.CharField(max_length=200, blank=True, null=True)
    criterio = models.CharField(max_length=85, blank=True, null=True)
    status = models.CharField(max_length=25, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    classorigen = models.CharField(max_length=35, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    enviofruta = models.BigIntegerField(blank=True, null=True)
    orden = models.CharField(max_length=30, blank=True, null=True)
    viaje = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recepciones'

class causasRechazo(models.Model):
    
    registro = models.BigAutoField(primary_key=True)
    causa = models.CharField(max_length=75, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return str(self.registro)

class inventarioProdTerm(models.Model):
    
    #op_proveedor = [('','-'),('FINCA LA PASTORIA, S.A.','FINCA LA PASTORIA, S.A.'),('INVERSIONES LA PASTORIA, S.A.','INVERSIONES LA PASTORIA, S.A.'),('SDC','SDC'),('AGROINDUSTRIAS SAN RAFAEL, S.A.','AGROINDUSTRIAS SAN RAFAEL, S.A.'),('INVERNADEROS TECNOLOGICOS S.A','INVERNADEROS TECNOLOGICOS S.A'),('HORTEX, S.A.','HORTEX, S.A.'),('DANIEL ESTUARDO GALICIA CARRERA','DANIEL ESTUARDO GALICIA CARRERA'),('PRODUCTOS DEL VALLE, S.A.','PRODUCTOS DEL VALLE, S.A.')]
    #op_cultivo =   [('','-'),('ROMA','ROMA'),('CHERRY','CHERRY'),('ARANDANO','ARANDANO'),('PITAYA','PITAYA'),('PEPINO','PEPINO'),('AGUACATE','AGUACATE'),('PEPINO','PEPINO'),('MEDLEY','MEDLEY'),('BEEF','BEEF'),('SALADETTE','SALADETTE'),('GRAPE','GRAPE'),('GRAPE ORGANICO','GRAPE ORGANICO'),('CHERRY ORGANICO','CHERRY ORGANICO'),('BLOCKY','BLOCKY'),('BLOCKY ORGANICO','BLOCKY ORGANICO'),('MINI','MINI'),('MINI ORGANICO','MINI ORGANICO')]
    #op_categoria = [('','-'),('Exportación','Exportación'),('Merma','Merma'),('Carreta','Carreta'),('Cenma','Cenma'),('Devolución','Devolución')]
    #op_empaque =   [('Cajas','Cajas'),('Libras','Libras')]
    #op_status = [('Pendiente','-'),('Cerrado','Cerrado'),('En proceso','En proceso')]

    registro = models.BigAutoField(primary_key=True)
    fecha = models.DateField(blank=True, null=True)
    categoria = models.CharField(max_length=50,  blank=True, null=True)
    cultivo = models.CharField(max_length=50,  blank=True, null=True)
    proveedor = models.CharField(max_length=75, blank=True, null=True)
    #empaque = models.CharField(max_length=75, choices=op_empaque,blank=True, null=True)
    itemsapcode = models.CharField(max_length=20, blank=True, null=True)
    itemsapname = models.CharField(max_length=200, blank=True, null=True)
    calidad1 = models.CharField(max_length=200, blank=True, null=True)
    cajas = models.BigIntegerField(blank=True, null=True)
    libras =  models.FloatField(blank=True, null=True)
    pesostdxcaja =  models.FloatField(blank=True, null=True)
    lbsintara =  models.FloatField(blank=True, null=True)
    pesostd = models.FloatField(blank=True, null=True)
    merma =  models.FloatField(blank=True, null=True)
    pesorxcaja =  models.FloatField(blank=True, null=True)
    pesosinmerma = models.FloatField(blank=True, null=True)
    tara = models.FloatField(blank=True, null=True)
    orden=models.CharField(max_length=20,blank=True,null=True)
    status = models.CharField(max_length=25, blank=True, null=True)
    status2 = models.CharField(max_length=25, blank=True, null=True)
    status3 = models.CharField(max_length=25, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    op_sap = models.CharField(max_length=20,blank=True, null=True)
    boleta=models.BigIntegerField(blank=True, null=True)
    reasignacion=models.CharField(max_length=75,null=True,blank=True)
    enviorec=models.BigIntegerField(blank=True, null=True)
    
    def __str__(self):
        return str(self.registro) + " | " + str(self.proveedor) + " | " + str(self.itemsapname)+ " | " + str(self.cultivo)


class inventarioProdTermAux(models.Model):
    
    #op_proveedor = [('','-'),('FINCA LA PASTORIA, S.A.','FINCA LA PASTORIA, S.A.'),('INVERSIONES LA PASTORIA, S.A.','INVERSIONES LA PASTORIA, S.A.'),('SDC','SDC'),('AGROINDUSTRIAS SAN RAFAEL, S.A.','AGROINDUSTRIAS SAN RAFAEL, S.A.'),('INVERNADEROS TECNOLOGICOS S.A','INVERNADEROS TECNOLOGICOS S.A'),('HORTEX, S.A.','HORTEX, S.A.'),('DANIEL ESTUARDO GALICIA CARRERA','DANIEL ESTUARDO GALICIA CARRERA'),('PRODUCTOS DEL VALLE, S.A.','PRODUCTOS DEL VALLE, S.A.')]
    #op_cultivo =   [('','-'),('ROMA','ROMA'),('CHERRY','CHERRY'),('ARANDANO','ARANDANO'),('PITAYA','PITAYA'),('PEPINO','PEPINO'),('AGUACATE','AGUACATE'),('PEPINO','PEPINO'),('MEDLEY','MEDLEY'),('BEEF','BEEF'),('SALADETTE','SALADETTE'),('GRAPE','GRAPE'),('GRAPE ORGANICO','GRAPE ORGANICO'),('CHERRY ORGANICO','CHERRY ORGANICO'),('BLOCKY','BLOCKY'),('BLOCKY ORGANICO','BLOCKY ORGANICO'),('MINI','MINI'),('MINI ORGANICO','MINI ORGANICO')]
    #op_categoria = [('','-'),('Exportación','Exportación'),('Merma','Merma'),('Carreta','Carreta'),('Cenma','Cenma'),('Devolución','Devolución')]
    #op_empaque =   [('Cajas','Cajas'),('Libras','Libras')]
    #op_status = [('Pendiente','-'),('Cerrado','Cerrado'),('En proceso','En proceso')]

    registro = models.BigAutoField(primary_key=True)
    inventarioreg = models.BigIntegerField(blank=True, null = True)
    fecha = models.DateField(blank=True, null=True)
    categoria = models.CharField(max_length=50,  blank=True, null=True)
    cultivo = models.CharField(max_length=50, blank=True, null=True)
    proveedor = models.CharField(max_length=75,blank=True, null=True)
    #empaque = models.CharField(max_length=75, choices=op_empaque,blank=True, null=True)
    itemsapcode = models.CharField(max_length=20, blank=True, null=True)
    itemsapname = models.CharField(max_length=200, blank=True, null=True)
    calidad1 = models.CharField(max_length=200, blank=True, null=True)
    cajas = models.BigIntegerField(blank=True, null=True)
    pesostdxcaja =  models.FloatField(blank=True, null=True)
    lbsintara =  models.FloatField(blank=True, null=True)
    pesostd = models.FloatField(blank=True, null=True)
    merma =  models.FloatField(blank=True, null=True)
    pesorxcaja =  models.FloatField(blank=True, null=True)
    pesosinmerma = models.FloatField(blank=True, null=True)
    orden=models.CharField(max_length=20,blank=True,null=True)
    status = models.CharField(max_length=25,blank=True, null=True)
    status2 = models.CharField(max_length=25, blank=True, null=True)
    status3 = models.CharField(max_length=25, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    op_sap = models.CharField(max_length=20,blank=True, null=True)
    boleta=models.BigIntegerField(blank=True, null=True)
    salidacontenedores=models.CharField(max_length=20,blank=True,null=True)
    
    
    def __str__(self):
        return str(self.registro) + " | " + str(self.proveedor) + " | " + str(self.itemsapname)+ " | " + str(self.cultivo)

class contenedores(models.Model):
    
    #op_empaque =   [('Cajas','Cajas'),('Libras','Libras')]
    #op_status = [('Pendiente','-'),('Cerrado','Cerrado')]
    #op_destino = [('Jonestown','Jonestown'),('Lakeland','Lakeland'),('Laredo, Texas','Laredo, Texas'),('Miami','Miami')]
    #op_naviera = [('SEABOARD','SEABOARD'),('CROWLEY','CROWLEY')]
    

    registro = models.BigAutoField(primary_key=True)
    fecha = models.DateField(blank=True, null=True)
    destino = models.CharField(max_length=30, blank=True, null=True)
    transportista = models.CharField(max_length=30, blank=True, null=True)
    contenedor = models.CharField(max_length=50, blank=True, null=True)
    viaje = models.BigIntegerField(blank=True, null=True)
    temperatura = models.BigIntegerField(blank=True, null=True)
    ventilacion = models.BigIntegerField(blank=True, null=True)
    piloto = models.CharField(max_length=50, blank=True, null=True)
    marchamo = models.CharField(max_length=50, blank=True, null=True)
    placacamion = models.CharField(max_length=50, blank=True, null=True)
    horasalida = models.TimeField(blank=True, null=True)
    status = models.CharField(max_length=25,blank=True, null=True)
    etd = models.DateField(blank=True, null=True)
    eta = models.DateField(blank=True, null=True)
    bl = models.CharField(max_length=50, blank=True, null=True)
    booking = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    def __str__(self):
        return str(self.registro) + " | " + str(self.fecha)+ " | " + str(self.contenedor)

class salidacontenedores(models.Model):

    #op_status = [('Pendiente','-'),('Cerrado','Cerrado')]
    #op_proveedor = [('','-'),('SDC','SDC'),('AGROINDUSTRIAS SAN RAFAEL, S.A.','AGROINDUSTRIAS SAN RAFAEL, S.A.'),('INVERNADEROS TECNOLOGICOS S.A','INVERNADEROS TECNOLOGICOS S.A'),('HORTEX, S.A.','HORTEX, S.A.'),('DANIEL ESTUARDO GALICIA CARRERA','DANIEL ESTUARDO GALICIA CARRERA'),('PRODUCTOS DEL VALLE, S.A.','PRODUCTOS DEL VALLE, S.A.')]
    #op_cultivo =   [('','-'),('ROMA','ROMA'),('CHERRY','CHERRY'),('MEDLEY','MEDLEY'),('BEEF','BEEF'),('SALADETTE','SALADETTE'),('GRAPE','GRAPE'),('GRAPE ORGANICO','GRAPE ORGANICO'),('CHERRY ORGANICO','CHERRY ORGANICO'),('BLOCKY','BLOCKY'),('BLOCKY ORGANICO','BLOCKY ORGANICO'),('MINI','MINI'),('MINI ORGANICO','MINI ORGANICO')]
    #op_categoria = [('','-'),('Exportación','Exportación'),('Carreta','Carreta'),('Cenma','Cenma'),('Devolución','Devolución')]
    #op_empaque =   [('Cajas','Cajas'),('Libras','Libras')]

    registro = models.BigAutoField(primary_key=True)
    key = models.BigIntegerField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    fechasalcontenedor =models.DateField(blank=True, null=True)
    contenedor = models.CharField(max_length=50, blank=True, null=True)
    categoria = models.CharField(max_length=50,  blank=True, null=True)
    cultivo = models.CharField(max_length=50,  blank=True, null=True)
    proveedor = models.CharField(max_length=75, blank=True, null=True)
    #empaque = models.CharField(max_length=75, choices=op_empaque,blank=True, null=True)
    itemsapcode = models.CharField(max_length=20, blank=True, null=True)
    itemsapname = models.CharField(max_length=200, blank=True, null=True)
    calidad1 = models.CharField(max_length=200, blank=True, null=True)
    cajas = models.BigIntegerField(blank=True, null=True)
    pesostdxcaja =  models.FloatField(blank=True, null=True)
    lbsintara =  models.FloatField(blank=True, null=True)
    pesostd = models.FloatField(blank=True, null=True)
    merma =  models.FloatField(blank=True, null=True)
    pesorxcaja =  models.FloatField(blank=True, null=True)
    pesosinmerma = models.FloatField(blank=True, null=True)
    orden=models.CharField(max_length=20,blank=True,null=True)
    boleta=models.BigIntegerField(blank=True, null=True)
    reasignacion=models.CharField(max_length=75,null=True, blank=True)
    importe =models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    status=models.CharField(max_length=25,blank=True,null=True)
    palet = models.IntegerField(blank=True, null=True)
    def __str__(self):
        return str(self.registro) + " | " + str(self.contenedor) + " | " + str(self.proveedor) + " | " + str(self.itemsapname)+ " | " + str(self.cultivo)
    
class productoTerm(models.Model):
    
    #op_cultivo =   [('ROMA','ROMA'),('AGUACATE','AGUACATE'),('PITAYA','PITAYA'),('PEPINO','PEPINO'),('ARANDANO','ARANDANO'),('CHERRY','CHERRY'),('MEDLEY','MEDLEY'),('BEEF','BEEF'),('SALADETTE','SALADETTE'),('GRAPE','GRAPE'),('GRAPE ORGANICO','GRAPE ORGANICO'),('CHERRY ORGANICO','CHERRY ORGANICO'),('BLOCKY','BLOCKY'),('BLOCKY ORGANICO','BLOCKY ORGANICO'),('MINI','MINI'),('MINI ORGANICO','MINI ORGANICO')]
    #op_categoria = [('Exportación','Exportación'),('Carreta','Carreta'),('Cenma','Cenma'),('Devolución','Devolución')]
    #op_tipo =      [('Tomate','Tomate'),('Aguacate','Aguacate'),('Chile','Chile'),('Arandano','Arandano'),('Pitaya','Pitaya'),('Pepino','Pepino')]
    
    registro = models.BigAutoField(primary_key=True)
    cultivo = models.CharField(max_length=50, blank=True, null=True)
    itemsapcode  = models.CharField(max_length=50, blank=True, null=True)
    itemsapname = models.CharField(max_length=200, blank=True, null=True)
    
    itemsapcodelibra = models.CharField(max_length=200, blank=True, null=True)
    
    calidad1 = models.CharField(max_length=200, blank=True, null=True)
    precio = models.FloatField(blank=True, null=True)
    categoria = models.CharField(max_length=50, blank=True, null=True)
    taraxcaja = models.FloatField(blank=True, null=True)
    pesostdxcaja = models.FloatField(blank=True, null=True)
    tipo = models.CharField(max_length=50,  blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    orden= models.CharField(max_length=30, blank=True, null=True)
    cajasxtarima= models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(str(self.cultivo)+ " | " + str(self.itemsapcode)+ " | " + str(self.itemsapname))

class tipoCajas(models.Model):
    registro = models.BigAutoField(primary_key=True)
    tcaja = models.CharField(max_length=75, blank=True, null=True)
    peso =  models.FloatField(blank=True, null=True)
    

    def __str__(self):
        return str(self.tcaja)

class productores(models.Model):
    registro = models.BigAutoField(primary_key=True)
    productor = models.CharField(max_length=75, blank=True, null=True)
    tipo = models.CharField(max_length=75, blank=True, null=True)
    def __str__(self):
        return str(self.productor)

class cultivos(models.Model):
    registro = models.BigAutoField(primary_key=True)
    cultivo = models.CharField(max_length=75, blank=True, null=True)
    
    def __str__(self):
        return str(self.cultivo)
       
class detallerec(models.Model):

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
    llave2 = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=25,blank=True,null = True)
    classorigen = models.CharField(max_length=35, blank= True, null = True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    enviofruta = models.BigIntegerField(blank=True, null=True)
    boleta = models.BigIntegerField(blank=True, null = True)
    fechasalidafruta = models.DateField(blank=True, null=True)
    
    viaje = models.CharField(max_length=30, blank=True, null=True)
    orden = models.CharField(max_length=30, blank=True, null=True)

class detallerecaux(models.Model):

    #op_status = [('Pendiente','-'),('En proceso','En proceso'),('Cerrado','Cerrado')]
    
    registro = models.BigAutoField(primary_key=True)
    recepcion = models.BigIntegerField(blank=True, null = True)
    fecha = models.DateField(blank=True, null=True)
    llave = models.CharField(max_length=200, blank = True, null = True)
    finca = models.CharField(max_length= 75, blank = True, null =  True)
    cajas = models.BigIntegerField(blank = True, null = True)
    libras = models.FloatField(blank=True, null = True)
    observaciones = models.CharField(max_length=125,blank=True, null = True)
    cultivo = models.CharField(max_length=50, blank = True, null = True)
    llave2 = models.CharField(max_length=200, blank=True, null=True)
    criterio = models.CharField(max_length=85, blank = True, null = True)
    status = models.CharField(max_length=25,blank=True,null = True)
    classorigen = models.CharField(max_length=35, blank= True, null = True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    enviofruta = models.BigIntegerField(blank=True, null=True)
    boleta = models.BigIntegerField(blank=True, null = True)
    fechasalidafruta = models.DateField(blank=True, null=True)
    orden = models.CharField(max_length=30, blank=True, null=True)

class enviosrec(models.Model):
    #op_status = [('Pendiente','-'),('En proceso','En proceso'),('Cerrado','Cerrado')]
    registro = models.BigAutoField(primary_key=True)
    envio = models.BigIntegerField(blank=True, null = True)
    cantidad = models.FloatField(blank = True, null = True)
    u_m = models.CharField(max_length= 25, blank = True, null =  True)
    itemsap_name = models.CharField(max_length= 200, blank = True, null =  True)
    itemsap_code = models.CharField(max_length= 15, blank = True, null =  True)
    calidad1 = models.CharField(max_length= 200, blank = True, null =  True)
    fecha = models.DateField(blank=True, null=True)
    destino = models.CharField(max_length= 150, blank = True, null =  True)
    recibe = models.CharField(max_length= 75, blank = True, null =  True)
    observaciones = models.CharField(max_length=125,blank=True, null = True)
    empaque_cnt = models.FloatField(blank = True, null = True)
    empaque_tipo = models.CharField(max_length= 25, blank = True, null =  True)
    lugar = models.CharField(max_length= 25, blank = True, null =  True)
    clasificacion = models.CharField(max_length= 25, blank = True, null =  True)
    rubro = models.CharField(max_length= 25, blank = True, null =  True)
    grupoarticulos = models.CharField(max_length= 25, blank = True, null =  True)
    almacen = models.CharField(max_length= 25, blank = True, null =  True)
    firma = models.CharField(max_length= 75, blank = True, null =  True)
    status = models.CharField(max_length=25,blank=True,null = True)
    productor = models.CharField(max_length= 75, blank = True, null =  True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    libras = models.FloatField(blank = True, null = True)

class paramenvlocales(models.Model):
    #op_status = [('Pendiente','-'),('En proceso','En proceso'),('Cerrado','Cerrado')]
    registro = models.BigAutoField(primary_key=True)
    descripcion = models.CharField(max_length= 200, blank = True, null =  True)
    u_m = models.CharField(max_length= 25, blank = True, null =  True)
    item = models.CharField(max_length= 30, blank = True, null =  True)
    clasificacion = models.CharField(max_length= 45, blank = True, null =  True)
    almacen = models.CharField(max_length= 25, blank = True, null =  True)
    grupo = models.CharField(max_length= 50, blank = True, null =  True)
    rubro = models.CharField(max_length= 50, blank = True, null =  True)

class destinoslocales(models.Model):
    #op_status = [('Pendiente','-'),('En proceso','En proceso'),('Cerrado','Cerrado')]
    registro = models.BigAutoField(primary_key=True)
    cod_destino = models.CharField(max_length= 20, blank = True, null =  True)
    destino = models.CharField(max_length= 200, blank = True, null =  True)

class und_emplocales(models.Model):
    #op_status = [('Pendiente','-'),('En proceso','En proceso'),('Cerrado','Cerrado')]
    registro = models.BigAutoField(primary_key=True)
    cod_empaque = models.CharField(max_length= 20, blank = True, null =  True)


class pedidos(models.Model):

    registro = models.AutoField(primary_key=True)
    pedido = models.BigIntegerField(blank=True, null = True)
    fecha = models.DateField(blank=True, null=True)
    fechapedido = models.DateField(blank=True, null=True)
    cultivo = models.CharField(max_length=45, blank=True, null=True)
    itemsapname =models.CharField(max_length=150, blank=True, null=True)
    calidad1 =models.CharField(max_length=150, blank=True, null=True)
    itemsapcode =models.CharField(max_length=45, blank=True, null=True)
    precio = models.FloatField(blank=True, null=True)
    total =models.FloatField(blank=True, null=True)
    cantidad = models.IntegerField(blank=True, null=True)
    orden = models.CharField(max_length=20, blank=True, null=True)
    libras = models.FloatField(blank=True, null=True)
    cantidadentregado = models.IntegerField(blank=True, null=True)
    cliente = models.CharField(max_length=45, blank=True,  null=True)
    categoria = models.CharField(max_length=45, blank=True,  null=True)
    encargado = models.CharField(max_length=75, blank=True,  null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    envio = models.BigIntegerField(blank=True, null = True)

    def __str__(self):
        return (str(self.registro)+ " | " + str(self.fecha) + " | " + str(self.pedido) + " | " + str(self.itemsapname)+ " | " + str(self.encargado) + " | " + str(self.cultivo))
