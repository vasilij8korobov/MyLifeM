from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model

from users.forms import SignUpForm

User = get_user_model()


class UserModelTests(TestCase):
    def test_user_creation(self):
        """Тест создания пользователя с дополнительными полями"""
        user = User.objects.create_user(
            username='user@example.com',
            email='user@example.com',
            phone='+79001234567',
            birth_date='2000-01-01',
            password='testpass123'
        )
        self.assertEqual(user.phone, '+79001234567')
        self.assertFalse(user.is_staff)

    def test_avatar_upload(self):
        """Тест загрузки аватарки"""
        test_image = SimpleUploadedFile(
            'avatar.jpg',
            b'file_content',
            content_type='image/jpeg'
        )
        user = User.objects.create_user(
            username='avatar@example.com',
            password='testpass123',
            avatar=test_image
        )
        self.assertIn('images/avatars/', user.avatar.name)


class AuthViewTests(TestCase):
    def test_signup_flow(self):
        """Полный тест регистрации"""
        response = self.client.post(reverse('register'), {
            'username': 'new@example.com',
            'phone': '+79007654321',
            'birth_date': '2000-01-01',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
            'wants_school_diary': True
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), 1)

        new_user = User.objects.first()
        self.assertEqual(new_user.phone, '+79007654321')

    def test_login_redirect(self):
        """Тест перенаправления после входа"""
        User.objects.create_user(
            username='login@example.com',
            password='testpass123'
        )
        response = self.client.post(reverse('login'), {
            'username': 'login@example.com',
            'password': 'testpass123'
        }, follow=True)
        self.assertRedirects(response, reverse('diary_list'))


class UserFormTests(TestCase):
    def test_signup_form_validation(self):
        """Тест валидации формы регистрации"""
        # Неправильная дата рождения
        form_data = {
            'username': 'test@example.com',
            'phone': '+79001234567',
            'birth_date': '3000-01-01',  # Дата в будущем
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Дата рождения не может быть в будущем', str(form.errors))

    def test_phone_validation(self):
        """Тест валидации номера телефона"""
        form_data = {
            'username': 'test@example.com',
            'phone': 'не номер',  # Невалидный номер
            'birth_date': '2000-01-01',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
