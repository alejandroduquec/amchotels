""" Post views """
#Django
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView,TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
#Forms
from reservations.forms import * 

#Models
from reservations.models import *
from users.models import *
#urls
from reservations.urls import *
#Utils
import sweetify
from sweetify.views import SweetifySuccessMixin

@login_required
def RegisterReservationView(request):
    
    if request.method=='POST':
        form = ReservationsForms(request.POST)
        form2 = HotelsForms(request.POST)
        
        if form.is_valid() and form2.is_valid():
            data =form.cleaned_data
            check_in=data['check_in']
            check_out=data['check_out']
            id_room=data['id_room']

            if (check_out >= check_in):
                busy_room=Reservations.objects.filter(Q(id_room_id=id_room)&(Q(check_in__range=(check_in, check_out))|Q(check_out__range=(check_in, check_out))))
                busy_hotel=RestrictionHotels.objects.filter(Q(id_hotel=id_room.id_hotel.id)&(Q(date_on__range=(check_in, check_out))|Q(date_on__range=(check_in, check_out))))
                if busy_room or busy_hotel:
                    messages.error(request, "Habitación ocupada en el espacio de tiempo seleccionado!")
                else:
                    hotel=form2.cleaned_data['hotel'] 
                    form.save()
                    sweetify.success(request,'Registro Exitoso')
                    return redirect('reservations:calendar', hotel=hotel.id)
    else:
        form = ReservationsForms()
        form2 = HotelsForms()
        
    return render(request,'dashboard/register.html',{'form': form,'form2': form2})
def CalendarView(request,hotel):
    """Calendar view for each hotel information"""
    if hotel == 0:
        rooms=Rooms.objects.all()
        hotel_name='Todos los hoteles AMC'
    else:
        rooms=Rooms.objects.filter(id_hotel=hotel)
        hotel_name=Hotels.objects.get(id=hotel)
        

    reservations=Reservations.objects.filter(id_room__in=rooms)
    return render(request,'dashboard/calendar.html',{'reservations':reservations,'hotel_name':hotel_name})

class SelectorHotel(LoginRequiredMixin,ListView):
    """Selector hotel class to render all hotels info"""
    template_name='dashboard/selector_hotel.html'
    queryset=Hotels.objects.all()
    context_object_name='hotels'

def ajax_get_rooms(request):
    if request.method == 'POST':
        hotel=request.POST['hotel']
        rooms=Rooms.objects.filter(id_hotel=int(hotel))
        html_options=''
        for room in rooms:
            html_options += '<option value="{0}" label="{1}"></option>'.format(room.id,room.name)
        return HttpResponse(html_options)
