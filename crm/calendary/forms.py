from django import forms
from .models import Devent

class DeventForm(forms.ModelForm):


    class Meta():
        model = Devent
        fields = ['title','description','start','end']


        widgets = {

                'start':forms.DateInput(attrs={'type': 'time'}),
                'end':forms.DateInput(attrs={'type': 'time'}),

                }
