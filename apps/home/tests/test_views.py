import datetime

from django.shortcuts import redirect
from django.urls import reverse

from apps.home.forms import BookingForm
from apps.home.models import Room, Booking
from django.test import TestCase


class BookingTest(TestCase):
    def setUp(self):
        self.room_type = Room.objects.create(name='Deluxe')
        self.room = Room.objects.create(name='Egypt',
                                        number=101,
                                        room_type=self.room_type,
                                        price_per_night=150.00)

    # Check: the booking creation page opens and contains a valid BookingForm
    def test_correct_operation_of_booking_create_and_form(self):
        response = self.client.get('/booking/create/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], BookingForm)


class BookingTest2(TestCase):
    def setUp(self):
        self.room_type = Room.objects.create(name='Deluxe')
        self.room = Room.objects.create(name='Egypt',
                                        number=101,
                                        room_type=self.room_type,
                                        price_per_night=150.00)

    # Tests creating a booking with valid data
    def test_post_creates_booking_with_valid_data(self):
        form_data = {
            'name': 'Alex',
            'room': str(self.room.id),
            'rooms_count': 1,
            'start_date': '2025-09-09',
            'end_date': '2025-09-11',
            'guest_count': 2,
            'phone': '+380974637685',
        }

        response = self.client.post('/booking/create/', data=form_data)
        self.assertEqual(response.status_code, 302)

        booking = Booking.objects.get(name='Alex')
        self.assertEqual(booking.room, self.room)
        self.assertEqual(booking.check_in.isoformat(), '2025-09-09')
        self.assertEqual(booking.check_out.isoformat(), '2025-09-11')
        self.assertEqual(booking.guests, 2)
        self.assertEqual(booking.phone, '+380974637685')


class BookingTest3(TestCase):
    def setUp(self):
        self.room_type = Room.objects.create(name='Deluxe')
        self.room = Room.objects.create(name='Egypt',
                                        number=101,
                                        room_type=self.room_type,
                                        price_per_night=150.00)

    #Checks for redirect to confirmation page after successful booking
    def test_after_post_good_working_redirect(self):
        form_data = {
            'name': 'Alex',
            'room': str(self.room.id),
            'rooms_count': 1,
            'start_date': '2025-09-09',
            'end_date': '2025-09-11',
            'guest_count': 2,
            'phone': '+380974637685',
        }
        response = self.client.post('/booking/create/', data=form_data)
        self.assertEqual(response.status_code, 302)

        self.assertRedirects(response, '/booking/1/confirmation/')


class BookingTest4(TestCase):
    def setUp(self):
        self.room_type = Room.objects.create(name='Deluxe')
        self.room = Room.objects.create(
            name='Egypt',
            number=101,
            room_type=self.room_type,
            price_per_night=150.00
        )
        self.booking = Booking.objects.create(
            name='Alex',
            phone='+380974637685',
            start_date=datetime.date(2025, 9, 9),
            end_date=datetime.date(2025, 9, 11),
            room=self.room,
            rooms_count=2,
            guest_count=2
        )

    # Checks that booking confirmation page displays booking details (name, dates, price).
    def test_booking_confirmation_displays_booking_details(self):
        booking = self.booking

        url = reverse('home:booking_confirmation', args=[booking.id])
        response = self.client.get(url)

        self.assertContains(response, 'Sept. 9, 2025')
        self.assertContains(response, 'Sept. 11, 2025')
        self.assertContains(response, '300.00')
        self.assertContains(response, 'Alex')


class BookingTest5(TestCase):
    def setUp(self):
        self.room_type = Room.objects.create(name='Deluxe')
        self.room = Room.objects.create(name='Egypt',
                                        number=101,
                                        room_type=self.room_type,
                                        price_per_night=150.00)

    #Checks that accessing booking confirmation page with nonexistent ID returns 404.
    def test_booking_confirmation_returns_404_for_nonexistent_booking(self):
        non_existent_id = 999
        url = reverse('home:booking_confirmation', args=[non_existent_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
