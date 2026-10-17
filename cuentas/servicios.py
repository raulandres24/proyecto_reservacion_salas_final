from reservas import reglas
from reservas.reglas import Rechazo

from .models import Usuario
from .padron import buscar_por_codigo

def ya_tiene_cuenta(persona):
    return Usuario.objects.filter(codigo=persona["codigo"]).exists()

def cuenta_desde_el_padron(persona):
    return Usuario(
        correo=Usuario.objects.normalize_email(persona["correo"]),
        codigo=persona["codigo"],
        nombre=persona["nombre"],
        rol=persona["rol"],
        nivel=persona["nivel"],
        matricula_al_dia=persona["matricula_al_dia"],
    )

def registrar(codigo, correo, contrasena):
    persona = buscar_por_codigo(codigo)
    reglas.verificar_persona_en_padron(persona)
    reglas.verificar_correo_del_padron(persona, correo)
    reglas.verificar_persona_activa(persona)
    reglas.verificar_sin_cuenta(ya_tiene_cuenta(persona))
    cuenta = cuenta_desde_el_padron(persona)
    reglas.verificar_contrasena(contrasena, cuenta)
    cuenta.set_password(contrasena)
    cuenta.save()
    return cuenta