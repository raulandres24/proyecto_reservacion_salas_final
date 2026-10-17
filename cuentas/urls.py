from django.urls import path

from . import views

urlpatterns = [
    path("registro/", views.registrarse, name="registro"),
    path("login/", views.iniciar_sesion, name="login"),
    path("logout/", views.cerrar_sesion, name="logout"),
]