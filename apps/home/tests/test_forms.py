import datetime
from apps.home.forms import BookingForm
from apps.home.models import Room, RoomType
from django.test import TestCase


class BookingFormTest(TestCase):
    def setUp(self):
        self.room_type = RoomType.objects.create(name='Deluxe')

        self.room = Room.objects.create(name='Deluxe',
                                        number=101,
                                        room_type=self.room_type,
                                        price_per_night=150.00
                                        )

    # Check: The booking form is valid when all required fields are provided with correct data
    def test_booking_form_valid_with_correct_data(self):
        form_data = {
            'name': 'Alex',
            'room': str(self.room.id),
            'rooms_count': 1,
            'start_date': datetime.date.today(),
            'end_date': datetime.date.today() + datetime.timedelta(days=2),
            'guest_count': 2,
            'phone': '+380974637685',
        }
        form = BookingForm(data=form_data)
        form.fields['room'].queryset = Room.objects.all()

        self.assertTrue(form.is_valid())


class BookingFormTest2(TestCase):
    def setUp(self):
        room_type = RoomType.objects.create(name='Deluxe')
        room = Room.objects.create(name='Deluxe',
                                   number=101,
                                   room_type=room_type,
                                   price_per_night=150.00)

    # Check: Booking form fails without required fields
    def test_booking_form_fails_when_required_fields_missing(self):
        form_data = BookingForm(data={
            'name': '',
            'phone': '',
            'start_date': '',
            'end_date': '',
            'room': '',
        })

        self.assertFalse(form_data.is_valid())

        self.assertIn('name', form_data.errors)
        self.assertIn('phone', form_data.errors)
        self.assertIn('start_date', form_data.errors)
        self.assertIn('end_date', form_data.errors)
        self.assertIn('room', form_data.errors)


class BookingFormTest3(TestCase):
    def setUp(self):
        self.room_type = RoomType.objects.create(name='Deluxe')
        self.room = Room.objects.create(name='Deluxe',
                                   number=101,
                                   room_type=self.room_type,
                                   price_per_night=150.00)

    # Booking form fails if end_date is earlier than start_date
    def test_booking_form_invalid_if_end_date_before_start_date(self):
        form_data = BookingForm(data={
            'name': 'Alex',
            'phone': '+380974637685',
            'start_date': datetime.date(2025, 9, 11),
            'end_date': datetime.date(2025, 9, 9),
            'room': str(self.room.id)
        })

        self.assertFalse(form_data.is_valid())

        self.assertIn('__all__', form_data.errors)


class BookingFormTest4(TestCase):
    def setUp(self):
        self.room_type = RoomType.objects.create(name='Deluxe')
        self.room = Room.objects.create(name='Deluxe',
                                        number=101,
                                        room_type=self.room_type,
                                        price_per_night=150.00)

    # Check: phone field is validated (only digits and minimum length)
    def test_phone_field_only_digits_and_min_length(self):
        form_data = BookingForm(data={
            'name': 'Alex',
            'phone': '+38097Lgrd',
            'start_date': datetime.date(2025, 9, 9),
            'end_date': datetime.date(2025, 9, 11),
            'room': str(self.room.id)
        })

        form = BookingForm(data=form_data)
        form.fields['room'].queryset = Room.objects.all()

        self.assertFalse(form_data.is_valid())

        self.assertIn('phone', form_data.errors)