""" Post views """
#Django
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
#Forms
from reservations.forms import * 

#Models
from reservations.models import *
from users.models import *


class IndexView(LoginRequiredMixin,FormView):
    template_name='dashboard/index.html'
    form_class=ReservationsForms