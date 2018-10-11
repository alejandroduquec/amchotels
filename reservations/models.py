"""reservations models"""
#Django
from django.db import models
from django.contrib.auth.models import User

class Hotels(models.Model):
    """hotel model"""
    name=models.CharField(max_length=255)
    ubication=models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        """returrn hotel name"""
        return self.name
    
class RestrictionHotels(models.Model):
    """Restriction model for days off """
    id_hotel=models.ForeignKey(Hotels,on_delete=models.DO_NOTHING)
    date_on=models.DateTimeField()
    date_off=models.DateTimeField()

    #metadata
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    id_user_register=models.ForeignKey(User,related_name='user_register_restriction', on_delete=models.DO_NOTHING)
    id_user_modify=models.ForeignKey(User,related_name='user_modify_restriction',on_delete=models.DO_NOTHING, blank=True, null=True)

class Rooms(models.Model):
    """Rooms model"""
    name=models.CharField(max_length=255)
    number=models.CharField(max_length=10)
    id_hotel=models.ForeignKey(Hotels,on_delete=models.DO_NOTHING)
    tipo = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        """returrn room name"""
        return self.name

class Reservations(models.Model):
    """ Reservations Model"""
    id_room = models.ForeignKey(Rooms,on_delete=models.DO_NOTHING)
    name_guest=models.CharField(max_length=255)
    telephone_guest=models.CharField(max_length=255)
    city_guest = models.CharField(max_length=255, blank=True, null=True)
    id_guest= models.CharField(max_length=255)
    check_in= models.DateField()
    check_out= models.DateField()
    nights=models.IntegerField()
    number_adults=models.PositiveIntegerField(default=1)
    number_childs=models.PositiveIntegerField(default=0,blank=True, null=True)
    rate= models.FloatField()
    commission=models.FloatField()
    total=models.FloatField()
    total_amc = models.FloatField()
    observations=models.CharField(max_length=500)


    #metadata
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    id_user_register=models.ForeignKey(User,related_name='user_register_reservation', on_delete=models.DO_NOTHING)
    id_user_modify=models.ForeignKey(User,related_name='user_modify_reservation', blank=True, null=True, on_delete=models.DO_NOTHING)




