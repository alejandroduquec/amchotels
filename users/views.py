""" Users  views """
#django
from django.shortcuts import render , redirect,resolve_url
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.urls import reverse_lazy
#models
from reservations.urls import *

class LoginView(auth_views.LoginView):
    """Login view"""
    template_name='base/login.html'
    def get_success_url(self):
        role=self.request.user.profile.role
        if role  in [3 ,2]:
            return resolve_url('reservations:selector')
        elif role == 1:
            url = self.get_redirect_url()
            return resolve_url(settings.LOGIN_REDIRECT_URL)
        

        

class LogoutView(LoginRequiredMixin,auth_views.LogoutView):
    """logout view"""
    template_name='users/login.html'