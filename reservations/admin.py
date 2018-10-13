"""Reservations admin classes"""
#Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

#models
from users.models import *
from reservations.models import *

admin.site.register(Hotels)
admin.site.register(Rooms)
admin.site.register(RestrictionHotels)