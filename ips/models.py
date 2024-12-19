from django.db import models

class QRCodeData(models.Model):
    op_color = [('','Seleccione un color'),('Amarillo','Amarillo'),('Naranja','Naranja'),('Rojo','Rojo'),('Morado','Morado'),('Verde','Verde'),('Café','Café'),('Rosado','Rosado')]
    op_cosechador = [('','Seleccione un cosechador'),('JV','JV'),('RC','RC'),('SS','SS'),('SC','SC')]
    id_escaner = models.BigAutoField(primary_key=True)
    data = models.TextField()  # Campo para almacenar los datos del QR
    cantidad = models.FloatField()
    color = models.CharField(max_length=25, choices=op_color,blank=True, null=True)
    cosechador = models.CharField(max_length=25, choices=op_color,blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.data