from datetime import date, datetime
from io import StringIO

import pytest
from django.core.management import call_command

from cuentas.models import Usuario
from reservas.models import Reserva, Sala
from reservas.reglas import ZONA_HORARIA

CONTRASENA = "clave-de-prueba-123"

@pytest.fixture
def hora():
    def armar(dia, horas, minutos=0):
        return datetime(2026, 10, dia, horas, minutos, tzinfo=ZONA_HORARIA)

    return armar

@pytest.fixture
def fecha():
    def armar(dia):
        return date(2026, 10, dia)

    return armar

@pytest.fixture
def salas(transactional_db):
    call_command("cargar_salas", stdout=StringIO())
    return {sala.letra: sala for sala in Sala.objects.all()}

def crear_persona(codigo, nombre, correo, rol, nivel="", matricula_al_dia=True):
    return Usuario.objects.create_user(
        correo=correo, password=CONTRASENA, codigo=codigo, nombre=nombre,
        rol=rol, nivel=nivel, matricula_al_dia=matricula_al_dia,
    )

@pytest.fixture
def valeria(transactional_db):
    return crear_persona(
        "31245", "Valeria Rojas", "valeria.rojas@upb.example", "estudiante", "pregrado"
    )

@pytest.fixture
def mateo(transactional_db):
    return crear_persona(
        "31246", "Mateo Suarez", "mateo.suarez@upb.example", "estudiante", "pregrado"
    )

@pytest.fixture
def lucia(transactional_db):
    return crear_persona(
        "31247", "Lucia Fernandez", "lucia.fernandez@upb.example", "estudiante",
        "pregrado", matricula_al_dia=False,
    )

@pytest.fixture
def ana(transactional_db):
    return crear_persona(
        "20101", "Ana Gutierrez", "ana.gutierrez@upb.example", "docente",
        matricula_al_dia=False,
    )

@pytest.fixture
def sergio(transactional_db):
    return crear_persona(
        "10001", "Sergio Barrientos", "adminsergio@upb.example", "administrador",
        matricula_al_dia=False,
    )

@pytest.fixture
def dar_reserva(salas):
    def dar(dueno, letra, dia, bloque, asistentes=3):
        return Reserva.objects.create(
            dueno=dueno, sala=salas[letra], fecha=date(2026, 10, dia),
            bloque=bloque, asistentes=asistentes,
        )
    return dar
