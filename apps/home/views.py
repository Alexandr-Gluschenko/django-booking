from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView
from django import forms


from apps.home.forms import BookingForm
from apps.home.models import Booking, Room


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))


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


def create_booking(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
    if form.is_valid():
        booking = form.save()
        return redirect("home:booking_confirmation", booking_id=booking.id)
    else:
        form = BookingForm()
        return render(request, 'home/booking_create.html', {'form': form})


def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    return render(request, "home/confirmation.html", {'booking': booking})


def turkey_hotel(request):
    return render(request, 'home/turkey_hotel.html')

def egypt_hotel(request):
    return render(request, 'home/egypt_hotel.html')
def odessa_hotel(request):
    return render(request, 'home/odessa_hotel.html')
def thailand_hotel(request):
    return render(request, 'home/thailand_hotel.html')

def about_us(request):
    return render(request, 'home/about-us.html')