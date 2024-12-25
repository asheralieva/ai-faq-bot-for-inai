from django import forms
from .models import QuestionAnswer

class FAQForm(forms.ModelForm):
    class Meta:
        model = QuestionAnswer
        fields = ['question', 'answer']
        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your question'}),
            'answer': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Provide an answer'}),
        }