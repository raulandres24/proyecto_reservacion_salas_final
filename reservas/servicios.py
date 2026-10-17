from . import reglas
from .models import Mantenimiento, Reserva, Sala
from .reglas import Rechazo
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django_mongodb_backend import transaction
from .reglas import BLOQUES, Rechazo

def buscar_sala(letra):
    try:
        return Sala.objects.get(letra=letra)
    except Sala.DoesNotExist:
        raise Rechazo("la sala no existe")

def sala_esta_ocupada(sala, fecha, bloque, excepto=None):
    reservas = Reserva.objects.filter(
        sala=sala, fecha=fecha, bloque=bloque, estado=Reserva.Estado.CONFIRMADA
    )
    if excepto:
        reservas = reservas.exclude(pk=excepto.pk)
    return reservas.exists()

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

def mis_reservas(usuario):
    return list(Reserva.objects.filter(dueno=usuario).order_by("fecha", "bloque"))

def listar_reservas(administrador, fecha):
    reglas.verificar_es_administrador(administrador)
    return list(
        Reserva.objects.filter(fecha=fecha, estado=Reserva.Estado.CONFIRMADA).order_by("bloque")
    )

def sala_esta_libre(sala, fecha, bloque):
    return not sala_esta_ocupada(sala, fecha, bloque) and not hay_mantenimiento(
        sala, fecha, bloque
    )

def consultar_salas_libres(usuario, fecha, bloque, ahora):
    reglas.verificar_dia_y_bloque(fecha, bloque, ahora)
    reglas.verificar_anticipacion(usuario, fecha, ahora)
    return [
        sala
        for sala in Sala.objects.order_by("letra")
        if reglas.puede_usar_sala(usuario, sala) and sala_esta_libre(sala, fecha, bloque)
    ]

def aplicar_cambio(reserva, fecha, bloque, asistentes, ahora):
    dueno = reserva.dueno
    sala = reserva.sala
    reglas.comprobar_reserva(
        dueno, sala, fecha, bloque, asistentes, ahora,
        sala_esta_ocupada(sala, fecha, bloque, excepto=reserva),
        hay_mantenimiento(sala, fecha, bloque),
        bloques_del_dueno(dueno, fecha, excepto=reserva),
    )
    reserva.fecha = fecha
    reserva.bloque = bloque
    reserva.asistentes = asistentes
    guardar_reserva(reserva)

def reserva_a_modificar(usuario, reserva_id, ahora):
    reserva = buscar_reserva(reserva_id)
    reglas.verificar_puede_modificar(reserva, usuario, ahora)
    return reserva

def modificar_reserva(usuario, reserva_id, fecha, bloque, asistentes, ahora):
    reserva = reserva_a_modificar(usuario, reserva_id, ahora)
    try:
        aplicar_cambio(reserva, fecha, bloque, asistentes, ahora)
    except Rechazo as rechazo:
        rechazo.preguntar_si_mantener = reglas.debe_preguntar_si_mantener(reserva, usuario)
        raise
    return reserva

def poner_en_mantenimiento(administrador, sala, fecha, bloque, ahora):
    Mantenimiento.objects.get_or_create(
        sala=sala, fecha=fecha, bloque=bloque,
        defaults={"registrado_por": administrador, "registrado_en": ahora},
    )
    afectadas = list(
        Reserva.objects.filter(
            sala=sala, fecha=fecha, bloque=bloque, estado=Reserva.Estado.CONFIRMADA
        )
    )
    return [cancelar(reserva, Reserva.MotivoCancelacion.POR_MANTENIMIENTO) for reserva in afectadas]

def registrar_mantenimiento(administrador, letra_sala, fecha, bloques, ahora):
    reglas.verificar_es_administrador(administrador)
    reglas.verificar_hay_bloques(bloques)
    sala = buscar_sala(letra_sala)
    for bloque in bloques:
        reglas.verificar_dia_y_bloque(fecha, bloque, ahora)
    canceladas = []
    with transaction.atomic():
        for bloque in bloques:
            canceladas += poner_en_mantenimiento(administrador, sala, fecha, bloque, ahora)
    return canceladas

def todas_las_salas():
    return list(Sala.objects.order_by("letra"))