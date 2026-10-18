import pytest

from reservas import servicios
from reservas.models import Reserva
from reservas.reglas import Rechazo

pytestmark = pytest.mark.django_db(transaction=True)


def test_HU04_CA1_reserva_a_las_18_en_punto_para_el_dia_siguiente(valeria, salas, hora, fecha):
    servicios.crear_reserva(valeria, "C", fecha(22), 2, 3, hora(21, 18, 0))

    reserva = Reserva.objects.get()
    assert reserva.dueno == valeria
    assert reserva.sala == salas["C"]
    assert reserva.fecha == fecha(22)
    assert reserva.bloque == 2
    assert reserva.asistentes == 3
    assert reserva.estado == Reserva.Estado.CONFIRMADA


def test_HU04_CA2_rechaza_si_choca_con_otra_reserva(valeria, mateo, salas, dar_reserva, hora, fecha):
    reserva_de_mateo = dar_reserva(mateo, "C", 22, 2)

    with pytest.raises(Rechazo) as error:
        servicios.crear_reserva(valeria, "C", fecha(22), 2, 3, hora(21, 18, 5))

    assert error.value.causa == "sala ocupada en ese bloque"
    assert list(Reserva.objects.filter(sala=salas["C"])) == [reserva_de_mateo]


def test_HU04_CA3_acepta_bloque_siguiente_con_15_min_de_desalojo(
    valeria, mateo, salas, dar_reserva, hora, fecha
):
    dar_reserva(mateo, "B", 22, 1)

    servicios.crear_reserva(valeria, "B", fecha(22), 2, 3, hora(21, 18, 5))

    reservas_de_b = Reserva.objects.filter(sala=salas["B"])
    assert sorted((reserva.dueno.codigo, reserva.bloque) for reserva in reservas_de_b) == [
        ("31245", 2),
        ("31246", 1),
    ]


def test_HU04_CA4_rechaza_segunda_reserva_en_el_mismo_bloque(valeria, dar_reserva, hora, fecha):
    reserva_de_valeria = dar_reserva(valeria, "B", 22, 2)

    with pytest.raises(Rechazo) as error:
        servicios.crear_reserva(valeria, "C", fecha(22), 2, 3, hora(21, 18, 5))

    assert error.value.causa == "ya tienes una reserva en ese bloque"
    assert list(Reserva.objects.all()) == [reserva_de_valeria]


def test_HU04_CA5_rechaza_bloques_seguidos_en_otra_sala(valeria, dar_reserva, hora, fecha):
    reserva_de_valeria = dar_reserva(valeria, "B", 22, 2)

    with pytest.raises(Rechazo) as error:
        servicios.crear_reserva(valeria, "C", fecha(22), 3, 3, hora(21, 18, 5))

    assert error.value.causa == "no puedes reservar dos bloques seguidos"
    assert list(Reserva.objects.all()) == [reserva_de_valeria]


def test_HU04_CA6_rechaza_si_matricula_no_esta_al_dia(lucia, salas, hora, fecha):
    with pytest.raises(Rechazo) as error:
        servicios.crear_reserva(lucia, "C", fecha(22), 2, 3, hora(21, 18, 5))

    assert error.value.causa == "matrícula no vigente"
    assert Reserva.objects.count() == 0


def test_HU04_CA7_rechaza_si_supera_la_capacidad(valeria, salas, hora, fecha):
    with pytest.raises(Rechazo) as error:
        servicios.crear_reserva(valeria, "B", fecha(22), 2, 5, hora(21, 18, 5))

    assert error.value.causa == "capacidad superada"
    assert Reserva.objects.count() == 0
