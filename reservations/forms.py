"""Reservations forms """

#Django
from django import forms 
from django.db.models import Q
#model
from django.contrib.auth.models import User
from reservations.models import *
#Utils
import sweetify
from sweetify.views import SweetifySuccessMixin

class ReservationsForms(forms.ModelForm):
    """Form for reservations"""
    class Meta:
        model=Reservations
        fields=[
            'id_room',
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

            'id_user_register',
            'id_user_modify',
        ]
        labels={
            'id_room':'Seleccione Habitación',
            'name_guest':'Nombre Completo',
            'telephone_guest':'Teléfono ',
            'city_guest':'Ciudad ',
            'id_guest':'Cédula',
            'check_in':'Check In',
            'check_out':'Check Out',
            'nights':'Noches de Estadía',
            'number_adults':'Número de Adultos',
            'number_childs':'Número de Niños',
            'rate':'Tarifa por Noche',
            'commission':'Porcentaje de Comisión',
            'total':'Total',
            'total_amc':'AMC Ingresos',
            'observations':'Observaciones',
        }
        widgets={
            'id_room':forms.Select(attrs={'class':'form-control'}),  
            'name_guest':forms.TextInput(attrs={'class':'form-control'}),
            'telephone_guest':forms.TextInput(attrs={'class':'form-control','type':'number'}),
            'city_guest':forms.TextInput(attrs={'class':'form-control'}),
            'id_guest':forms.TextInput(attrs={'class':'form-control','type':'number'}),
            'check_in':forms.DateInput(attrs={'class':'form-control'}),
            'check_out':forms.DateInput(attrs={'class':'form-control'}),
            'nights':forms.TextInput(attrs={'class':'form-control','type':'number'}),
            'number_adults':forms.TextInput(attrs={'class':'form-control','type':'number'}),
            'number_childs':forms.TextInput(attrs={'class':'form-control','type':'number'}),
            'rate':forms.TextInput(attrs={'class':'form-control','type':'number','onchange':'CalcleTotal()'}),
            'commission':forms.TextInput(attrs={'class':'form-control','type':'number','onchange':'CalcleTotalAmc()'}),
            'total':forms.TextInput(attrs={'class':'form-control','type':'number'}),
            'total_amc':forms.TextInput(attrs={'class':'form-control','type':'number'}),
            'observations':forms.Textarea(attrs={'class':'form-control'}),

            'id_user_register':forms.HiddenInput(),
            'id_user_modify':forms.HiddenInput(),
            }
                
class HotelsForms(forms.Form):
    """hotels form to consult the room"""
    hotel=forms.ModelChoiceField(queryset=Hotels.objects.filter(),empty_label="------",label='Seleccionar Hotel', widget=forms.Select(attrs={'class':'form-control','onchange':'SelectRoom()' }))
    

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)

        super(HotelsForms, self).__init__(*args, **kwargs)

        if self.instance:
            self.initial['hotel'] = self.instance
    
class ReportsForms(forms.Form):
    """Report Form by critery """
    MONTH_CHOICE=((1,'Enero'),(2,'Febrero'),(3,'Marzo'),(4,'Abril'),(5,'Mayo'),(6,'Junio'),(7,'Julio'),(8,'Agosto'),(9,'Septiembre'),(10,'Octubre'),(11,'Noviembre'),(12,'Diciembre'))
    CRITERY_CHOICE=((1,'Por día'),(2,'Semanal'),(3,'Mensual'))
    critery=forms.ChoiceField(choices=CRITERY_CHOICE,label='Criterio de Reporte', widget=forms.Select(attrs={'class':'form-control'}), required= True)
    hotel=forms.ModelChoiceField(queryset=Hotels.objects.filter(),empty_label="------",label='Seleccionar Hotel', widget=forms.Select(attrs={'class':'form-control'}),required= True)
    
    day=forms.CharField(label='Seleccionar día',widget=forms.DateInput(attrs={'class':'form-control','id':'single_cal3'}),required= False)
    weaks=forms.CharField(label='Seleccionar Rango de Fechas',widget=forms.DateInput(attrs={'class':'form-control','id':'reservation'}),required= False)
    month=forms.ChoiceField(choices= MONTH_CHOICE,initial={'max_number': '3'},label='Seleccionar Mes', widget=forms.Select(attrs={'class':'form-control'}),required= False)
    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)

        super(ReportsForms, self).__init__(*args, **kwargs)

        if self.instance:
            self.initial['month'] = self.instance
    


