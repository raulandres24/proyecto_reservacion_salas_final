from django.apps import AppConfig


class ReservasConfig(AppConfig):
    default_auto_field = 'django_mongodb_backend.fields.ObjectIdAutoField'
    name = 'reservas'