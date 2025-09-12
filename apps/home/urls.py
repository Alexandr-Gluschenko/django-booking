from django.urls import path, re_path
from apps.home import views
from apps.home.views import BookingCreateView, IndexView, BookingConfirmationView, PagesView, HotelsPageView, \
    AboutUsView

app_name = "home"

urlpatterns = [

    # The home page
    path('', IndexView.as_view(), name='index'),
    path('<str:hotel>_hotel/', HotelsPageView.as_view(), name='hotel_page'),
    path('about_us/', AboutUsView.as_view(), name='about_us'),
        path("booking/<int:booking_id>/confirmation/", BookingConfirmationView.as_view(), name="booking_confirmation"),
    re_path(r'^.*\.*', PagesView.as_view(), name='pages'),
]
