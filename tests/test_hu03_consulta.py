import pytest

from reservas import servicios
from reservas.models import Mantenimiento, Reserva
from reservas.reglas import Rechazo

pytestmark = pytest.mark.django_db(transaction=True)


def foto_de_la_base():
    reservas = list(Reserva.objects.order_by("pk").values())
    mantenimientos = list(Mantenimiento.objects.order_by("pk").values())
    return reservas, mantenimientos


def test_HU03_CA1_muestra_salas_libres_sin_a_ni_e_y_no_modifica_datos(
    valeria, mateo, dar_reserva, hora, fecha
):
    dar_reserva(mateo, "B", 22, 2)
    base_antes = foto_de_la_base()

    salas_libres = servicios.consultar_salas_libres(valeria, fecha(22), 2, hora(21, 18, 5))

    assert [sala.letra for sala in salas_libres] == ["C", "D", "F", "H", "J"]
    assert foto_de_la_base() == base_antes


def test_HU03_CA2_antes_de_las_18_no_muestra_el_dia_siguiente(valeria, hora, fecha):
    base_antes = foto_de_la_base()

    with pytest.raises(Rechazo) as error:
        servicios.consultar_salas_libres(valeria, fecha(22), 1, hora(21, 17, 59))

    assert error.value.causa == "las reservas para el jueves se abren el miércoles a las 18:00"
    assert foto_de_la_base() == base_antes
