from django import forms

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

class ImageUploadForm(forms.Form):
    image = forms.ImageField()