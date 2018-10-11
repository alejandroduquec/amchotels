"""Reservations forms """

#Django
from django import forms 

#model
from django.contrib.auth.models import User
from reservations.models import *

class ReservationsForms(forms.ModelForm):
    """Form for reservations"""
    class Meta:
        model=Reservations
        fields=[
            'name_guest',
            'telephone_guest',
            'city_guest',
            'id_guest',
            'check_in',
            'check_out',
            'nights',
            'number_adults',
            'number_childs',
            'rate',
            'commission',
            'total',
            'total_amc',
            'observations',
        ]
        labels={
            'name_guest':'Nombre ',
            'telephone_guest':'Teléfono ',
            'city_guest':'Ciudad ',
            'id_guest':'Cédula',
            'check_in':'Check In',
            'check_out':'Check Out',
            'nights':'Noches de Estadía',
            'number_adults':'Número de Adultos',
            'number_childs':'Número de Niños',
            'rate':'Tarifa',
            'commission':'Porcentaje de Comisión',
            'total':'Total',
            'total_amc':'AMC Ingresos',
            'observations':'Observaciones',
        }
        widgets={
            'name_guest':forms.TextInput(attrs={'class':'form-control'}),
            'telephone_guest':forms.TextInput(attrs={'class':'form-control','type':'number'}),
            'city_guest':forms.TextInput(attrs={'class':'form-control'}),
            'id_guest':forms.TextInput(attrs={'class':'form-control'}),
            'check_in':forms.TextInput(attrs={'class':'form-control'}),
            'check_out':forms.TextInput(attrs={'class':'form-control'}),
            'nights':forms.TextInput(attrs={'class':'form-control','type':'number'}),
            'number_adults':forms.TextInput(attrs={'class':'form-control','type':'number'}),
            'number_childs':forms.TextInput(attrs={'class':'form-control','type':'number'}),
            'rate':forms.TextInput(attrs={'class':'form-control','type':'number'}),
            'commission':forms.TextInput(attrs={'class':'form-control','type':'number'}),
            'total':forms.TextInput(attrs={'class':'form-control','type':'number'}),
            'total_amc':forms.TextInput(attrs={'class':'form-control','type':'number'}),
            'Observaciones':forms.Textarea(attrs={'class':'form-control'}),
            }

