from django.contrib.auth.forms import UserCreationForm
from django import forms
import datetime
from .models import *

YEARS= [x for x in range(2018,2021)]


class DateForm(forms.ModelForm):
    checkIn = forms.DateField(initial=datetime.date.today,widget=forms.SelectDateWidget(years=YEARS))
    checkOut = forms.DateField(initial=datetime.date.today,widget=forms.SelectDateWidget(years=YEARS))

    class Meta:
        model = Reservation
        fields = ['checkIn', 'checkOut', ]


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = [
            'first_name',
            'last_name',
            'phone',
            'email',
            'city', ]


class SelectionForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['room', ]
