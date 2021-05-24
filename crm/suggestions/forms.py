from django import forms
from .models import Question,Answer


class QuestionForm(forms.ModelForm):
        class Meta():
            model = Question
            fields = ['body','title','category']

class AnswerForm(forms.ModelForm):
    class Meta():
        model = Answer
        fields = ['body']
