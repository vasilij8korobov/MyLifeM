from datetime import date
import re
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.core.exceptions import ValidationError


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone')


class SignUpForm(UserCreationForm):
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Дата рождения',
        required=True,
        help_text="Формат: ДД.ММ.ГГГГ"
    )

    phone = forms.CharField(
        max_length=20,  # Согласуйте с моделью
        label="Телефон",
        widget=forms.TextInput(attrs={'placeholder': '+79991234567'})
    )

    wants_school_diary = forms.BooleanField(
        required=False,
        label='Хотите завести дополнительный "Дневник с оценками"?',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'phone', 'birth_date', 'password1', 'password2', 'wants_school_diary')

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        print("Birth date received:", birth_date)  # Отладочная печать

        if not birth_date:
            raise forms.ValidationError("Дата рождения обязательна")

        if birth_date and birth_date > date.today():
            raise forms.ValidationError("Дата рождения не может быть в будущем")
        return birth_date

    def clean(self):
        cleaned_data = super().clean()
        print("Cleaned data:", cleaned_data)
        return cleaned_data

    def clean_phone(self):
        phone = self.cleaned_data['phone']

        if not phone:
            return phone

        if not re.match(r'^\+?[0-9]{10,15}$', phone):
            raise ValidationError("Введите корректный номер телефона")
        return phone
