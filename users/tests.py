from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from users.forms import SignUpForm

User = get_user_model()


class UserModelTest(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user(username='test@example.com', password='testpass123')
        self.assertEqual(user.username, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertEqual(str(user), 'test@example.com')


class UserViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test@example.com', password='testpass123')

    def test_register_view(self):
        response = self.client.post(reverse('register'), {
            'username': 'new@example.com',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='new@example.com').exists())

    def test_login_view(self):
        response = self.client.post(reverse('login'), {
            'username': 'test@example.com',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('diary_list'))

    def test_logout_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))


class UserFormsTest(TestCase):
    def test_signup_form_valid(self):
        form = SignUpForm(data={
            'username': 'valid@example.com',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        })
        self.assertTrue(form.is_valid())

    def test_signup_form_password_mismatch(self):
        form = SignUpForm(data={
            'username': 'valid@example.com',
            'password1': 'complexpass123',
            'password2': 'differentpass'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('Введенные пароли не совпадают', str(form.errors))

    def test_signup_form_invalid_email(self):
        form = SignUpForm(data={
            'username': 'invalid-email',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('Введите правильный адрес электронной почты', str(form.errors))
