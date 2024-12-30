# forms.py
from django import forms
from .models import QRCodeData

class RegistroQRForm(forms.ModelForm):
    op_status = [('Pendiente',''),('Cerrado','Cerrado')]
    status = forms.ChoiceField(choices=op_status,widget=forms.Select(attrs={'class': 'my-input'}))

    class Meta:
        model = QRCodeData
        
        fields = ['data','color', 'cantidad','cosechador','blossom','n_semillas','peso','status']  # Los campos que pueden ser editados