from datetime import timezone

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader, TemplateDoesNotExist
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from django import forms
from django.views.generic import TemplateView


from apps.home.forms import BookingForm
from apps.home.models import Booking, Room, Hotel, RoomType


class IndexView(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "index"
        return context


class PagesView(TemplateView):
    def get_template_names(self):
        load_template = self.request.path.split('/')[-1]

        if load_template == "admin":
            return HttpResponseRedirect(reverse('admin:index'))

        try:
            return [f"home/{load_template}"]
        except TemplateDoesNotExist:
            return [f"home/page-404.html"]


class BookingCreateView(CreateView):
    model = Booking
    form_class = BookingForm
    template_name = "home/booking_create.html"

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
        form.instance.price_per_night = form.instance.room.price_per_night
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse_lazy("home:booking_confirmation", kwargs={"booking_id": self.object.id})


class BookingConfirmationView(DetailView):
    model = Booking
    template_name = "home/confirmation.html"
    context_object_name = "hotels"


class HotelListView(ListView):
    model = Hotel
    template_name = 'home/hotel_page.html'


class AboutUsView(TemplateView):
    template_name = "home/about-us.html"


class BookingListView(ListView):
    model = Booking
    template_name = "home/booking_list.html"
    context_object_name = "bookings"

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)


class UserBookingView(ListView):
    model = Booking
    template_name = "home/bookings.html"
    context_object_name = "bookings"

    def get_queryset(self):
        user = self.request.user
        today = timezone.now().date()

        queryset = Booking.objects.filter(user=user)

        filter_type = self.request.GET.get("filter")
        if filter_type == "past":
            queryset = queryset.filter(check_out__lt=today, status="accepted")
        elif filter_type == "future":
            queryset = queryset.filter(check_in__gte=today, status="accepted")
        elif filter_type == "cancelled":
            queryset = queryset.filter(status="cancelled")

        return queryset.order_by("-check_in")


class RoomTypeListView(ListView):
    model = RoomType
    template_name = "home/room_type_list.html"
    context_object_name = "room_types"


class RoomListView(ListView):
    model = Room
    template_name = "home/room_list.html"
    context_object_name = "rooms"


class RoomDetailView(DetailView):
    model = Room
    template_name = "home/room_detail.html"
    context_object_name = "room"
