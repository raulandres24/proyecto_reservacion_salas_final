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


def test_HU07_CA1_modifica_el_bloque_de_la_misma_reserva(
    valeria, mateo, dar_reserva, hora, fecha
):
    # Dado: hoy es miércoles, 19:00; Valeria tiene la sala B el jueves, bloque 2, y Mateo, bloque 3
    reserva_de_valeria = dar_reserva(valeria, "B", JUEVES, BLOQUE_2, ASISTENTES)
    reserva_de_mateo = dar_reserva(mateo, "B", JUEVES, BLOQUE_3, ASISTENTES)

    # Cuando: Valeria mueve su reserva al bloque 4
    modificada = servicios.modificar_reserva(
        valeria, reserva_de_valeria.pk, fecha(JUEVES), BLOQUE_4, ASISTENTES, hora(MIERCOLES, 19)
    )

    # Entonces: la misma reserva queda en el bloque 4, Confirmada y con 3 asistentes,
    # y la de Mateo no cambia
    assert modificada.pk == reserva_de_valeria.pk
    assert Reserva.objects.count() == 2
    verificar_reserva_guardada(reserva_de_valeria, BLOQUE_4)
    verificar_reserva_guardada(reserva_de_mateo, BLOQUE_3)


def test_HU07_CA2_rechazo_y_si_conserva_ambas_reservas(
    valeria, mateo, dar_reserva, hora, fecha
):
    # Dado: hoy es miércoles, 19:00; Valeria tiene la sala B el jueves, bloque 2, y Mateo, bloque 3
    reserva_de_valeria = dar_reserva(valeria, "B", JUEVES, BLOQUE_2, ASISTENTES)
    reserva_de_mateo = dar_reserva(mateo, "B", JUEVES, BLOQUE_3, ASISTENTES)

    # Cuando: Valeria intenta moverla al bloque 3
    with pytest.raises(Rechazo) as error:
        servicios.modificar_reserva(
            valeria, reserva_de_valeria.pk, fecha(JUEVES), BLOQUE_3, ASISTENTES, hora(MIERCOLES, 19)
        )

    # Entonces: se rechaza con la pregunta "¿Deseas mantenerla?"; con "Sí", ambas siguen igual
    assert error.value.causa == "sala ocupada en ese bloque"
    assert error.value.preguntar_si_mantener is True
    verificar_reserva_guardada(reserva_de_valeria, BLOQUE_2)
    verificar_reserva_guardada(reserva_de_mateo, BLOQUE_3)


def test_HU07_CA3_rechazo_y_no_cancela_la_original(
    valeria, mateo, dar_reserva, hora, fecha
):
    # Dado: hoy es miércoles, 19:00; Valeria tiene la sala B el jueves, bloque 2, y Mateo, bloque 3
    reserva_de_valeria = dar_reserva(valeria, "B", JUEVES, BLOQUE_2, ASISTENTES)
    reserva_de_mateo = dar_reserva(mateo, "B", JUEVES, BLOQUE_3, ASISTENTES)

    # Cuando: Valeria intenta moverla al bloque 3 y responde "No" a "¿Deseas mantenerla?"
    with pytest.raises(Rechazo) as error:
        servicios.modificar_reserva(
            valeria, reserva_de_valeria.pk, fecha(JUEVES), BLOQUE_3, ASISTENTES, hora(MIERCOLES, 19)
        )
    assert error.value.causa == "sala ocupada en ese bloque"
    servicios.no_mantener_reserva(valeria, reserva_de_valeria.pk)

    # Entonces: su reserva queda Cancelada "no la mantuvo", con los datos del bloque 2,
    # y la de Mateo no cambia
    verificar_reserva_guardada(reserva_de_valeria, BLOQUE_2, estado=Reserva.Estado.CANCELADA)
    assert reserva_de_valeria.motivo_cancelacion == Reserva.MotivoCancelacion.NO_LA_MANTUVO
    verificar_reserva_guardada(reserva_de_mateo, BLOQUE_3)


def test_HU07_CA4_rechaza_modificar_reserva_ya_comenzada(valeria, dar_reserva, hora, fecha):
    # Dado: hoy es jueves a las 10:00 en punto; Valeria tiene la sala B ese día en el bloque 2
    reserva_de_valeria = dar_reserva(valeria, "B", JUEVES, BLOQUE_2, ASISTENTES)

    # Cuando: intenta moverla al bloque 4
    with pytest.raises(Rechazo) as error:
        servicios.modificar_reserva(
            valeria, reserva_de_valeria.pk, fecha(JUEVES), BLOQUE_4, ASISTENTES, hora(JUEVES, 10)
        )

    # Entonces: se rechaza sin pregunta y la reserva sigue en el bloque 2
    assert error.value.causa == "la reserva ya comenzó"
    assert error.value.preguntar_si_mantener is False
    verificar_reserva_guardada(reserva_de_valeria, BLOQUE_2)