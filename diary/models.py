from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models

from config.DRY import NULLABLE


class FileAttachment(models.Model):
    file = models.FileField(
        upload_to='diary_attachments/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'png', 'docx'])]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(  # Добавляем пользователя
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True
    )

    diary_entry = models.ForeignKey(  # Явная связь с записью
        'DiaryEntry',
        on_delete=models.CASCADE,
        related_name='file_attachments',
        **NULLABLE,
    )

    def __str__(self):
        return f"Файл {self.file.name} к записи {self.diary_entry_id}"

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=7, default='#007bff')  # HEX цвет

    def __str__(self):
        return self.name


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

    tags = models.ManyToManyField(Tag, blank=True)
    attachments = models.ManyToManyField(
        FileAttachment,
        through='DiaryFileAttachment',
        blank=True,
        related_name='entries'
    )

    class Meta:
        ordering = ['-date', '-updated_at']
        verbose_name = 'Запись дневника'
        verbose_name_plural = 'Записи дневника'

    def __str__(self):
        return f'{self.title} (автор: {self.user.username})'


# ниже лишнее
class SchoolDiary(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now=True)


class GradeRecord(models.Model):
    diary = models.ForeignKey(SchoolDiary, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, verbose_name="Название предмета")
    grade = models.CharField(max_length=3, verbose_name="Оценка")
    date = models.DateField(verbose_name="Дата записи")
    homework = models.TextField(**NULLABLE, verbose_name="Домашнее задание")
    reminder = models.TextField(**NULLABLE, verbose_name="Напоминание")
