from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import UsuarioMantenimiento


@login_required
def index(request):

    # ---------------------------------------------------------
    # El usuario ya fue autenticado por Microsoft / ADFS.
    # Ahora verificamos si tiene autorización para
    # utilizar el sistema de mantenimiento.
    # ---------------------------------------------------------

    try:

        perfil = request.user.mantenimiento

    except UsuarioMantenimiento.DoesNotExist:

        return render(
            request,
            "mantenimiento/acceso_denegado.html",
            {
                "mensaje": (
                    "Tu usuario está autenticado, "
                    "pero no está registrado en el sistema "
                    "de mantenimiento."
                )
            },
            status=403
        )


    # ---------------------------------------------------------
    # Verificar si está activo
    # ---------------------------------------------------------

    if not perfil.activo:

        return render(
            request,
            "mantenimiento/acceso_denegado.html",
            {
                "mensaje": (
                    "Tu acceso al sistema de mantenimiento "
                    "se encuentra desactivado."
                )
            },
            status=403
        )


    # ---------------------------------------------------------
    # Verificar permiso
    # ---------------------------------------------------------

    if not perfil.puede_acceder:

        return render(
            request,
            "mantenimiento/acceso_denegado.html",
            {
                "mensaje": (
                    "Tu cuenta de Microsoft está autenticada, "
                    "pero no tienes autorización para utilizar "
                    "el sistema de mantenimiento."
                )
            },
            status=403
        )


    # ---------------------------------------------------------
    # Todo correcto
    # ---------------------------------------------------------

    return redirect("home")


@login_required
def home(request):

    # ---------------------------------------------------------
    # Nunca permitir entrar al Home solamente por estar
    # autenticado en Microsoft.
    # ---------------------------------------------------------

    try:

        perfil = request.user.mantenimiento

    except UsuarioMantenimiento.DoesNotExist:

        return render(
            request,
            "mantenimiento/acceso_denegado.html",
            {
                "mensaje": (
                    "No tienes autorización para acceder "
                    "al sistema de mantenimiento."
                )
            },
            status=403
        )


    if not perfil.activo or not perfil.puede_acceder:

        return render(
            request,
            "mantenimiento/acceso_denegado.html",
            {
                "mensaje": (
                    "Tu acceso al sistema de mantenimiento "
                    "está desactivado."
                )
            },
            status=403
        )


    return render(
        request,
        "mantenimiento/home.html",
        {
            "perfil": perfil
        }
    )

