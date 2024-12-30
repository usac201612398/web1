# forms.py
from django import forms
from .models import QRCodeData

class RegistroQRForm(forms.ModelForm):
    class Meta:
        model = QRCodeData
        fields = ['data','color', 'cantidad','cosechador','blossom','n_semillas','peso','status']  # Los campos que pueden ser editados