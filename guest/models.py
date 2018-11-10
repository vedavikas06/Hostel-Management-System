from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator

# Create your models here.


class Room(models.Model):
    # room_id = models.AutoField(primary_key=True)
    room_choice = [('S', 'Single Occupancy'), ('D', 'Double Occupancy')]
    no = models.CharField(validators=[MinLengthValidator(2)],max_length=5,unique=True)
    max_persons = models.IntegerField(default=10)
    room_type = models.CharField(choices=room_choice, max_length=1, default=None)
    price = models.IntegerField(default=500)

    def __str__(self):
        return str(self.no)


class Reservation(models.Model):
    room = models.ForeignKey('Room', default=None,null=True, on_delete=models.CASCADE)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    checkIn = models.DateField()
    checkOut = models.DateField()
    booking_id = models.AutoField(primary_key=True)
    guest = models.ForeignKey('Guest', default=None, null=True, on_delete=models.CASCADE)
    room_alloted = models.BooleanField(default=False)
    class Meta:
        verbose_name_plural = 'Reservation'

    def __str__(self):
        return str(self.booking_id)


class Guest(models.Model):
    guest_id = models.AutoField(primary_key=True)
    first_name = models.CharField(validators=[MinLengthValidator(3)],max_length=255)
    last_name = models.CharField(validators=[MinLengthValidator(3)],max_length=255)
    phone = models.CharField(
        validators=[MinLengthValidator(5)],
        max_length=12,
        blank=True,
    )
    email = models.EmailField(
        verbose_name= ('e-mail'),
        blank=True,
    )
    city = models.CharField(
        max_length=20,
        blank=True,
    )
    # room = models.OneToOneField(
    #     'Room',
    #     blank=True,
    #     on_delete=models.CASCADE,
    #     null=True)
    # room_allotted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.guest_id)


