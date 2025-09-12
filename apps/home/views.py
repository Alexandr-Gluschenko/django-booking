from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader, TemplateDoesNotExist
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView
from django import forms
from django.views.generic import TemplateView


from apps.home.forms import BookingForm
from apps.home.models import Booking, Room



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


class HotelsPageView(TemplateView):
    def get_template_names(self):
        hotel = self.kwargs.get('hotel')
        return [f"home/{hotel}_hotel.html"]


class AboutUsView(TemplateView):
    template_name = "home/about-us.html"