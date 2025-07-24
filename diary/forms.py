from django import forms
from .models import GradeRecord, DiaryEntry


class DiaryEntryForm(forms.ModelForm):
    class Meta:
        model = DiaryEntry
        fields = ['title', 'text', 'is_private']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 5}),
        }


class GradeForm(forms.ModelForm):
    class Meta:
        model = GradeRecord
        fields = ['subject', 'grade', 'date', 'homework']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }