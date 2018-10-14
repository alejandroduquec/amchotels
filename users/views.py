""" Users  views """
#django
from django.shortcuts import render
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin

class LoginView(auth_views.LoginView):
    """Login view"""
    template_name='base/login.html'

class LogoutView(LoginRequiredMixin,auth_views.LogoutView):
    """logout view"""
    template_name='users/login.html'