from django.db import models

class QRCodeData(models.Model):
    op_color = [('','Seleccione un color'),('Amarillo','Amarillo'),('Naranja','Naranja'),('Rojo','Rojo'),('Morado','Morado'),('Verde','Verde'),('Café','Café'),('Rosado','Rosado')]
    op_cosechador = [('','Seleccione un cosechador'),('JV','JV'),('RC','RC'),('SS','SS'),('SC','SC')]
    op_blossom = [('','Seleccione criterio'),('Si','Si'),('No','No')]
    op_status = [('Pendiente',''),('Cerrado','Cerrado')]

    id_escaner = models.BigAutoField(primary_key=True)
    data = models.TextField()  # Campo para almacenar los datos del QR
    cantidad = models.FloatField(blank=True, null=True)
    color = models.CharField(max_length=25, choices=op_color,blank=True, null=True)
    cosechador = models.CharField(max_length=25, choices=op_cosechador,blank=True, null=True)
    blossom = models.CharField(max_length=10, choices=op_blossom,blank=True, null=True)
    n_semillas = models.FloatField(blank=True, null=True)
    peso = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=op_status,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.data