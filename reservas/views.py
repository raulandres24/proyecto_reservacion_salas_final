from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from .servicios import BLOQUES, Rechazo, cancelar_reserva, consultar_salas_libres, crear_reserva, mis_reservas
from .servicios import BLOQUES, Rechazo, consultar_salas_libres, crear_reserva, mis_reservas


@login_required
def salas_libres(request):
    salas = fecha = bloque = None
    if "fecha" in request.GET:
        try:
            fecha = date.fromisoformat(request.GET["fecha"])
            bloque = int(request.GET["bloque"])
            salas = consultar_salas_libres(request.user, fecha, bloque, timezone.localtime())
        except Rechazo as rechazo:
            messages.error(request, rechazo.causa)
        except ValueError:
            messages.error(request, "La fecha o el bloque no son válidos")
    contexto = {"salas": salas, "fecha": fecha, "bloque": bloque, "bloques": BLOQUES}
    return render(request, "reservas/salas_libres.html", contexto)


@require_POST
@login_required
def reservar(request):
    try:
        fecha = date.fromisoformat(request.POST["fecha"])
        bloque = int(request.POST["bloque"])
        asistentes = int(request.POST["asistentes"])
        crear_reserva(request.user, request.POST["sala"], fecha, bloque, asistentes, timezone.localtime())
    except Rechazo as rechazo:
        messages.error(request, rechazo.causa)
        return redirect("salas_libres")
    except ValueError:
        messages.error(request, "Los datos de la reserva no son válidos")
        return redirect("salas_libres")
    messages.success(request, "Reserva confirmada")
    return redirect("mis_reservas")


@login_required
def ver_mis_reservas(request):
    return render(request, "reservas/mis_reservas.html", {"reservas": mis_reservas(request.user)})

@require_POST
@login_required
def cancelar(request, reserva_id):
    try:
        cancelar_reserva(request.user, reserva_id, timezone.localtime())
    except Rechazo as rechazo:
        messages.error(request, rechazo.causa)
    else:
        messages.success(request, "Reserva cancelada")
    return redirect("mis_reservas")