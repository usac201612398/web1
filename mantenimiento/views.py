from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from .forms import LoginMantenimientoForm
from .models import UsuarioMantenimiento


def index(request):

    # Si ya inició sesión, no tiene sentido
    # volver a mostrar el login.
    if request.user.is_authenticated:
        return redirect("home")

    form = LoginMantenimientoForm(request.POST or None)

    if request.method == "POST":

        if form.is_valid():

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            # Django comprueba usuario y contraseña
            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is None:

                form.add_error(
                    None,
                    "Usuario o contraseña incorrectos."
                )

            else:

                try:
                    perfil = UsuarioMantenimiento.objects.get(
                        user=user
                    )

                except UsuarioMantenimiento.DoesNotExist:

                    form.add_error(
                        None,
                        "Este usuario no está registrado "
                        "en el sistema de mantenimiento."
                    )

                else:

                    if not perfil.activo:

                        form.add_error(
                            None,
                            "Este usuario se encuentra desactivado."
                        )

                    elif not perfil.puede_acceder:

                        form.add_error(
                            None,
                            "No tienes autorización para acceder "
                            "al sistema de mantenimiento."
                        )

                    else:

                        # Login Django
                        login(request, user)

                        return redirect("home")

    return render(
        request,
        "mantenimiento/login.html",
        {
            "form": form
        }
    )


def home(request):

    return render(
        request,
        "home.html"
    )

