import os

from django.conf import settings
from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from django.utils.text import slugify

from posts import views
from .forms import PostCreationForm
from .models import Post, PostFiles


class TestUrls(SimpleTestCase):
    def test_post_creation_url_resolves(self):
        url = reverse('posts:post_creation')
        self.assertEqual(resolve(url).func.view_class, views.PostCreator)

    def test_post_url_resolves(self):
        url = reverse('posts:post', kwargs={'post_slug': 'test'})
        self.assertEqual(resolve(url).func.view_class, views.ShowPost)

    def test_edit_post_url_resolves(self):
        url = reverse('posts:edit_post', kwargs={'post_slug': 'test'})
        self.assertEqual(resolve(url).func.view_class, views.EditPost)

    def test_delete_post_url_resolves(self):
        url = reverse('posts:delete_post', kwargs={'slug': 'test'})
        self.assertEqual(resolve(url).func.view_class, views.DeletePost)


class PostViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='password123')

        cls.post = Post.objects.create(
            title='Test Post',
            content='This is a test post',
            slug='test-post',
            author=cls.user,
            is_published=True
        )

    def setUp(self):
        self.client.login(username='testuser', password='password123')

    def test_post_creation_view(self):
        url = reverse('posts:post_creation')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_creation.html')

        self.assertIsInstance(response.context['form'], PostCreationForm)

        post_data = {
            'title': 'New Test Post',
            'content': 'Content of the new post',
            'is_published': Post.STATUS.PUBLISHED,
        }
        response = self.client.post(url, post_data)
        self.assertRedirects(response, reverse('user_profiles:profile'))
        self.assertTrue(Post.objects.filter(title='New Test Post').exists())

    def test_show_post_view(self):
        url = reverse('posts:post', kwargs={'post_slug': self.post.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post.html')
        self.assertEqual(response.context['post'], self.post)
        self.assertEqual(response.context['user_name'], self.user.get_username())

    def test_edit_post_view(self):
        url = reverse('posts:edit_post', kwargs={'post_slug': self.post.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/edit_post.html')
        self.assertEqual(response.context['post'], self.post)

        updated_data = {
            'title': 'Updated Post Title',
            'content': 'Updated content',
            'is_published': Post.STATUS.PUBLISHED,
        }
        response = self.client.post(url, updated_data)
        self.assertRedirects(response, reverse('user_profiles:profile'))
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Post Title')

    def test_delete_post_view(self):
        url = reverse('posts:delete_post', kwargs={'slug': self.post.slug})
        response = self.client.post(url)
        self.assertRedirects(response, reverse('user_profiles:profile'))
        self.assertFalse(Post.objects.filter(slug=self.post.slug).exists())


class PostCreationFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='password123')

    def test_form_valid_data(self):
        data = {
            'title': 'Test Post',
            'content': 'This is a test post content.',
            'is_published': Post.STATUS.PUBLISHED,
        }
        form = PostCreationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_without_title(self):
        data = {
            'content': 'Content without title',
            'is_published': Post.STATUS.PUBLISHED,
        }
        form = PostCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_form_invalid_with_long_title(self):
        data = {
            'title': 'a' * 256,
            'content': 'Valid content',
            'is_published': Post.STATUS.PUBLISHED,
        }
        form = PostCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_form_invalid_with_invalid_status(self):
        data = {
            'title': 'Test Post',
            'content': 'Content with invalid status',
            'is_published': 'invalid',
        }
        form = PostCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('is_published', form.errors)

    def test_form_file_upload(self):
        data = {
            'title': 'Post with file',
            'content': 'This post contains a file',
            'is_published': Post.STATUS.PUBLISHED,
        }
        file = self.generate_test_file()

        data['file'] = file
        form = PostCreationForm(data=data, files={'file': file})

        self.assertTrue(form.is_valid())

    def test_form_file_not_required(self):
        data = {
            'title': 'Post without file',
            'content': 'This post does not contain a file',
            'is_published': Post.STATUS.PUBLISHED,
        }
        form = PostCreationForm(data=data)
        self.assertTrue(form.is_valid())

    def generate_test_file(self):
        from io import BytesIO
        from django.core.files.uploadedfile import InMemoryUploadedFile

        file = BytesIO(b'This is a test file.')
        file.name = 'testfile.txt'
        file.seek(0)
        uploaded_file = InMemoryUploadedFile(file, None, 'testfile.txt', 'text/plain', len(file.getvalue()), None)
        return uploaded_file


class PostModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='password123')
        cls.post = Post.objects.create(
            title='Test Post Title',
            content='This is a test post content.',
            author=cls.user,
            is_published=Post.STATUS.PUBLISHED
        )

    def test_post_creation(self):
        post = self.post
        self.assertEqual(post.title, 'Test Post Title')
        self.assertEqual(post.content, 'This is a test post content.')
        self.assertEqual(post.author.username, 'testuser')
        self.assertTrue(post.is_published)
        self.assertIsNotNone(post.slug)  # Проверяем, что slug был сгенерирован

    def test_get_absolute_url(self):
        post = self.post
        expected_url = reverse('posts:post', kwargs={'post_slug': post.slug})
        self.assertEqual(post.get_absolute_url(), expected_url)

    def test_get_edit_url(self):
        post = self.post
        expected_url = reverse('posts:edit_post', kwargs={'post_slug': post.slug})
        self.assertEqual(post.get_edit_url(), expected_url)

    def test_get_delete_url(self):
        post = self.post
        expected_url = reverse('posts:delete_post', kwargs={'slug': post.slug})
        self.assertEqual(post.get_delete_url(), expected_url)

    def test_get_author_url(self):
        post = self.post
        expected_url = reverse('user_profiles:author_profile', kwargs={'author_post_user': post.author.pk})
        self.assertEqual(post.get_author_url(), expected_url)

    def test_slug_generation(self):
        post = self.post
        expected_slug = slugify(post.title)
        self.assertEqual(post.slug, expected_slug)

    def test_published_manager(self):
        Post.objects.create(title='Unpublished Post', content='Content', author=self.user,
                            is_published=Post.STATUS.PRIVATE)
        post = self.post
        published_posts = Post.published.all()
        self.assertEqual(published_posts.count(), 1)
        self.assertEqual(published_posts.first(), post)


class PostFilesModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='password123')
        cls.post = Post.objects.create(
            title='Test Post Title',
            content='This is a test post content.',
            author=cls.user,
            is_published=Post.STATUS.PUBLISHED
        )

    def test_create_post_file(self):
        file = PostFiles.objects.create(post=self.post, file='upload_posts_files/test_file.txt')

        self.assertEqual(file.post, self.post)
        self.assertEqual(file.file.name, 'upload_posts_files/test_file.txt')
