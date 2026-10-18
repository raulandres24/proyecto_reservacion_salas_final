import pytest

from reservas import servicios
from reservas.models import Mantenimiento, Reserva
from reservas.reglas import Rechazo

pytestmark = pytest.mark.django_db(transaction=True)

MIERCOLES = 21
JUEVES = 22
BLOQUE_2 = 2
BLOQUE_3 = 3


def test_HU08_CA1_mantenimiento_cancela_reservas_y_bloquea_el_periodo(
    valeria, mateo, sergio, salas, dar_reserva, hora, fecha
):
    # Dado: Valeria tiene la sala C el jueves en el bloque 2, y hoy es miércoles, 20:00
    reserva = dar_reserva(valeria, "C", JUEVES, BLOQUE_2)

    # Cuando: Sergio registra mantenimiento de la sala C el jueves, en los bloques 2 y 3
    servicios.registrar_mantenimiento(
        sergio, "C", fecha(JUEVES), [BLOQUE_2, BLOQUE_3], hora(MIERCOLES, 20)
    )

    # Entonces: la reserva de Valeria queda Cancelada "por mantenimiento" y, si Mateo pide
    # después la sala C en el bloque 3, se rechaza con "sala en mantenimiento"
    registrados = Mantenimiento.objects.filter(sala=salas["C"], fecha=fecha(JUEVES))
    assert sorted(mantenimiento.bloque for mantenimiento in registrados) == [BLOQUE_2, BLOQUE_3]
    reserva.refresh_from_db()
    assert reserva.estado == Reserva.Estado.CANCELADA
    assert reserva.motivo_cancelacion == Reserva.MotivoCancelacion.POR_MANTENIMIENTO
    with pytest.raises(Rechazo) as error:
        servicios.crear_reserva(mateo, "C", fecha(JUEVES), BLOQUE_3, 3, hora(MIERCOLES, 20, 5))
    assert error.value.causa == "sala en mantenimiento"
    assert Reserva.objects.count() == 1


def test_HU08_CA2_rechaza_mantenimiento_en_bloque_ya_empezado(
    valeria, sergio, dar_reserva, hora, fecha
):
    # Dado: Valeria tiene la sala C el jueves en el bloque 2, y hoy es jueves, 10:30
    reserva = dar_reserva(valeria, "C", JUEVES, BLOQUE_2)

    # Cuando: Sergio intenta registrar mantenimiento de la sala C en el bloque 2
    with pytest.raises(Rechazo) as error:
        servicios.registrar_mantenimiento(
            sergio, "C", fecha(JUEVES), [BLOQUE_2], hora(JUEVES, 10, 30)
        )

    # Entonces: se rechaza, no se registra el mantenimiento y la reserva de Valeria sigue Confirmada
    assert error.value.causa == "el bloque ya empezó"
    assert Mantenimiento.objects.count() == 0
    reserva.refresh_from_db()
    assert reserva.estado == Reserva.Estado.CONFIRMADA