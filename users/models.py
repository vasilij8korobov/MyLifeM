from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from datetime import date
from config.DRY import NULLABLE


class CustomUser(AbstractUser):
    username = models.EmailField(
        unique=True,
        verbose_name='Ваш email'
    )

    phone = models.CharField(max_length=20, verbose_name='Номер телефона')

    avatar = models.ImageField(
        upload_to='images/avatars/',
        **NULLABLE,
        verbose_name='Аватарка'
    )

    birth_date = models.DateField(**NULLABLE, verbose_name='Дата рождения')



    def clean(self):
        super().clean()
        if self.birth_date and self.birth_date > date.today():
            raise ValidationError({'birth_date': 'Дата рождения не может быть в будущем'})

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'