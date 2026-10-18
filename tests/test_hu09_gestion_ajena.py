import pytest

from reservas import servicios
from reservas.models import Reserva
from reservas.reglas import Rechazo

pytestmark = pytest.mark.django_db(transaction=True)

MIERCOLES = 21
JUEVES = 22
BLOQUE_2 = 2
BLOQUE_3 = 3
BLOQUE_4 = 4
ASISTENTES = 3


def verificar_reserva_guardada(reserva, bloque, estado=Reserva.Estado.CONFIRMADA):
    reserva.refresh_from_db()
    assert reserva.bloque == bloque
    assert reserva.asistentes == ASISTENTES
    assert reserva.estado == estado


def test_HU09_CA1_admin_rechazado_sin_pregunta_conserva_ambas(
    valeria, mateo, sergio, dar_reserva, hora, fecha
):
    # Dado: hoy es miércoles, 19:00; Valeria tiene la sala B el jueves, bloque 2, y Mateo, bloque 3
    reserva_de_valeria = dar_reserva(valeria, "B", JUEVES, BLOQUE_2, ASISTENTES)
    reserva_de_mateo = dar_reserva(mateo, "B", JUEVES, BLOQUE_3, ASISTENTES)

    # Cuando: Sergio, el administrador, intenta mover la reserva de Valeria al bloque 3
    with pytest.raises(Rechazo) as error:
        servicios.modificar_reserva(
            sergio, reserva_de_valeria.pk, fecha(JUEVES), BLOQUE_3, ASISTENTES, hora(MIERCOLES, 19)
        )

    # Entonces: se rechaza sin preguntar "¿Deseas mantenerla?" y las dos reservas quedan igual
    assert error.value.causa == "sala ocupada en ese bloque"
    assert error.value.preguntar_si_mantener is False
    verificar_reserva_guardada(reserva_de_valeria, BLOQUE_2)
    verificar_reserva_guardada(reserva_de_mateo, BLOQUE_3)


def test_HU09_CA2_admin_aplica_reglas_del_dueno(valeria, sergio, dar_reserva, hora, fecha):
    # Dado: hoy es miércoles, 19:00; Valeria tiene la sala B en el bloque 2 y la sala C en el 4
    reserva_en_sala_b = dar_reserva(valeria, "B", JUEVES, BLOQUE_2, ASISTENTES)
    reserva_en_sala_c = dar_reserva(valeria, "C", JUEVES, BLOQUE_4, ASISTENTES)

    # Cuando: Sergio intenta mover la reserva del bloque 4 al bloque 3 (la sala C está libre)
    with pytest.raises(Rechazo) as error:
        servicios.modificar_reserva(
            sergio, reserva_en_sala_c.pk, fecha(JUEVES), BLOQUE_3, ASISTENTES, hora(MIERCOLES, 19)
        )

    # Entonces: se rechaza por las reglas de Valeria, la dueña, y sus dos reservas quedan igual
    assert error.value.causa == "no puedes reservar dos bloques seguidos"
    verificar_reserva_guardada(reserva_en_sala_b, BLOQUE_2)
    verificar_reserva_guardada(reserva_en_sala_c, BLOQUE_4)