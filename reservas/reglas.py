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