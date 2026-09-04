from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

#from .forms import LoginMantenimientoForm
#from .models import UsuarioMantenimiento


def index(request):

    

    return render(
        request,
        "mantenimiento/login.html"
    )


@login_required
def home(request):

    return render(
        request,
        "mantenimiento/home.html"
    )

