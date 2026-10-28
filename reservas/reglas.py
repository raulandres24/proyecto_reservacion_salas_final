from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

ZONA_HORARIA = ZoneInfo("America/La_Paz")

BLOQUES = {
    1: (time(7, 45), time(9, 45)),
    2: (time(10, 0), time(12, 0)),
    3: (time(12, 15), time(14, 15)),
    4: (time(14, 30), time(16, 30)),
    5: (time(16, 45), time(18, 45)),
    6: (time(19, 0), time(21, 0)),
}
CAUSA_SALA_OCUPADA = "sala ocupada en ese bloque"
CAUSA_BLOQUE_REPETIDO = "ya tienes una reserva en ese bloque"


class Rechazo(Exception):
    def __init__(self, causa, preguntar_si_mantener=False):
        super().__init__(causa)
        self.causa = causa
        self.preguntar_si_mantener = preguntar_si_mantener


def verificar_capacidad(sala, asistentes):
    if asistentes < 1:
        raise Rechazo("los asistentes deben ser 1 o más")
    if asistentes > sala.capacidad:
        raise Rechazo("capacidad superada")


def verificar_sala_libre(sala_ocupada):
    if sala_ocupada:
        raise Rechazo(CAUSA_SALA_OCUPADA)


def verificar_un_bloque_por_persona(bloques_del_dueno, bloque):
    if bloque in bloques_del_dueno:
        raise Rechazo(CAUSA_BLOQUE_REPETIDO)


def es_estudiante(usuario):
    return usuario.rol == "estudiante"


def verificar_matricula(dueno):
    if es_estudiante(dueno) and not dueno.matricula_al_dia:
        raise Rechazo("matrícula no vigente")


def puede_usar_sala(usuario, sala):
    if es_estudiante(usuario) and usuario.nivel == "pregrado":
        return sala.nivel == "pregrado"
    return True


def verificar_nivel_de_sala(dueno, sala):
    if not puede_usar_sala(dueno, sala):
        raise Rechazo("sala no disponible para tu nivel")


def verificar_sin_mantenimiento(hay_mantenimiento):
    if hay_mantenimiento:
        raise Rechazo("sala en mantenimiento")

# --------------------------------------------------------------------------------------------------------

def inicio_del_bloque(fecha, bloque):
    hora_de_inicio = BLOQUES[bloque][0]
    return datetime.combine(fecha, hora_de_inicio, tzinfo=ZONA_HORARIA)


def ya_comenzo(fecha, bloque, ahora):
    return ahora >= inicio_del_bloque(fecha, bloque)


def verificar_no_comenzada(reserva, ahora):
    if ya_comenzo(reserva.fecha, reserva.bloque, ahora):
        raise Rechazo("la reserva ya comenzó")


def verificar_dia_y_bloque(fecha, bloque, ahora):
    if fecha.weekday() >= 5:
        raise Rechazo("no hay atención ese día")
    if bloque not in BLOQUES:
        raise Rechazo("el bloque no existe")
    if ya_comenzo(fecha, bloque, ahora):
        raise Rechazo("el bloque ya empezó")


HORA_DE_APERTURA = time(18, 0)
DIAS = ("lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo")


def hoy(ahora):
    return ahora.astimezone(ZONA_HORARIA).date()


def dia_de_clase_anterior(fecha):
    anterior = fecha - timedelta(days=1)
    while anterior.weekday() >= 5:
        anterior -= timedelta(days=1)
    return anterior


def verificar_anticipacion(dueno, fecha, ahora):
    if not es_estudiante(dueno) or fecha == hoy(ahora):
        return
    anterior = dia_de_clase_anterior(fecha)
    apertura = datetime.combine(anterior, HORA_DE_APERTURA, tzinfo=ZONA_HORARIA)
    if ahora < apertura:
        raise Rechazo(
            f"las reservas para el {DIAS[fecha.weekday()]} "
            f"se abren el {DIAS[anterior.weekday()]} a las 18:00"
        )


def verificar_bloques_no_seguidos(dueno, bloques_del_dueno, bloque):
    if not es_estudiante(dueno):
        return
    if bloque - 1 in bloques_del_dueno or bloque + 1 in bloques_del_dueno:
        raise Rechazo("no puedes reservar dos bloques seguidos")


def comprobar_reserva(
        dueno, sala, fecha, bloque, asistentes, ahora,
        sala_ocupada, hay_mantenimiento, bloques_del_dueno,
):
    verificar_matricula(dueno)
    verificar_dia_y_bloque(fecha, bloque, ahora)
    verificar_anticipacion(dueno, fecha, ahora)
    verificar_nivel_de_sala(dueno, sala)
    verificar_sin_mantenimiento(hay_mantenimiento)
    verificar_capacidad(sala, asistentes)
    verificar_sala_libre(sala_ocupada)
    verificar_un_bloque_por_persona(bloques_del_dueno, bloque)
    verificar_bloques_no_seguidos(dueno, bloques_del_dueno, bloque)


def es_administrador(usuario):
    return usuario.rol == "administrador"


def es_dueno(reserva, usuario):
    return reserva.dueno_id == usuario.pk


def verificar_es_administrador(usuario):
    if not es_administrador(usuario):
        raise Rechazo("solo el administrador puede hacer esto")


def verificar_confirmada(reserva):
    if reserva.estado != "confirmada":
        raise Rechazo("la reserva ya está cancelada")


def verificar_dueno(reserva, usuario):
    if not es_dueno(reserva, usuario):
        raise Rechazo("la reserva no es tuya")


def verificar_puede_modificar(reserva, usuario, ahora):
    if not es_administrador(usuario):
        verificar_dueno(reserva, usuario)
    verificar_confirmada(reserva)
    verificar_no_comenzada(reserva, ahora)


def verificar_puede_cancelar(reserva, usuario, ahora):
    if es_administrador(usuario):
        verificar_confirmada(reserva)
        return
    verificar_dueno(reserva, usuario)
    verificar_confirmada(reserva)
    verificar_no_comenzada(reserva, ahora)


def motivo_de_cancelacion(usuario):
    if es_administrador(usuario):
        return "por_el_administrador"
    return "por_el_dueno"


def debe_preguntar_si_mantener(reserva, usuario):
    return es_dueno(reserva, usuario)


def verificar_persona_en_padron(persona):
    if persona is None:
        raise Rechazo("código no encontrado en el padrón")


def verificar_correo_del_padron(persona, correo):
    if persona["correo"].lower() != correo.lower():
        raise Rechazo("el correo no corresponde a ese código")


def verificar_persona_activa(persona):
    if not persona["activo"]:
        raise Rechazo("persona no activa en el padrón")


def verificar_sin_cuenta(ya_tiene_cuenta):
    if ya_tiene_cuenta:
        raise Rechazo("ya tienes una cuenta")


def verificar_contrasenas_iguales(contrasena, confirmacion):
    if contrasena != confirmacion:
        raise Rechazo("las contraseñas no coinciden")


def verificar_contrasena(contrasena, cuenta_nueva):
    try:
        validate_password(contrasena, user=cuenta_nueva)
    except ValidationError as error:
        raise Rechazo(" ".join(error.messages))

def verificar_hay_bloques(bloques):
    if not bloques:
        raise Rechazo("elige al menos un bloque")
