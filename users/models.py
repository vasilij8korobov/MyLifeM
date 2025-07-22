from django.contrib.auth.models import AbstractUser
from django.db import models

from config.DRY import NULLABLE


class CustomUser(AbstractUser):
    username = models.EmailField(
        unique=True,
        verbose_name='Ваш никнейм'
    )

    phone = models.CharField(max_length=15, unique=True)

    avatar = models.ImageField(
        upload_to='images/avatars/',
        **NULLABLE,
        verbose_name='Аватарка'
    )

    birth_date = models.DateField(**NULLABLE, verbose_name='Дата рождения')

    wants_school_diary = models.BooleanField(default=False)

    @property
    def is_minor(self):
        from datetime import date
        return (date.today() - self.birth_date).days < 18 * 365

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'