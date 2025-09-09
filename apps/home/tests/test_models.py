import datetime

from apps.home.models import Room, RoomType, Booking
from django.test import TestCase


class RoomModelTest(TestCase):
    def setUp(self):
        self.room_type = RoomType.objects.create(name="Deluxe")

    # Check: The room is created with the correct type and price
    def test_room_creation_with_type_and_price(self):
        room = Room.objects.create(
            name="Egypt",
            number=101,
            room_type=self.room_type,
            price_per_night=150.00
        )


        self.assertEqual(room.name, "Egypt")
        self.assertEqual(room.number, 101)
        self.assertEqual(room.price_per_night, 150.00)
        self.assertEqual(room.room_type, self.room_type)

class BookingModelTest(TestCase):
    def setUp(self):
        self.room_type = RoomType.objects.create(name="Deluxe")

        self.room = Room.objects.create(
            name="Egypt",
            number=101,
            room_type=self.room_type,
            price_per_night=150.00
        )

    # Check: the booking is saved with correct data in all fields
    def test_booking_creation_with_all_fields(self):
        booking = Booking.objects.create(
            name="Alex",
            room=self.room,
            rooms_count=1,
            start_date=datetime.date(2025, 9, 9),
            end_date=datetime.date(2025, 9, 11),
            guest_count=2,
            phone="+380974637685"
        )

        self.assertEqual(booking.name, "Alex")
        self.assertEqual(booking.room, self.room)
        self.assertEqual(booking.rooms_count, 1)
        self.assertEqual(booking.start_date, datetime.date(2025, 9, 9))
        self.assertEqual(booking.end_date, datetime.date(2025, 9, 11))
        self.assertEqual(booking.guest_count, 2)
        self.assertEqual(booking.phone, "+380974637685")


class BookingModelPriceTest(TestCase):
    def setUp(self):
        self.room_type = RoomType.objects.create(name="Deluxe")

        self.room = Room.objects.create(
            name="Egypt",
            number=101,
            room_type=self.room_type,
            price_per_night=150.00)

    #Checking the correct calculation of the booking cost
    def test_checking_price_correctly(self):
        booking = Booking.objects.create(
            room=self.room,
            start_date=datetime.date(2025, 9, 9),
            end_date=datetime.date(2025, 9, 11),
            name="Alex"
        )

        self.assertEqual(booking.price_per_night, 150.00)

        num_nights = (booking.end_date - booking.start_date).days
        expected_total = num_nights * booking.room.price_per_night

        self.assertEqual(booking.total_price(), expected_total)

