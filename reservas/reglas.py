from datetime import time

BLOQUES = {
    1: (time(7, 45), time(9, 45)),
    2: (time(10, 0), time(12, 0)),
    3: (time(12, 15), time(14, 15)),
    4: (time(14, 30), time(16, 30)),
    5: (time(16, 45), time(18, 45)),
    6: (time(19, 0), time(21, 0)),
}


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
        raise Rechazo("sala ocupada en ese bloque")

def verificar_un_bloque_por_persona(bloques_del_dueno, bloque):
    if bloque in bloques_del_dueno:
        raise Rechazo("ya tienes una reserva en ese bloque")

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