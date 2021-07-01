from django import forms
from .models import UserProfile
from django.forms import ClearableFileInput

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_pic']
