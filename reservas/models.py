from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q


class Sala(models.Model):
    class Nivel(models.TextChoices):
        PREGRADO = "pregrado", "Pregrado"
        POSGRADO = "posgrado", "Posgrado"

    letra = models.CharField(max_length=1, unique=True)
    capacidad = models.PositiveSmallIntegerField()
    nivel = models.CharField(max_length=10, choices=Nivel.choices)

    def __str__(self):
        return f"Sala {self.letra}"


class Reserva(models.Model):
    class Estado(models.TextChoices):
        CONFIRMADA = "confirmada", "Confirmada"
        CANCELADA = "cancelada", "Cancelada"

    class MotivoCancelacion(models.TextChoices):
        POR_EL_DUENO = "por_el_dueno", "Por el dueño"
        NO_LA_MANTUVO = "no_la_mantuvo", "No la mantuvo"
        POR_EL_ADMINISTRADOR = "por_el_administrador", "Por el administrador"
        POR_MANTENIMIENTO = "por_mantenimiento", "Por mantenimiento"

    dueno = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    sala = models.ForeignKey(Sala, on_delete=models.PROTECT)
    fecha = models.DateField()
    bloque = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)]
    )
    asistentes = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    estado = models.CharField(
        max_length=10, choices=Estado.choices, default=Estado.CONFIRMADA
    )
    motivo_cancelacion = models.CharField(
        max_length=25, choices=MotivoCancelacion.choices, blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["sala", "fecha", "bloque"],
                condition=Q(estado="confirmada"),
                name="una_reserva_confirmada_por_sala_fecha_bloque",
            ),
            models.UniqueConstraint(
                fields=["dueno", "fecha", "bloque"],
                condition=Q(estado="confirmada"),
                name="una_reserva_confirmada_por_dueno_fecha_bloque",
            ),
        ]

    def __str__(self):
        return f"{self.sala} · {self.fecha} · B{self.bloque}"


class Mantenimiento(models.Model):
    sala = models.ForeignKey(Sala, on_delete=models.PROTECT)
    fecha = models.DateField()
    bloque = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)]
    )
    registrado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    registrado_en = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["sala", "fecha", "bloque"],
                name="un_mantenimiento_por_sala_fecha_bloque",
            ),
        ]

    def __str__(self):
        return f"{self.sala} · {self.fecha} · B{self.bloque}"