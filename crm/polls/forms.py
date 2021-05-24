from django import forms
from .models import Poll

class PollForm(forms.ModelForm):
    class Meta():
        model = Poll
        fields = ['title','target_departament','target_location']
