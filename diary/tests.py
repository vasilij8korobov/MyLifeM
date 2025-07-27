from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse

from diary.forms import DiaryEntryForm
from diary.models import DiaryEntry, FileAttachment

User = get_user_model()


class DiaryModelsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test@example.com', password='testpass123')
        self.entry = DiaryEntry.objects.create(
            user=self.user,
            title='Test Entry',
            text='Test content',
            is_private=True
        )
        self.file = SimpleUploadedFile('test.pdf', b'file_content', content_type='application/pdf')
        self.attachment = FileAttachment.objects.create(
            file=self.file,
            uploaded_by=self.user,
            entry=self.entry
        )

    def test_diary_entry_creation(self):
        self.assertEqual(self.entry.title, 'Test Entry')
        self.assertEqual(str(self.entry), f'Test Entry (автор: {self.user.username})')
        self.assertTrue(self.entry.is_private)

    def test_file_attachment_creation(self):
        self.assertTrue(self.attachment.file.name.startswith('diary_attachments/'))
        self.assertTrue(self.attachment.file.name.endswith('.pdf'))
        self.assertEqual(self.attachment.uploaded_by, self.user)
        self.assertEqual(str(self.attachment), f"Файл {self.attachment.file.name} к записи {self.entry.id}")


class DiaryViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test@example.com', password='testpass123')
        self.entry = DiaryEntry.objects.create(
            user=self.user,
            title='Test Entry',
            text='Test content',
            is_private=True
        )

    def test_home_view_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Entry')

    def test_diary_create_view(self):
        self.client.force_login(self.user)
        file = SimpleUploadedFile('test.pdf', b'file_content', content_type='application/pdf')
        response = self.client.post(reverse('diary_create'), {
            'title': 'New Entry',
            'text': 'New content',
            'is_private': False,
            'attachments': [file]
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(DiaryEntry.objects.filter(title='New Entry').exists())

    def test_diary_update_view(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('diary_update', kwargs={'pk': self.entry.pk}), {
            'title': 'Updated',
            'text': 'Updated content',
            'is_private': False
        })
        self.assertEqual(response.status_code, 302)
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.title, 'Updated')


class DiaryFormsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test@example.com', password='testpass123')

    def test_diary_entry_form_valid(self):
        file = SimpleUploadedFile('test.pdf', b'file_content', content_type='application/pdf')
        form = DiaryEntryForm(data={
            'title': 'Test',
            'text': 'Content',
            'is_private': True
        }, files={'attachments': [file]})
        self.assertTrue(form.is_valid())

    def test_diary_entry_form_invalid_extension(self):
        file = SimpleUploadedFile('test.exe', b'file_content', content_type='application/exe')
        form = DiaryEntryForm(data={
            'title': 'Test',
            'text': 'Content',
            'is_private': True
        }, files={'attachments': [file]})
        self.assertFalse(form.is_valid())
        self.assertIn('Недопустимое расширение файла', str(form.errors))
