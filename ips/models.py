from django.db import models

class QRCodeData(models.Model):
    op_color = [('-','-'),('AMARILLO','AMARILLO'),('ANARANJADO','ANARANJADO'),('ROJO','ROJO')]
    op_cosechador = [('-','-'),('VM','VM')]
    id_escaner = models.BigAutoField(primary_key=True)
    data = models.TextField()  # Campo para almacenar los datos del QR
    cantidad = models.FloatField()
    color = models.CharField(max_length=25, choices=op_color,blank=True, null=True)
    cosechador = models.CharField(max_length=25, choices=op_color,blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.data