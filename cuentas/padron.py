import json

from django.conf import settings

RUTA_DEL_PADRON = settings.BASE_DIR / "padron" / "padron.json"


def leer_padron():
    with open(RUTA_DEL_PADRON, encoding="utf-8") as archivo:
        return json.load(archivo)


def buscar_por_codigo(codigo):
    for persona in leer_padron():
        if persona["codigo"] == codigo:
            return persona
    return None