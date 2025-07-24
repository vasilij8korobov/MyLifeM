from django import forms
from .models import GradeRecord, DiaryEntry, Tag


class DiaryEntryForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    attachments = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        required=False
    )

    class Meta:
        model = DiaryEntry
        fields = ['title', 'text', 'is_private']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 5}),
        }


# ниже лишнее
class GradeForm(forms.ModelForm):
    class Meta:
        model = GradeRecord
        fields = ['subject', 'grade', 'date', 'homework']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
