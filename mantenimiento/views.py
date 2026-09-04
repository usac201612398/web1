from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import LoginMantenimientoForm
from .models import UsuarioMantenimiento


def index(request):

    # ---------------------------------------------------------
    # Si YA pasó el login propio de Mantenimiento,
    # entonces sí puede entrar directamente al Home.
    # ---------------------------------------------------------

    if request.session.get("mantenimiento_autenticado"):

        return redirect("home")


    # ---------------------------------------------------------
    # Mostrar nuestro Login de Mantenimiento
    # ---------------------------------------------------------

    form = LoginMantenimientoForm(request.POST or None)


    if request.method == "POST":

        if form.is_valid():

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]


            # -------------------------------------------------
            # Validar usuario y contraseña contra Django
            # -------------------------------------------------

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

                # ---------------------------------------------
                # Buscar perfil de Mantenimiento
                # ---------------------------------------------

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

                    # -----------------------------------------
                    # Verificar estado
                    # -----------------------------------------

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

                        # -------------------------------------
                        # Usuario autorizado
                        # -------------------------------------

                        login(request, user)

                        # Marcar segundo login como válido
                        request.session[
                            "mantenimiento_autenticado"
                        ] = True

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

    # ---------------------------------------------------------
    # Verificar que también haya pasado el login propio
    # de Mantenimiento.
    # ---------------------------------------------------------

    if not request.session.get(
        "mantenimiento_autenticado"
    ):

        return redirect("index")


    return render(
        request,
        "mantenimiento/home.html"
    )


