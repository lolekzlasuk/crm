from django import forms
from .models import News, NewsFile, DocumentF, DocFile, DocQuestion, UserQuestion
from django.forms import ClearableFileInput


class NewsForm(forms.ModelForm):
    class Meta():
        model = News
        fields = ['body', 'title', 'staticdoc',
                  'target_location', 'target_departament']

        widgets = {
            'body': forms.Textarea(attrs={'rows': 3,
                                          'cols': 30,
                                          'class': 'editable',
                                          "placeholder": "Title"}),


        }


class NewsFileForm(forms.ModelForm):
    class Meta:
        model = NewsFile
        fields = ['file']
        widgets = {
            'file': ClearableFileInput(attrs={'multiple': True}),
        }


class DocumentFForm(forms.ModelForm):
    class Meta:
        model = DocumentF
        fields = ['title', 'body', 'target_location',
                  'target_departament', 'category']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3,
                                          'cols': 30,
                                          'class': 'editable',
                                          "placeholder": "Title"}),
        }


class DocFileForm(forms.ModelForm):
    class Meta:
        model = DocFile
        fields = ['title', 'file', 'target_location',
                  'target_departament', 'category']
        widgets = {
            'file': ClearableFileInput(),
        }


class DocQuestionForm(forms.ModelForm):
    class Meta:
        model = DocQuestion
        fields = ['title', 'body', 'answer', 'target_location',
                  'target_departament', 'category']


class UserQuestionForm(forms.ModelForm):
    class Meta:
        model = UserQuestion
        fields = ['title', 'body']
