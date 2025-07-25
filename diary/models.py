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


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=7, default='#007bff')  # HEX цвет

    def __str__(self):
        return self.name


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
    files = models.ManyToManyField('FileAttachment', blank=True)

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
