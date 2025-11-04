from datetime import timezone, datetime
from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django import template
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from django import forms
from django.views.generic import TemplateView
from django.contrib import messages

from apps.home.forms import BookingForm, BookSearchForm
from apps.home.models import Booking, Room, Hotel


class IndexView(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "index"
        return context


class BookingCreateView(CreateView):
    model = Booking
    form_class = BookingForm
    template_name = "home/booking_create.html"
    login_url = '/login/'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        room_id = self.request.GET.get('room_id')

        if room_id:
            qs = Room.objects.filter(pk=room_id)
            form.fields['room'].queryset = qs
            form.fields['room'].initial = qs.first()
            form.fields['room'].widget = forms.HiddenInput()
        else:
            form.fields['room'].queryset = Room.objects.all()
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.price_per_night = form.instance.room.price_per_night
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse_lazy("home:booking_confirmation", kwargs={"booking_id": self.object.id})


class BookingConfirmationView(DetailView):
    model = Booking
    template_name = "home/confirmation.html"
    context_object_name = "booking"
    pk_url_kwarg = "booking_id"


class HotelListView(ListView):
    model = Hotel
    template_name = 'home/hotel_page.html'
    context_object_name = 'hotels'

    def get_context_data(self, *, object_list =None, **kwargs):
        context = super(HotelListView, self).get_context_data(**kwargs)
        context["search_form"] = BookSearchForm()
        return context


class AboutUsView(TemplateView):
    template_name = "home/about-us.html"


class BookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'bookings_list.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)


class RoomListView(ListView):
    model = Room
    template_name = "home/room_list.html"
    context_object_name = "rooms"


@method_decorator(login_required, name="dispatch")
class MyBookingsView(ListView):
    model = Booking
    template_name = "home/my_bookings.html"
    context_object_name = "bookings"

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by("-id")

@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    booking.status = "cancelled"
    booking.save()
    messages.success(request, "Your booking has been cancelled.")
    return redirect("home:my_bookings")

@login_required
def edit_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)

    if request.method == "POST":
        check_in_str = request.POST.get("check_in")
        check_out_str = request.POST.get("check_out")

        new_check_in = datetime.strptime(check_in_str, "%Y-%m-%d").date()
        new_check_out = datetime.strptime(check_out_str, "%Y-%m-%d").date()

        if not booking.room.is_available(new_check_in, new_check_out, exclude_booking_id=booking.pk):
            messages.error(request, "The room is not available for these dates.")
            return render(request, "home/edit_booking.html", {"booking": booking})

        booking.check_in = new_check_in
        booking.check_out = new_check_out
        booking.save()
        messages.success(request, "Booking updated successfully.")
        return redirect("home:my_bookings")

    return render(request, "home/edit_booking.html", {"booking": booking})