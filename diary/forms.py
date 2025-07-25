from django import forms
from .models import GradeRecord, DiaryEntry, Tag


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class DiaryEntryForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    attachments = MultipleFileField(required=False)

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
