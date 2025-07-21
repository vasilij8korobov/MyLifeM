from django.contrib.auth.models import AbstractUser
from django.db import models

from config.DRY import NULLABLE


class CustomUser(AbstractUser):
    username = models.EmailField(
        unique=True,
        verbose_name='Ваш никнейм'
    )

    phone = models.CharField(max_length=15, blank=True)

    avatar = models.ImageField(
        upload_to='images/avatars/',
        **NULLABLE,
        verbose_name='Аватарка'
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'