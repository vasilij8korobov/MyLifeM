from django import forms
from django.core.validators import FileExtensionValidator

from .models import DiaryEntry, FileAttachment


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
    attachments = MultipleFileField(
        required=False,
        validators=[FileExtensionValidator(
            allowed_extensions=['pdf', 'jpg', 'png', 'docx'],
            message='Недопустимое расширение файла'
        )],
    )

    class Meta:
        model = DiaryEntry
        fields = ['title', 'text', 'is_private']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 5}),
        }

    def save(self, commit=True):
        instance = super().save(commit=commit)
        if commit and 'attachments' in self.files:
            for uploaded_file in self.files.getlist('attachments'):
                attachment = FileAttachment.objects.create(
                    file=uploaded_file,
                    uploaded_by=self.instance.user,
                    diary_entry=instance
                )
                instance.attachments.add(attachment)
        return instance
