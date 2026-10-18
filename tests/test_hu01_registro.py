import pytest
from django.contrib.auth import authenticate

from cuentas import servicios
from cuentas.models import Usuario
from cuentas.padron import leer_padron
from reservas.reglas import Rechazo

pytestmark = pytest.mark.django_db(transaction=True)

CONTRASENA = "clave-segura-123"


def test_HU01_CA1_registra_cuenta_con_codigo_y_correo_del_padron():
    padron_antes = leer_padron()

    cuenta = servicios.registrar("31245", "valeria.rojas@upb.example", CONTRASENA)

    assert cuenta.codigo == "31245"
    assert cuenta.rol == "estudiante"
    assert cuenta.nivel == "pregrado"
    assert authenticate(username="valeria.rojas@upb.example", password=CONTRASENA) == cuenta
    assert leer_padron() == padron_antes


def test_HU01_CA2_rechaza_registro_de_persona_inactiva():
    padron_antes = leer_padron()

    with pytest.raises(Rechazo) as error:
        servicios.registrar("31248", "diego.vargas@upb.example", CONTRASENA)

    assert error.value.causa == "persona no activa en el padrón"
    assert Usuario.objects.count() == 0
    assert leer_padron() == padron_antes
