import datetime
from apps.home.forms import BookingForm
from apps.home.models import Room, Hotel, Booking
from django.test import TestCase


class BookingFormTest(TestCase):
    def setUp(self):
        self.hotel = Hotel.objects.create(
            name="Hilton",
            country="Turkey",
            city="Istanbul",
            address="Main Street 1",
            description="Luxury hotel"
        )

        self.room = Room.objects.create(name='Deluxe',
                                        hotel=self.hotel,
                                        number=101,
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
        self.hotel = Hotel.objects.create(
            name="Test Hotel",
            country="Egypt",
            city="Cairo",
            address="Main Street 1",
            description="A nice hotel for testing"
        )
        self.room = Room.objects.create(name='Deluxe',
                                        hotel=self.hotel,
                                        number=101,
                                        price_per_night=150.00)

    # Check: Booking form fails without required fields
    def test_booking_form_fails_when_required_fields_missing(self):
        form_data = BookingForm(data={
            'name': '',
            'phone': '',
            'check_in': '',
            'check_out': '',
            'room': '',
        })

        self.assertFalse(form_data.is_valid())

        self.assertIn('name', form_data.errors)
        self.assertIn('phone', form_data.errors)
        self.assertIn('check_in', form_data.errors)
        self.assertIn('check_out', form_data.errors)
        self.assertIn('room', form_data.errors)


class BookingFormTest3(TestCase):
    def setUp(self):
        self.hotel = Hotel.objects.create(
            name="Test Hotel",
            country="Egypt",
            city="Cairo",
            address="Main Street 1",
            description="A nice hotel for testing"
        )

        self.room = Room.objects.create(name='Deluxe',
                                        hotel=self.hotel,
                                        number=101,
                                        price_per_night=150.00)

    # Booking form fails if end_date is earlier than start_date
    def test_booking_form_invalid_if_end_date_before_start_date(self):
        form_data = BookingForm(data={
            'name': 'Alex',
            'phone': '+380974637685',
            'check_in': datetime.date(2025, 9, 11),
            'check_out': datetime.date(2025, 9, 9),
            'room': str(self.room.id),
            'guests': 1
        })

        self.assertFalse(form_data.is_valid())

        self.assertIn('__all__', form_data.errors)


class BookingFormTest4(TestCase):
    def setUp(self):
        self.hotel = Hotel.objects.create(
            name="Test Hotel",
            country="Egypt",
            city="Cairo",
            address="Main Street 1",
            description="A nice hotel for testing"
        )

        self.room = Room.objects.create(name='Deluxe',
                                        hotel=self.hotel,
                                        number=101,
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