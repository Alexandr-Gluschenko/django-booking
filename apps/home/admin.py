from django.contrib import admin
from .models import Hotel, Room, Booking

admin.site.register(Hotel)
admin.site.register(Room)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("user", "room", "check_in", "check_out", "status", "created_at")
    list_filter = ("status", "created_at")
    actions = ["accepted", "cancelled"]

    def accepted(self, request, queryset):
        queryset.update(status="accepted")
        self.message_user(request, "Selected bookings have been accepted.")

    accepted.short_description = "Accept selected bookings"

    def cancelled(self, request, queryset):
        queryset.update(status="cancelled")
        self.message_user(request, "Selected bookings have been cancelled.")

    cancelled.short_description = "Cancel selected bookings"
