from django.contrib import admin
from .models import Room,Reservation,Guest
# Register your models here.

admin.site.register(Room)
admin.site.register(Reservation)
admin.site.register(Guest)
