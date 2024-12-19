from django.contrib.auth.models import User
from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from user_profiles import views
from django.contrib.auth import get_user_model

from posts.models import Post


class TestUrls(SimpleTestCase):

    def test_profile_url(self):
        url = reverse('user_profiles:profile')
        self.assertEqual(resolve(url).func.view_class, views.ProfilePage)

    def test_author_profile_url(self):
        url = reverse('user_profiles:author_profile', kwargs={'author_post_user': 1})
        self.assertEqual(resolve(url).func.view_class, views.ProfilePage)

    def test_profile_settings_url(self):
        url = reverse('user_profiles:profile_settings')
        self.assertEqual(resolve(url).func.view_class, views.ProfileSettings)


class TestProfileViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='password123')
        cls.other_user = get_user_model().objects.create_user(username='otheruser', password='password123')
        cls.post = Post.objects.create(title='Test Post', content='This is a test post', author=cls.user)

    def setUp(self):
        self.client.login(username='testuser', password='password123')

    def test_profile_page_for_owner(self):
        url = reverse('user_profiles:profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')
        self.assertContains(response, 'This is a test post')
        self.assertNotContains(response, 'otheruser')

    def test_profile_page_for_other_user(self):
        url = reverse('user_profiles:author_profile', kwargs={'author_post_user': self.other_user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'otheruser')

    def test_profile_settings_page(self):
        url = reverse('user_profiles:profile_settings')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Profile settings')

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        url = reverse('user_profiles:profile')
        response = self.client.get(url)
        self.assertRedirects(response, f'/users/login/?next={url}')

        url = reverse('user_profiles:profile_settings')
        response = self.client.get(url)
        self.assertRedirects(response, f'/users/login/?next={url}')
