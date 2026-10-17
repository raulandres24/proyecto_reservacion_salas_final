from django.db import models

# Create your models here.
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class UsuarioManager(BaseUserManager):
    def create_user(self, correo, password=None, **campos):
        usuario = self.model(correo=self.normalize_email(correo), **campos)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

class Usuario(AbstractBaseUser):
    class Rol(models.TextChoices):
        ESTUDIANTE = "estudiante", "Estudiante"
        DOCENTE = "docente", "Docente"
        ADMINISTRADOR = "administrador", "Administrador"

    class Nivel(models.TextChoices):
        PREGRADO = "pregrado", "Pregrado"
        POSGRADO = "posgrado", "Posgrado"

    correo = models.EmailField(unique=True)
    codigo = models.CharField(max_length=5, unique=True)
    nombre = models.CharField(max_length=150)
    rol = models.CharField(max_length=15, choices=Rol.choices)
    nivel = models.CharField(max_length=10, choices=Nivel.choices, blank=True)
    matricula_al_dia = models.BooleanField(default=False)

    USERNAME_FIELD = "correo"
    REQUIRED_FIELDS = ["codigo", "nombre", "rol"]

    objects = UsuarioManager()

    def __str__(self):
        return self.correo