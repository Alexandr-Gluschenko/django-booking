import re
from types import NoneType

from django.utils import timezone

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.TextField(max_length=255)
    description = models.TextField(blank=True)
    stars = models.IntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} ({self.city})'


class Amenity(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    name = models.CharField(max_length=100)
    number = models.IntegerField(null=True)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    max_guests = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, default="available")
    amenities = models.ManyToManyField(Amenity, related_name='rooms', blank=True)

    def is_available(self, check_in, check_out, exclude_booking_id=None):
        overlapping_bookings = self.bookings.filter(
            Q(check_in__lt=check_out) & Q(check_out__gt=check_in),
            status='accepted'
        )
        if exclude_booking_id:
            overlapping_bookings = overlapping_bookings.exclude(pk=exclude_booking_id)

        return not overlapping_bookings.exists()

    def __str__(self):
        return f'{self.name or "No name"} - Room {self.number or "No number"}'


class Booking(models.Model):
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('accepted', 'Accepted'),
            ('cancelled', 'Cancelled'),
        ],
        default='pending'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings', blank=True, null=True)
    room = models.ForeignKey('Room', on_delete=models.CASCADE, related_name='bookings')

    check_in = models.DateTimeField(default=timezone.now)
    check_out = models.DateTimeField(default=timezone.now)
    phone = models.CharField(max_length=20,
                             validators=[RegexValidator(regex=r'^\+380\d{9}$',
                                                        message="The phone number must be in the format: '+380XXXXXXXXX' (for example, +380981234567)"
                                                        )
                                         ]
                             )
    guests = models.PositiveIntegerField(default=1)

    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        errors = {}
        # Check room availability
        if self.room_id is None or self.check_in is None or self.check_out is None:
            return

        if not self.room.is_available(self.check_in,
                                      self.check_out,
                                      exclude_booking_id=self.pk):
            raise ValidationError("Room is not available for these dates.")


        # Checking the number of guests
        if self.guests > self.room.max_guests:
            errors["guests"] = f"Maximum guests for this room: {self.room.max_guests}."

        # Phone number authentication
        if not re.match(r'^\+380\d{9}$', self.phone):
            errors["phone"] = "Phone number must be entered in the format: '+380985453232'"

        # Check if a room is available for booking based on its status.
        if self.room.status in ["repair", "occupied"]:
            msg = "The room is under renovation." if self.room.status == "repair" else "The room is occupied."
            errors["status"] = msg

        if errors:
            raise ValidationError(errors)

    def accept(self):
        self.status = 'accepted'
        self.save()

    def cancel(self):
        self.status = 'cancelled'
        self.save()

        if self.status == "cancelled":
            raise ValidationError("Booking is already cancelled")


    def save(self, *args, **kwargs):
        nights = (self.check_out - self.check_in).days
        if nights < 1:
            nights = 1

        # base price
        base_price = self.room.price_per_night * nights * self.guests

        #Discount logic
        if nights >= 7:
            base_price *= 0.9
        if self.guests >= 4:
            base_price *= 0.95

        # save the final price
        self.total_price = base_price

        # Validation (e.g. checking room availability)
        self.clean()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.room} ({self.check_in} -> {self.check_out})"
