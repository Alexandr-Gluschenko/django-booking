from datetime import datetime

from django.shortcuts import redirect
from django.urls import reverse

from django.contrib.auth import get_user_model
from apps.home.forms import BookingForm
from apps.home.models import Room, Booking, Hotel
from django.test import TestCase
from django.test import Client


User = get_user_model()

class BookingTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

        self.client.login(username='testuser', password='testpass')

        self.hotel = Hotel.objects.create(
            name="Hilton",
            country="Turkey",
            city="Istanbul",
            address="Main Street 1",
            description="Luxury hotel"
        )
        self.room = Room.objects.create(name='Egypt',
                                        hotel=self.hotel,
                                        number=101,
                                        price_per_night=150.00)

    # Check: the booking creation page opens and contains a valid BookingForm
    def test_correct_operation_of_booking_create_and_form(self):
        response = self.client.get('/bookings/create/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], BookingForm)


class BookingTest2(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(username='testuser', password='testpass')

        self.client.login(username='testuser', password='testpass')

        self.hotel = Hotel.objects.create(
            name="Hilton",
            country="Turkey",
            city="Istanbul",
            address="Main Street 1",
            description="Luxury hotel"
        )

        self.room = Room.objects.create(name='Egypt',
                                        hotel=self.hotel,
                                        number=101,
                                        price_per_night=150.00)

    # Tests creating a booking with valid data
    def test_post_creates_booking_with_valid_data(self):
        form_data = {
            'room': self.room.id,
            'check_in': '2025-12-10',
            'check_out': '2025-12-12',
            'guests': 1,
            'phone': '+380974637685',
        }

        response = self.client.post('/bookings/create/', data=form_data)
        self.assertEqual(response.status_code, 302)

        booking = Booking.objects.get(user=self.user)
        self.assertEqual(booking.room, self.room)
        self.assertEqual(booking.check_in.isoformat(), '2025-12-10T00:00:00+00:00')
        self.assertEqual(booking.check_out.isoformat(), '2025-12-12T00:00:00+00:00')
        self.assertEqual(booking.guests, 1)
        self.assertEqual(booking.phone, '+380974637685')


class BookingTest3(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

        self.client.login(username='testuser', password='testpass')

        self.hotel = Hotel.objects.create(
            name="Hilton",
            country="Turkey",
            city="Istanbul",
            address="Main Street 1",
            description="Luxury hotel"
        )

        self.room = Room.objects.create(
            name='Egypt',
            hotel=self.hotel,
            number=101,
            price_per_night=150.00
        )

    def test_after_post_good_working_redirect(self):
        form_data = {
            'name': 'Alex',
            'room': self.room.id,
            'check_in': '2025-12-10',
            'check_out': '2025-12-15',
            'guests': 1,
            'phone': '+380974637685',
        }

        response = self.client.post('/bookings/create/', data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/booking/1/confirmation/')



class BookingTest4(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(username='Alex', password='testpass')

        self.hotel = Hotel.objects.create(
            name="Hilton",
            country="Turkey",
            city="Istanbul",
            address="Main Street 1",
            description="Luxury hotel"
        )

        self.room = Room.objects.create(
            hotel=self.hotel,
            name="Deluxe",
            number=101,
            price_per_night=150.00,
            max_guests=2,
            status="available",
        )

        self.booking = Booking.objects.create(
            user=self.user,
            phone='+380974637685',
            room=self.room,
            check_in=datetime(2025, 12, 10),
            check_out=datetime(2025, 12, 12),
        )

    # Checks that booking confirmation page displays booking details (name, dates, price).
    def test_booking_confirmation_displays_booking_details(self):
        booking = self.booking

        url = reverse('home:booking_confirmation', args=[booking.id])
        response = self.client.get(url)

        self.assertContains(response, 'Dec. 10, 2025')
        self.assertContains(response, 'Dec. 12, 2025')
        self.assertContains(response, 'Total price:')
        self.assertContains(response, '300.00')
        self.assertContains(response, 'Alex')

class BookingTest5(TestCase):
    def setUp(self):
        self.hotel = Hotel.objects.create(
            name="Hilton",
            country="Turkey",
            city="Istanbul",
            address="Main Street 1",
            description="Luxury hotel"
        )

        self.room = Room.objects.create(hotel=self.hotel,
                                        name='Egypt',
                                        number=101,
                                        price_per_night=150.00,
                                        max_guests=10,
                                        status="available",
                                        )

    #Checks that accessing booking confirmation page with nonexistent ID returns 404.
    def test_booking_confirmation_returns_404_for_nonexistent_booking(self):
        non_existent_id = 999
        url = reverse('home:booking_confirmation', args=[non_existent_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
