from . import reglas
from .models import Mantenimiento, Reserva, Sala
from .reglas import Rechazo
from django.db import IntegrityError
from django.core.exceptions import ValidationError


def buscar_sala(letra):
    try:
        return Sala.objects.get(letra=letra)
    except Sala.DoesNotExist:
        raise Rechazo("la sala no existe")

def sala_esta_ocupada(sala, fecha, bloque):
    return Reserva.objects.filter(
        sala=sala, fecha=fecha, bloque=bloque, estado=Reserva.Estado.CONFIRMADA
    ).exists()

def hay_mantenimiento(sala, fecha, bloque):
    return Mantenimiento.objects.filter(sala=sala, fecha=fecha, bloque=bloque).exists()

def bloques_del_dueno(dueno, fecha, excepto=None):
    reservas = Reserva.objects.filter(
        dueno=dueno, fecha=fecha, estado=Reserva.Estado.CONFIRMADA
    )
    if excepto:
        reservas = reservas.exclude(pk=excepto.pk)
    return list(reservas.values_list("bloque", flat=True))

def guardar_reserva(reserva):
    try:
        reserva.save()
    except IntegrityError as error:
        llaves = error.__cause__.details["writeErrors"][0]["keyPattern"]
        if "sala_id" in llaves:
            raise Rechazo(reglas.CAUSA_SALA_OCUPADA)
        if "dueno_id" in llaves:
            raise Rechazo(reglas.CAUSA_BLOQUE_REPETIDO)
        raise

def crear_reserva(usuario, letra_sala, fecha, bloque, asistentes, ahora):
    sala = buscar_sala(letra_sala)
    reglas.comprobar_reserva(
        usuario, sala, fecha, bloque, asistentes, ahora,
        sala_esta_ocupada(sala, fecha, bloque),
        hay_mantenimiento(sala, fecha, bloque),
        bloques_del_dueno(usuario, fecha),
    )
    reserva = Reserva(
        dueno=usuario, sala=sala, fecha=fecha, bloque=bloque, asistentes=asistentes
    )
    guardar_reserva(reserva)
    return reserva

def buscar_reserva(reserva_id):
    try:
        return Reserva.objects.get(pk=reserva_id)
    except (Reserva.DoesNotExist, ValidationError):
        raise Rechazo("la reserva no existe")

def cancelar(reserva, motivo):
    reserva.estado = Reserva.Estado.CANCELADA
    reserva.motivo_cancelacion = motivo
    reserva.save()
    return reserva

def cancelar_reserva(usuario, reserva_id, ahora):
    reserva = buscar_reserva(reserva_id)
    reglas.verificar_puede_cancelar(reserva, usuario, ahora)
    return cancelar(reserva, reglas.motivo_de_cancelacion(usuario))

def no_mantener_reserva(usuario, reserva_id):
    reserva = buscar_reserva(reserva_id)
    reglas.verificar_dueno(reserva, usuario)
    reglas.verificar_confirmada(reserva)
    return cancelar(reserva, Reserva.MotivoCancelacion.NO_LA_MANTUVO)