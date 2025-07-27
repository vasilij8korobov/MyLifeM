from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model

from diary.models import DiaryEntry, FileAttachment, DiaryFileAttachment
from diary.forms import DiaryEntryForm
from diary.views import DiaryUpdateView

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

    def test_diary_file_attachment_relationship(self):
        link = DiaryFileAttachment.objects.create(
            diary_entry=self.entry,
            file_attachment=self.attachment
        )
        self.assertEqual(link.diary_entry, self.entry)
        self.assertEqual(link.file_attachment, self.attachment)


class MixinTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='test@example.com', password='testpass123')
        self.other_user = User.objects.create_user(username='other@example.com', password='testpass123')
        self.entry = DiaryEntry.objects.create(
            user=self.user,
            title='Test Entry',
            text='Test content'
        )

    def test_owner_required(self):
        request = self.factory.get('/fake-url')
        request.user = self.user

        view = DiaryUpdateView()
        view.request = request
        view.kwargs = {'pk': self.entry.pk}

        self.assertTrue(view.test_func())

        request.user = self.other_user
        self.assertFalse(view.test_func())


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


class PaginationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test@example.com', password='testpass123')
        for i in range(15):
            DiaryEntry.objects.create(
                user=self.user,
                title=f'Entry {i}',
                text=f'Content {i}'
            )

    def test_pagination(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('diary_list'))
        self.assertEqual(len(response.context['page_obj']), 10)

        response = self.client.get(reverse('diary_list') + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 5)
