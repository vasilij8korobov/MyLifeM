from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.utils import timezone

from diary.models import DiaryEntry, Tag, FileAttachment
from diary.forms import DiaryEntryForm

User = get_user_model()


class DiaryModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test@example.com',
            password='testpass123',
            phone='+79001234567'
        )
        self.tag = Tag.objects.create(name='Работа', color='#FF0000')
        self.entry = DiaryEntry.objects.create(
            user=self.user,
            title='Тестовая запись',
            text='Содержание записи',
            is_private=False
        )
        self.entry.tags.add(self.tag)

    def test_entry_creation(self):
        """Тестирование создания записи и связей"""
        self.assertEqual(self.entry.title, 'Тестовая запись')
        self.assertEqual(self.entry.tags.first().name, 'Работа')
        self.assertFalse(self.entry.is_private)
        self.assertLessEqual(self.entry.date, timezone.now())

    def test_file_attachment_creation(self):
        """Тестирование прикрепления файлов"""
        test_file = SimpleUploadedFile('test.txt', b'file content')
        attachment = FileAttachment.objects.create(file=test_file)
        self.entry.attachments.add(attachment)

        self.assertEqual(self.entry.attachments.count(), 1)
        self.assertIn('diary_attachments', attachment.file.name)

    def test_str_methods(self):
        """Тестирование строкового представления"""
        self.assertEqual(str(self.tag), 'Работа')
        self.assertIn(self.user.username, str(self.entry))


class DiaryViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test@example.com',
            password='testpass123'
        )
        self.client.login(username='test@example.com', password='testpass123')
        self.entry = DiaryEntry.objects.create(
            user=self.user,
            title='Тестовая запись',
            text='Контент'
        )

    def test_entry_list_view(self):
        """Тест списка записей"""
        response = self.client.get(reverse('diary_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Тестовая запись')

    def test_invalid_form_submission(self):
        response = self.client.post(
            reverse('diary_create'),
            {
                'title': '',  # Невалидные данные
                'text': 'Контент'
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_private_entry_access(self):
        other_user = User.objects.create_user(username='other@test.com', password='testpass')
        private_entry = DiaryEntry.objects.create(
            user=other_user,
            title='Чужая приватная запись',
            text='Секретно',
            is_private=True
        )

        response = self.client.get(
            reverse('diary_detail', args=[private_entry.pk])
        )
        self.assertEqual(response.status_code, 404)

    # def test_diary_list_view_queryset(self):
    #     # Создаём публичные и приватные записи
    #     public_entry = DiaryEntry.objects.create(
    #         user=self.user,
    #         title='Public',
    #         text='Content',
    #         is_private=False
    #     )
    #     private_entry = DiaryEntry.objects.create(
    #         user=self.user,
    #         title='Private',
    #         text='Secret',
    #         is_private=True
    #     )
    #
    #     response = self.client.get(reverse('diary_list'))
    #     self.assertContains(response, public_entry.title)
    #     self.assertNotContains(response, private_entry.title)

    # def test_entry_create_with_files(self):
    #     """Тест создания записи с файлами"""
    #     test_file = SimpleUploadedFile('test.txt', b'file content', content_type="text/plain")
    #     self.client.force_login(self.user)
    #     response = self.client.post(reverse('diary_create'), {
    #         'title': 'С файлом',
    #         'text': 'Контент',
    #         'is_private': False,
    #         'tags': [],
    #         'attachments': test_file
    #     },
    #     format='multipart')
    #
    #     self.assertEqual(response.status_code, 302)
    #     last_entry = DiaryEntry.objects.last()
    #     self.assertEqual(last_entry.title, 'С файлом')
    #
    #     self.assertEqual(last_entry.attachments.count(), 1)
    #     self.assertTrue(last_entry.attachments.first().file.name.endswith('test.txt'))

    def test_private_entry_access(self):
        """Тест доступа к приватным записям"""
        private_entry = DiaryEntry.objects.create(
            user=self.user,
            title='Приватная',
            text='Секретно',
            is_private=True
        )
        response = self.client.get(reverse('diary_detail', args=[private_entry.pk]))
        self.assertEqual(response.status_code, 200)


class DiaryFormTests(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name='Личное', color='#00FF00')

    def test_form_with_tags(self):
        """Тест формы с тегами"""
        form_data = {
            'title': 'Теговая запись',
            'text': 'Контент',
            'tags': [self.tag.pk]
        }
        form = DiaryEntryForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_file_validation(self):
        """Тест валидации файлов"""
        invalid_file = SimpleUploadedFile('test.exe', b'file content')
        form = DiaryEntryForm(
            data={'title': 'Test', 'text': 'Test'},
            files={'attachments': invalid_file}
        )
        self.assertFalse(form.is_valid())
        self.assertIn('Недопустимое расширение файла', str(form.errors))
