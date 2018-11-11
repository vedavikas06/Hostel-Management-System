from django.contrib.auth.forms import UserCreationForm
from django import forms
import datetime
from .models import *

YEARS= [x for x in range(2018,2021)]


class UserForm(UserCreationForm):
    password1 = forms.CharField(min_length=8, max_length=30, widget=forms.PasswordInput(render_value=False))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        help_texts = {
            'username': 'same as your roll no.',
        }

    # def clean_password(self):
    #     password = self.cleaned_data.get('password1')
    #     if len(password) < 8:
    #         raise ValidationError('Password too short')
    #     return super(UserCreationForm, self).clean_password1()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


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
