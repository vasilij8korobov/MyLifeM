from django.conf import settings
from django.db import models


class DiaryEntry(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Используем кастомную модель
        on_delete=models.CASCADE,
        related_name='diary_entries',
        verbose_name = 'Ваш никнейм'
    )
    title = models.CharField(max_length=100)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Запись дневника'
        verbose_name_plural = 'Записи дневника'

    def __str__(self):
        return f'{self.title} (автор: {self.user.username})'
