from django.urls import path, re_path
from apps.home.views import BookingCreateView, IndexView, BookingConfirmationView, \
    AboutUsView, HotelListView, RoomListView, BookingListView, MyBookingsView, cancel_booking, \
    edit_booking

app_name = "home"

urlpatterns = [

    # The home page
    path('', IndexView.as_view(), name='index'),
    path('hotels/', HotelListView.as_view(), name='hotel_page'),
    path('about_us/', AboutUsView.as_view(), name='about_us'),
    # Rooms and types
    path('rooms/', RoomListView.as_view(), name='room_list'),
    # Bookings
    path('bookings/', BookingListView.as_view(), name='booking_list'),
    path('bookings/create/', BookingCreateView.as_view(), name='booking_create'),
    path('my-bookings/', MyBookingsView.as_view(), name='my_bookings'),
    path("booking/<int:booking_id>/confirmation/", BookingConfirmationView.as_view(), name="booking_confirmation"),
    path('booking/<int:pk>/cancel/', cancel_booking, name="booking_cancel"),
    path('booking/<int:pk>/edit/', edit_booking, name="booking_edit"),
]
