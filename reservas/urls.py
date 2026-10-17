from django.urls import path

from . import views

urlpatterns = [
    path("salas-libres/", views.salas_libres, name="salas_libres"),
    path("reservar/", views.reservar, name="reservar"),
    path("mis-reservas/", views.ver_mis_reservas, name="mis_reservas"),
    path("cancelar/<str:reserva_id>/", views.cancelar, name="cancelar"),
    path("modificar/<str:reserva_id>/", views.modificar, name="modificar"),
    path("no-mantener/<str:reserva_id>/", views.no_mantener, name="no_mantener"),
]