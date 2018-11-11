from django.contrib.auth.forms import UserCreationForm
from .models import Student, User, Course
from django import forms
from django.core.exceptions import ValidationError


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


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'student_name',
            'father_name',
            'enrollment_no',
            'course',
            'dob',
            'gender']


class SelectionForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['room']


class DuesForm(forms.Form):
    choice = forms.ModelChoiceField(queryset=Student.objects.all().filter(no_dues=True))


class NoDuesForm(forms.Form):
    choice = forms.ModelChoiceField(queryset=Student.objects.all().filter(no_dues=False))
