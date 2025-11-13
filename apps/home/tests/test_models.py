import datetime

from django.contrib.auth import get_user_model
from apps.home.models import Room, Booking, Hotel
from django.test import TestCase


User = get_user_model()

class RoomModelTest(TestCase):
    def test_room_creation_with_type_and_price(self):
        room = Room.objects.create(
            hotel=Hotel.objects.create(
                name="Test Hotel",
                country="Egypt",
                city="Cairo",
                address="Main Street 1",
                description="A nice place"
            ),
            name="Egypt",
            number=101,
            price_per_night=150.00,
            max_guests=10,
            status="available",
        )

        room.amenities.set([])

        self.assertEqual(room.name, "Egypt")
        self.assertEqual(room.number, 101)
        self.assertEqual(room.price_per_night, 150.00)
        self.assertEqual(room.max_guests, 10)
        self.assertEqual(room.status, "available")
        self.assertEqual(room.amenities.count(), 0)


class BookingModelTest(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(username='Alex', password='testpass')

        self.hotel = Hotel.objects.create(
            name="Test Hotel",
            country="Egypt",
            city="Cairo",
            address="Main Street 1",
            description="A nice place"
        )

        self.room = Room.objects.create(
            hotel=self.hotel,
            name="Deluxe",
            number=101,
            price_per_night=150.00,
            max_guests=2,
            status="available",
        )

    # Check: the booking is saved with correct data in all fields
    def test_booking_creation_with_all_fields(self):
        booking = Booking.objects.create(
            user=self.user,
            room=self.room,
            check_in=datetime.date(2025, 9, 9),
            check_out=datetime.date(2025, 9, 11),
            guests=2,
            phone="+380974637685"
        )

        self.assertEqual(booking.user.username, "Alex")
        self.assertEqual(booking.room, self.room)
        self.assertEqual(booking.check_in, datetime.date(2025, 9, 9))
        self.assertEqual(booking.check_out, datetime.date(2025, 9, 11))
        self.assertEqual(booking.guests, 2)
        self.assertEqual(booking.phone, "+380974637685")


class BookingModelPriceTest(TestCase):
    def setUp(self):
        
        self.user = User.objects.create_user(username='testuser', password='testpass')

        self.hotel = Hotel.objects.create(
            name="Test Hotel",
            country="Egypt",
            city="Cairo",
            address="Main Street 1",
            description="A nice hotel for testing"
        )

        self.room = Room.objects.create(
            hotel=self.hotel,
            name="Deluxe",
            number=101,
            price_per_night=150.00,
            max_guests=2,
            status="available"
        )

    #Checking the correct calculation of the booking cost
    def test_checking_price_correctly(self):
    
        booking = Booking.objects.create(
            user=self.user,
            room=self.room,
            check_in=datetime.date(2025, 9, 9),
            check_out=datetime.date(2025, 9, 11),
            phone="+380985453232",
        )

        self.assertEqual(self.room.price_per_night, 150.00)

        num_nights = (booking.check_out - booking.check_in).days
        expected_total = num_nights * booking.room.price_per_night

        self.assertEqual(booking.total_price, expected_total)

