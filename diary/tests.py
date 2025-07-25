from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from diary.models import Tag, DiaryEntry
from users.models import CustomUser


class DiaryTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username='testuser')
        self.tag = Tag.objects.create(name='Работа')
        self.client.force_login(self.user)

    def test_create_entry_with_tags(self):
        response = self.client.post('/entries/add/', {
            'title': 'Тест',
            'content': 'Тест контент',
            'tags': [self.tag.id]
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(DiaryEntry.objects.first().tags.count(), 1)

    def test_file_upload(self):
        test_file = SimpleUploadedFile('test.txt', b'file_content')
        response = self.client.post('/entries/add/', {
            'title': 'Файл',
            'content': 'Тест',
            'attachments': test_file
        })
        self.assertEqual(DiaryEntry.objects.first().files.count(), 1)
