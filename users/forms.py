from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class SignUpForm(UserCreationForm):
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Дата рождения'
    )

    wants_school_diary = forms.BooleanField(
        required=False,
        label='Хотите завести дополнительный "Дневник с оценками"?',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'phone', 'birth_date', 'password1', 'password2', 'wants_school_diary')