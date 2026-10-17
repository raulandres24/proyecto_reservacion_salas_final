from django.core.management.base import BaseCommand

from reservas.models import Sala

SALAS = [
    ("A", 6, "posgrado"),
    ("B", 4, "pregrado"),
    ("C", 6, "pregrado"),
    ("D", 8, "pregrado"),
    ("E", 10, "posgrado"),
    ("F", 6, "pregrado"),
    ("H", 12, "pregrado"),
    ("J", 4, "pregrado"),
]


class Command(BaseCommand):
    help = "Carga las 8 salas. Se puede correr varias veces sin duplicar."

    def handle(self, *args, **opciones):
        for letra, capacidad, nivel in SALAS:
            sala, creada = Sala.objects.update_or_create(
                letra=letra, defaults={"capacidad": capacidad, "nivel": nivel}
            )
            self.stdout.write(f"{sala}: {'creada' if creada else 'actualizada'}")