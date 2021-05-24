from django import forms
from .models import Devent

class DeventForm(forms.ModelForm):
    start = forms.TimeField()
    end = forms.TimeField()
    class Meta():
        model = Devent
        fields = ['title','description','start','end']
