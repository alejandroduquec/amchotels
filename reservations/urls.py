"""Reservations URLs."""

# Django
from django.urls import path

# View
from reservations import views


urlpatterns = [

    path(
        route='',
        view=views.IndexView.as_view(),
        name='login'
    ),
  

]