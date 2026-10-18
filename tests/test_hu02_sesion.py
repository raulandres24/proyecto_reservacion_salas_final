import pytest
from django.contrib.messages import get_messages
from django.urls import reverse

from conftest import CONTRASENA
from cuentas.models import Usuario

pytestmark = pytest.mark.django_db(transaction=True)

MENSAJE_UNICO = "Correo o contraseña incorrectos"


def datos_de_la_cuenta(codigo):
    return Usuario.objects.filter(codigo=codigo).values(
        "correo", "codigo", "nombre", "rol", "nivel", "matricula_al_dia", "password"
    ).get()


def test_HU02_CA1_inicia_sesion_con_correo_y_contrasena(client, valeria):
    cuenta_antes = datos_de_la_cuenta("31245")

    respuesta = client.post(
        reverse("login"), {"correo": "valeria.rojas@upb.example", "contrasena": CONTRASENA}
    )

    assert respuesta.status_code == 302
    assert respuesta.wsgi_request.user.codigo == "31245"
    assert datos_de_la_cuenta("31245") == cuenta_antes


def test_HU02_CA2_contrasena_incorrecta_da_mensaje_unico(client, valeria):
    con_contrasena_incorrecta = client.post(
        reverse("login"), {"correo": "valeria.rojas@upb.example", "contrasena": "otra-clave-999"}
    )
    con_correo_inexistente = client.post(
        reverse("login"), {"correo": "nadie@upb.example", "contrasena": CONTRASENA}
    )

    for respuesta in (con_contrasena_incorrecta, con_correo_inexistente):
        mensajes = [str(mensaje) for mensaje in get_messages(respuesta.wsgi_request)]
        assert mensajes == [MENSAJE_UNICO]
        assert not respuesta.wsgi_request.user.is_authenticated
