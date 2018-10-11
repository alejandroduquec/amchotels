"""AMC urls """
#Django 
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('users/', include(('users.urls','users'),namespace='users')),
    path('reservas/', include(('reservations.urls','reservations'),namespace='reservations')),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)