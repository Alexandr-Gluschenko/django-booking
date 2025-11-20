from django.contrib import admin
from .models import Hotel, Room, Booking, HotelImage


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("user", "room", "check_in", "check_out", "status", "created_at")
    list_filter = ("status", "created_at")
    actions = ["mark_accepted", "mark_cancelled"]

    def mark_accepted(self, request, queryset):
        for booking in queryset:
            booking.accept()
        self.message_user(request, "Selected bookings have been accepted.")
    mark_accepted.short_description = "Accept selected bookings"

    def mark_cancelled(self, request, queryset):
        for booking in queryset:
            try:
                booking.cancel()
            except Exception:
                pass
        self.message_user(request, "Selected bookings have been cancelled.")
    mark_cancelled.short_description = "Cancel selected bookings"


@admin.register(HotelImage)
class HotelImageAdmin(admin.ModelAdmin):
    list_display = ("id", "hotel", "image")


class HotelImageInline(admin.TabularInline):
    model = HotelImage
    extra = 1


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "country", "stars", "created_at")
    search_fields = ("name", "city", "country")
    list_filter = ("country", "city", "stars")
    inlines = [HotelImageInline]


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("name", "number", "hotel", "price_per_night", "status")
    list_filter = ("status", "hotel")
    search_fields = ("name", "number")
