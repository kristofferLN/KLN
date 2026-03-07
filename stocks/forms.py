# i want to make a modelform based of the model "debat".

from django import forms
from .models import debat

class DebatForm(forms.ModelForm):
    class Meta:
        model = debat
        fields = ['bruger', 'tekst', 'selskab']
        widgets = {
            'bruger': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Gæst',
            }),
            'tekst': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 1, 'columns': 60,
                'placeholder': 'Skriv din kommentar her…',
            }),
            'selskab': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'size':1,
                
            }),
        }
        help_texts = {
            'selskab': 'Vælg det eller de selskaber, din kommentar handler om.'
        }
