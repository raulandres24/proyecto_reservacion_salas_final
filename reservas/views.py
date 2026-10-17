from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .servicios import (
    BLOQUES, Rechazo, cancelar_reserva, consultar_salas_libres, crear_reserva,
    listar_reservas, mis_reservas, modificar_reserva, no_mantener_reserva,
    registrar_mantenimiento, reserva_a_modificar, todas_las_salas,
)


def leer_fecha_bloque_asistentes(datos):
    return date.fromisoformat(datos["fecha"]), int(datos["bloque"]), int(datos["asistentes"])


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
        fecha, bloque, asistentes = leer_fecha_bloque_asistentes(request.POST)
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


@login_required
def modificar(request, reserva_id):
    ahora = timezone.localtime()
    try:
        reserva = reserva_a_modificar(request.user, reserva_id, ahora)
    except Rechazo as rechazo:
        messages.error(request, rechazo.causa)
        return redirect("mis_reservas")
    preguntar = False
    if request.method == "POST":
        try:
            fecha, bloque, asistentes = leer_fecha_bloque_asistentes(request.POST)
            modificar_reserva(request.user, reserva_id, fecha, bloque, asistentes, ahora)
        except Rechazo as rechazo:
            messages.error(request, rechazo.causa)
            preguntar = rechazo.preguntar_si_mantener
        except ValueError:
            messages.error(request, "Los datos de la reserva no son válidos")
        else:
            messages.success(request, "Reserva modificada")
            return redirect("mis_reservas")
    contexto = {"reserva": reserva, "bloques": BLOQUES, "preguntar": preguntar}
    return render(request, "reservas/modificar.html", contexto)


@require_POST
@login_required
def no_mantener(request, reserva_id):
    try:
        no_mantener_reserva(request.user, reserva_id)
    except Rechazo as rechazo:
        messages.error(request, rechazo.causa)
    else:
        messages.success(request, "Reserva cancelada")
    return redirect("mis_reservas")

@login_required
def reservas_del_dia(request):
    reservas = fecha = None
    if "fecha" in request.GET:
        try:
            fecha = date.fromisoformat(request.GET["fecha"])
            reservas = listar_reservas(request.user, fecha)
        except Rechazo as rechazo:
            messages.error(request, rechazo.causa)
        except ValueError:
            messages.error(request, "La fecha no es válida")
    return render(request, "reservas/reservas_del_dia.html", {"reservas": reservas, "fecha": fecha})

@login_required
def mantenimiento(request):
    if request.method == "POST":
        try:
            fecha = date.fromisoformat(request.POST["fecha"])
            bloques = [int(bloque) for bloque in request.POST.getlist("bloques")]
            canceladas = registrar_mantenimiento(
                request.user, request.POST["sala"], fecha, bloques, timezone.localtime()
            )
        except Rechazo as rechazo:
            messages.error(request, rechazo.causa)
        except ValueError:
            messages.error(request, "Los datos no son válidos")
        else:
            messages.success(request, f"Mantenimiento registrado. Reservas canceladas: {len(canceladas)}")
            return redirect("mantenimiento")
    return render(request, "reservas/mantenimiento.html", {"salas": todas_las_salas(), "bloques": BLOQUES})