from django.db import models

class QRCodeData(models.Model):
    id_escaner = models.BigAutoField(primary_key=True)
    data = models.TextField()  # Campo para almacenar los datos del QR
    cantidad = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.data