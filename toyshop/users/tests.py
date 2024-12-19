from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User

from .forms import LoginUserForm, RegisterUserForm
from . import views


class UsersURLsTest(SimpleTestCase):

    def test_login_url_resolves(self):
        url = reverse('users:login')
        self.assertEqual(resolve(url).func.view_class, views.LoginUser)

    def test_logout_url_resolves(self):
        url = reverse('users:logout')
        self.assertEqual(resolve(url).func, views.logout_user)

    def test_register_url_resolves(self):
        url = reverse('users:register')
        self.assertEqual(resolve(url).func.view_class, views.RegisterUser)


class ViewsTest(TestCase):

    def setUp(self):
        self.user_credentials = {
            'username': 'testuser',
            'password': 'password123',
        }
        self.user = User.objects.create_user(**self.user_credentials)

    def test_login_view_get(self):
        url = reverse('users:login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertIsInstance(response.context['form'], LoginUserForm)

    def test_login_view_post_success(self):
        url = reverse('users:login')
        response = self.client.post(url, self.user_credentials, follow=True)
        self.assertRedirects(response, reverse('user_profiles:profile'))
        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_view_post_failure(self):
        url = reverse('users:login')
        response = self.client.post(url, {'username': 'wrong', 'password': 'wrong'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertFalse(response.context['user'].is_authenticated)

    def test_register_view_get(self):
        url = reverse('users:register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertIsInstance(response.context['form'], RegisterUserForm)

    def test_register_view_post_success(self):
        url = reverse('users:register')
        new_user_data = {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
        }
        response = self.client.post(url, new_user_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_logout_view(self):
        self.client.login(**self.user_credentials)
        url = reverse('users:logout')
        response = self.client.get(url, follow=True)
        self.assertRedirects(response, '/')
        self.assertFalse(response.context['user'].is_authenticated)
