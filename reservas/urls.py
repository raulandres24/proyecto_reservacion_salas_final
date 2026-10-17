from django.urls import path

from . import views

urlpatterns = [
    path("salas-libres/", views.salas_libres, name="salas_libres"),
]