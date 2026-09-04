from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import LoginMantenimientoForm
from .models import UsuarioMantenimiento


def index(request):

    # Si ya tiene una sesión de Django,
    # no mostramos nuevamente el login.
    if request.user.is_authenticated:
        return redirect("home")

    form = LoginMantenimientoForm(request.POST or None)

    if request.method == "POST":

        if form.is_valid():

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            # Validar usuario y contraseña
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

                        # Crear sesión de Django
                        login(request, user)

                        return redirect("home")

    return render(
        request,
        "mantenimiento/login.html",
        {
            "form": form
        }
    )


@login_required
def home(request):

    return render(
        request,
        "mantenimiento/home.html"
    )

