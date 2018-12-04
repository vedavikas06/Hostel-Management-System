from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['no', 'room_type', 'price']


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['booking_id', 'room', 'checkIn', 'checkOut','room_alloted','accept','reject']


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ['guest_id', 'first_name', 'last_name','username']

    def username(self, obj):
        return obj.user.username


