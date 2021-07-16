from django import forms
from .models import UserProfile
from django.forms import ClearableFileInput
from django.contrib.auth.models import User
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_pic']

class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name',
                'telephone',
                'position',
                'departament',
                'location',]

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email']
