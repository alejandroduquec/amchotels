""" Models for users"""
#Django
from django.db import models
from django.contrib.auth.models import User
#Models
from reservations.models import Hotels

class Profile(models.Model):
    """Profile model that extends from user model"""
    user=models.OneToOneField(User,on_delete=models.DO_NOTHING)

    ROLE_CHOICES=(
        (1,'Administrador'),
        (2,'Operador'),
        (3,'Consulta')
        )
    role=models.PositiveIntegerField(choices=ROLE_CHOICES)

    created=models.DateTimeField(auto_now_add=True)
    modified=models.DateTimeField(auto_now=True)
    operator_hotel = models.ForeignKey(
        Hotels,
        blank=True,
        null=True,
        on_delete = models.DO_NOTHING)

    def __str__(self):
        """Return username when call the profile"""
        return self.user.username
    