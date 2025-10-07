from django.urls import path, re_path
from apps.home.views import BookingCreateView, IndexView, BookingConfirmationView, PagesView, \
    AboutUsView, HotelListView, RoomTypeListView, RoomListView, BookingListView, UserBookingView, RoomDetailView

app_name = "home"

urlpatterns = [

    # The home page
    path('', IndexView.as_view(), name='index'),
    path('hotels/', HotelListView.as_view(), name='hotel_page'),
    path('about_us/', AboutUsView.as_view(), name='about_us'),
    re_path(r'^.*\.*', PagesView.as_view(), name='pages'),
    # Rooms and types
    path('room-types/', RoomTypeListView.as_view(), name='room_type_list'),
    path('rooms/', RoomListView.as_view(), name='room_list'),
    path('rooms/<int:pk>/', RoomDetailView.as_view(), name='room_detail'),
    # Bookings
    path('bookings/', BookingListView.as_view(), name='booking_list'),
    path('bookings/create/', BookingCreateView.as_view(), name='booking_create'),
    path('my-bookings/', UserBookingView.as_view(), name='user_bookings'),
    path("booking/<int:booking_id>/confirmation/", BookingConfirmationView.as_view(), name="booking_confirmation"),
]
