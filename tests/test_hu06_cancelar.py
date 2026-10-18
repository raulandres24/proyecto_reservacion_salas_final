import pytest

from reservas import servicios
from reservas.models import Reserva
from reservas.reglas import Rechazo

pytestmark = pytest.mark.django_db(transaction=True)

MIERCOLES = 21
JUEVES = 22
BLOQUE_2 = 2
BLOQUE_3 = 3


def test_HU06_CA1_cancela_antes_de_que_empiece_y_conserva_el_registro(
    valeria, salas, dar_reserva, hora, fecha
):
    # Dado: Valeria tiene la sala B el jueves en el bloque 2, y hoy es miércoles, 19:00
    reserva = dar_reserva(valeria, "B", JUEVES, BLOQUE_2)

    # Cuando: la cancela
    servicios.cancelar_reserva(valeria, reserva.pk, hora(MIERCOLES, 19))

    # Entonces: queda Cancelada "por el dueño", el registro se conserva y la sala B queda libre
    reserva.refresh_from_db()
    assert reserva.estado == Reserva.Estado.CANCELADA
    assert reserva.motivo_cancelacion == Reserva.MotivoCancelacion.POR_EL_DUENO
    assert reserva.sala == salas["B"]
    assert reserva.fecha == fecha(JUEVES)
    assert reserva.bloque == BLOQUE_2
    assert Reserva.objects.count() == 1
    confirmadas = Reserva.objects.filter(
        sala=salas["B"], fecha=fecha(JUEVES), bloque=BLOQUE_2,
        estado=Reserva.Estado.CONFIRMADA,
    )
    assert not confirmadas.exists()


def test_HU06_CA2_rechaza_cancelar_reserva_ya_comenzada(valeria, dar_reserva, hora):
    # Dado: Valeria tiene la sala B el jueves en el bloque 2, y hoy es jueves a las 10:00 en punto
    reserva = dar_reserva(valeria, "B", JUEVES, BLOQUE_2)

    # Cuando: intenta cancelarla
    with pytest.raises(Rechazo) as error:
        servicios.cancelar_reserva(valeria, reserva.pk, hora(JUEVES, 10))

    # Entonces: se rechaza y la reserva sigue Confirmada
    assert error.value.causa == "la reserva ya comenzó"
    reserva.refresh_from_db()
    assert reserva.estado == Reserva.Estado.CONFIRMADA


def test_HU06_CA3_rechaza_cancelar_reserva_ajena(valeria, mateo, dar_reserva, hora):
    # Dado: Mateo tiene la sala D el jueves en el bloque 3, y hoy es miércoles, 19:00
    reserva_de_mateo = dar_reserva(mateo, "D", JUEVES, BLOQUE_3)

    # Cuando: Valeria intenta cancelar la reserva de Mateo
    with pytest.raises(Rechazo) as error:
        servicios.cancelar_reserva(valeria, reserva_de_mateo.pk, hora(MIERCOLES, 19))

    # Entonces: se rechaza y la reserva de Mateo sigue Confirmada
    assert error.value.causa == "la reserva no es tuya"
    reserva_de_mateo.refresh_from_db()
    assert reserva_de_mateo.estado == Reserva.Estado.CONFIRMADA