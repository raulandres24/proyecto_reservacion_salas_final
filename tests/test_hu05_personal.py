import pytest

from reservas import servicios
from reservas.models import Reserva
from reservas.reglas import Rechazo

pytestmark = pytest.mark.django_db(transaction=True)


def test_HU05_CA1_docente_reserva_sala_a_sin_limite_de_anticipacion(ana, salas, hora, fecha):
    servicios.crear_reserva(ana, "A", fecha(23), 2, 5, hora(19, 10, 30))

    reserva = Reserva.objects.get()
    assert reserva.dueno == ana
    assert reserva.sala == salas["A"]
    assert reserva.fecha == fecha(23)
    assert reserva.bloque == 2
    assert reserva.asistentes == 5
    assert reserva.estado == Reserva.Estado.CONFIRMADA


def test_HU05_CA2_rechaza_reserva_en_sabado(ana, salas, hora, fecha):
    with pytest.raises(Rechazo) as error:
        servicios.crear_reserva(ana, "C", fecha(24), 2, 3, hora(23, 10, 0))

    assert error.value.causa == "no hay atención ese día"
    assert Reserva.objects.count() == 0
