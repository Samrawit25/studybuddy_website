from django import forms
from django.contrib.auth.models import User
from .models import Profile, Course


class RegistrationForm(forms.Form):
    computing_id = forms.CharField(max_length=20, null=True, unique=True)
    date_of_birth = forms.DateField(null=True)
    department = forms.CharField(max_length=255, null=True)
    current_year = forms.CharField(max_length=20, null=True)

    class Meta:
        model = User
        fileds = ('date_of_birth', 'computing_id', 'department', 'current_year')
