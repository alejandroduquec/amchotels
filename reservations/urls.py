"""Reservations URLs."""

# Django
from django.urls import path

# View
from reservations import views


urlpatterns = [

    path(
        route='',
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
  

]