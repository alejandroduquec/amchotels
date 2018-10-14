"""Reservations URLs."""

# Django
from django.urls import path

# View
from reservations import views


urlpatterns = [
    path(
        route='',
        view=views.IndexView.as_view(),
        name='index'
    ),

    path(
        route='registrar/',
        view=views.RegisterReservationView,
        name='register'
    ),
    path(
        route='ajax_get_rooms',
        view=views.ajax_get_rooms,
        name='ajax_get_rooms'
    ),
    path(
        route='calendario/<int:hotel>/',
        view=views.CalendarView,
        name='calendar'
    ),
     path(
        route='selector/',
        view=views.SelectorHotel.as_view(),
        name='selector'
    ),
    path(
        route='edicion_reserva/<int:reservation>/',
        view=views.UpdateReservation.as_view(),
        name='edition'
    ),
    path(
        route='borrar_reserva/<int:reservation>/',
        view=views.DeleteReservationView.as_view(),
        name='delete'
    ),
  

]