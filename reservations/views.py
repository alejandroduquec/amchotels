""" Post views """
#Django
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView,TemplateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.db.models import Count
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
import datetime
import string



class IndexView(LoginRequiredMixin,TemplateView):
    """View for Index"""
    template_name='dashboard/index.html'

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        hotels=Hotels.objects.all()
        context['hotels']=hotels
        reservations=Reservations.objects.all()
        context['reservations']=reservations
        context['rooms']=Rooms.objects.count()
        today=datetime.datetime.now()
        totalamc=0
        list_hotels=[0]*(len(hotels)+1)
        dic_money={}
        for i in hotels:
            dic_money[i.name] = 0
        for i in reservations:
            #the pay is efective when user doing checkout
            if i.check_out.month == today.month or i.check_in.month == today.month:
                totalamc += int(i.total_amc)
                
                list_hotels[i.id_room.id_hotel.id] += 1
                dic_money[i.id_room.id_hotel.name]+= int(i.total_amc)
        context['totalamc']=totalamc
        context['dic_money']=dic_money
        context['today']=today
        
        context['reservations_hotels']=list_hotels
        return context

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
                #busca en el rango de la resrva no tener una superposicón con otra
                #excepto si la fecha de entrada es igual a la de salida por calendario hotelero
                busy_room=Reservations.objects.filter(
                    Q(id_room_id=id_room)&
                    (Q(check_in__range=(check_in, check_out))|Q(check_out__range=(check_in, check_out)))
                    ).exclude(Q(id_room_id=id_room)&(Q(check_out=check_in)|Q(check_in=check_out)))
                if check_in == check_out and not busy_room:
                    day = check_in
                    busy_room = Reservations.objects.filter(
                        id_room_id=id_room,
                        check_in__lte=day,
                        check_out__gt=day)
                #hotel ocupado por evento 
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
@login_required
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

class Reports(LoginRequiredMixin,FormView):
    """Reports View"""
    template_name='dashboard/reports.html'
    form_class=ReportsForms
    
    def post(self, request, *args, **kwargs):
        """On post to report"""
        form = self.get_form()
       
        if form.is_valid():
            data=form.cleaned_data
            hotel=data['hotel']
            critery=data['critery']
            rooms=Rooms.objects.filter(id_hotel=hotel).values('id')
            if critery == '1':
                #day
                day=datetime.datetime.strptime(data['day'],'%m/%d/%Y').strftime('%Y-%m-%d')
                reservations=Reservations.objects.filter(Q(id_room__in=rooms)&(Q(check_in=day)|Q(check_out=day)))
            elif critery =='2':
                #weak
                range_date=data['weaks']
                start,end=range_date.split('-')
                start=start.replace(' ', '')
                end=end.replace(' ','')
                start=datetime.datetime.strptime(start,'%m/%d/%Y').strftime('%Y-%m-%d')
                end=datetime.datetime.strptime(end,'%m/%d/%Y').strftime('%Y-%m-%d')
                reservations=Reservations.objects.filter(Q(id_room__in=rooms)&(Q(check_in__range=(start, end))|Q(check_out__range=(start, end))))
            elif critery == '3':
                month=int(data['month'])
                reservations=Reservations.objects.filter(Q(id_room__in=rooms)&(Q(check_in__month=month)|Q(check_out__month=month)))
            if reservations:
                sweetify.success(self.request,'Búsqueda Exitosa.')
            else:
                sweetify.error(self.request,'Ningún resultado para el criterio seleccionado')

            return render(request, 'dashboard/reports.html', {'form': form ,'reservations':reservations})
                
            
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class UpdateReservation(LoginRequiredMixin,UpdateView):
    """Update view"""
    form_class = ReservationsForms
    template_name='dashboard/editor_register.html'
    second_form_class=HotelsForms

    def get_object(self, queryset=None):
        """return object to edit"""
        
        obj = Reservations.objects.get(id=self.kwargs['reservation'])
        return obj
    def get_context_data(self, *args, **kwargs):
        """overload the context to add second form"""
        context = super(UpdateReservation,self).get_context_data(*args, **kwargs)
        hotel=self.object.id_room.id_hotel
        if 'form2' not in context:
            #form overload with instance 
            context['form2'] = self.second_form_class(instance=hotel.id)
        return context

    def form_valid(self, form):
        """When form is valid check the schedule availability"""
        data=form.cleaned_data
        check_in=data['check_in']
        check_out=data['check_out']
        reservation=Reservations.objects.get(id=self.kwargs['reservation'])
        if (check_out >= check_in):
            busy_room=Reservations.objects.filter(Q(id_room_id=reservation.id_room)&(Q(check_in__range=(check_in, check_out))|Q(check_out__range=(check_in, check_out)))).exclude(id=reservation.id).exclude(Q(check_out=check_in)|Q(check_in=check_out))
            busy_hotel=RestrictionHotels.objects.filter(Q(id_hotel=reservation.id_room.id_hotel.id)&(Q(date_on__range=(check_in, check_out))|Q(date_on__range=(check_in, check_out)))).exclude(id=reservation.id)
            if busy_room or busy_hotel:
                messages.error(self.request, "Habitación ocupada en el espacio de tiempo seleccionado!")
                return self.form_invalid(form)
        return super(UpdateReservation, self).form_valid(form)

    def get_success_url(self):
        """Returno to hotel schedule"""
        room=self.object.id_room.id_hotel.id
        sweetify.success(self.request,'Edición Exitosa')
        return reverse_lazy('reservations:calendar', kwargs={'hotel':room})

class DeleteReservationView(LoginRequiredMixin,DeleteView):
    """Delete View"""
    template_name='dashboard/delete_confirmation.html'
    context_object_name='reservation'

    def get_object(self, queryset=None):
        """Get object to delete"""
        obj = Reservations.objects.get(id=self.kwargs['reservation'])
        return obj
    def get_success_url(self):
        """Returno to hotel schedule"""
        room=self.object.id_room.id_hotel.id
        
        sweetify.success(self.request,'Reserva Eliminada')
        return reverse_lazy('reservations:calendar', kwargs={'hotel':room})


def ajax_get_rooms(request):
    """Ajax to return the rooms for each hotel"""
    if request.method == 'POST':
        hotel=request.POST['hotel']
        rooms=Rooms.objects.filter(id_hotel=int(hotel))
        html_options=''
        for room in rooms:
            html_options += '<option value="{0}" label="{1}"></option>'.format(room.id,room.name)
        return HttpResponse(html_options)
