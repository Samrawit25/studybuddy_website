from django import forms
from django.contrib.auth.models import User
from .models import Profile, Post
from datetime import datetime

# class RegistrationForm(forms.Form):
#     computing_id = forms.CharField(max_length=20, null=True, unique=True)
#     date_of_birth = forms.DateField(null=True)
#     department = forms.CharField(max_length=255, null=True)
#     current_year = forms.CharField(max_length=20, null=True)
#
#     class Meta:
#         model = User
#         fields = ['date_of_birth', 'computing_id', 'department', 'current_year']


class ProfileUpdateForm(forms.ModelForm):
    CURRENT_YEAR_CHOICES = ((1, '1'), (2, '2'),
            (3, '3'), (4, '4'),
            (4, 'Graduate'),)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'max': datetime.now().date()}))
    current_year = forms.ChoiceField(choices=CURRENT_YEAR_CHOICES)

    class Meta:
        model = Profile
        fields = ['date_of_birth', 'computing_id',
                  'department', 'current_year', 'profile_picture']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['studyCourse', 'studyPreference', 'description']
