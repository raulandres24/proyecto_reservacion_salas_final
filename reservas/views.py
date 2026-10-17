from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from .servicios import BLOQUES, Rechazo, consultar_salas_libres


@login_required
def salas_libres(request):
    salas = None
    if "fecha" in request.GET:
        try:
            fecha = date.fromisoformat(request.GET["fecha"])
            bloque = int(request.GET["bloque"])
            salas = consultar_salas_libres(request.user, fecha, bloque, timezone.localtime())
        except Rechazo as rechazo:
            messages.error(request, rechazo.causa)
        except ValueError:
            messages.error(request, "La fecha o el bloque no son válidos")
    return render(request, "reservas/salas_libres.html", {"salas": salas, "bloques": BLOQUES})