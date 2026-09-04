from django import forms


class LoginMantenimientoForm(forms.Form):

    username = forms.CharField(
        label="Usuario",
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Ingresa tu usuario",
                "autocomplete": "username",
            }
        )
    )

    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Ingresa tu contraseña",
                "autocomplete": "current-password",
            }
        )
    )
