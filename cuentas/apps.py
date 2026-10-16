from django.apps import AppConfig


class CuentasConfig(AppConfig):
    default_auto_field = 'django_mongodb_backend.fields.ObjectIdAutoField'
    name = 'cuentas'