from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .servicios import Rechazo, registrar


def registrarse(request):
    if request.method == "POST":
        try:
            registrar(
                request.POST["codigo"],
                request.POST["correo"],
                request.POST["contrasena"],
                request.POST["confirmacion"],
            )
        except Rechazo as rechazo:
            messages.error(request, rechazo.causa)
        else:
            messages.success(request, "Cuenta creada. Ya puedes iniciar sesión")
            return redirect("login")
    return render(request, "cuentas/registro.html")


def iniciar_sesion(request):
    if request.method == "POST":
        usuario = authenticate(request, username=request.POST["correo"], password=request.POST["contrasena"])
        if usuario is not None:
            login(request, usuario)
            return redirect("salas_libres")
        messages.error(request, "Correo o contraseña incorrectos")
    return render(request, "cuentas/login.html")


@require_POST
def cerrar_sesion(request):
    logout(request)
    return redirect("login")