import re
from decimal import Decimal

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

    @property
    def min_price(self):
        room = self.rooms.order_by("price_per_night").first()
        return room.price_per_night if room else None

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


class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='hotel_images/')

    def __str__(self):
        return f"{self.hotel.name} - Image {self.id}"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('cancelled', 'Cancelled'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings', blank=True, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')

    check_in = models.DateTimeField(default=timezone.now)
    check_out = models.DateTimeField(default=timezone.now)

    phone = models.CharField(
        max_length=20,
        validators=[RegexValidator(
            regex=r'^\+380\d{9}$',
            message="The phone number must be in format +380XXXXXXXXX"
        )]
    )

    guests = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        errors = {}

        # 1. Checking required fields using *_id
        if not self.room_id:
            errors["room"] = "Room is required."
            raise ValidationError(errors)

        if not self.check_in:
            errors["check_in"] = "Check-in date is required."

        if not self.check_out:
            errors["check_out"] = "Check-out date is required."

        if not self.guests:
            errors["guests"] = "Number of guests is required."

        if errors:
            raise ValidationError(errors)

        # 2. Checking date availability
        room = self.room

        if self.check_in >= self.check_out:
            raise ValidationError("Check-out must be after check-in.")

        if not room.is_available(self.check_in, self.check_out, exclude_booking_id=self.pk):
            raise ValidationError("Room is not available for these dates.")

        # 3. Checking guests
        if self.guests > room.max_guests:
            errors["guests"] = f"Maximum guests for this room: {room.max_guests}."

        if errors:
            raise ValidationError(errors)

    def accept(self):
        self.status = "accepted"
        self.save()

    def cancel(self):
        if self.status == "cancelled":
            raise ValidationError("Booking is already cancelled")

        self.status = "cancelled"
        self.save()

    def save(self, *args, **kwargs):
        nights = (self.check_out - self.check_in).days
        nights = max(nights, 1)

        base_price = self.room.price_per_night * nights * self.guests

        if nights >= 7:
            base_price *= Decimal("0.90")
        if self.guests >= 4:
            base_price *= Decimal("0.95")

        self.total_price = base_price

        self.clean()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.room} ({self.check_in} -> {self.check_out})"
