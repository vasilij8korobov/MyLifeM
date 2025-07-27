from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models

from config.DRY import NULLABLE


class FileAttachment(models.Model):
    file = models.FileField(
        upload_to='diary_attachments/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'png', 'docx'])],
        verbose_name='Загрузить файл'
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(  # Добавляем пользователя
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True
    )

    entry = models.ForeignKey(  # Явная связь с записью
        'DiaryEntry',
        on_delete=models.CASCADE,
        related_name='files',
        **NULLABLE,
    )

    def __str__(self):
        return f"Файл {self.file.name} к записи {self.entry.id}"


class DiaryFileAttachment(models.Model):
    diary_entry = models.ForeignKey('DiaryEntry', on_delete=models.CASCADE)
    file_attachment = models.ForeignKey(FileAttachment, on_delete=models.CASCADE)
    attached_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('diary_entry', 'file_attachment')


class DiaryEntry(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Используем кастомную модель
        on_delete=models.CASCADE,
        related_name='diary_entries',
        verbose_name='Ваш никнейм'
    )
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_private = models.BooleanField(default=True, verbose_name='Приватно')

    attachments = models.ManyToManyField(
        FileAttachment,
        through='DiaryFileAttachment',
        blank=True,
        related_name='entries',
        verbose_name='Загрузить файл'
    )
    file = models.FileField(upload_to='diary_files/', null=True, blank=True)

    class Meta:
        ordering = ['-date', '-updated_at']
        verbose_name = 'Запись дневника'
        verbose_name_plural = 'Записи дневника'

    def __str__(self):
        return f'{self.title} (автор: {self.user.username})'
