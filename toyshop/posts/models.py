import string
import random

from django.core.validators import validate_comma_separated_integer_list
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from autoslug import AutoSlugField


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Post.STATUS.PUBLISHED)


class Post(models.Model):
    class STATUS(models.IntegerChoices):
        PRIVATE = 0, 'Private'
        PUBLISHED = 1, 'Published'

    objects = models.Manager()
    published = PublishedManager()

    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='title', always_update=False, unique=True, db_index=True)
    content = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(choices=STATUS.choices, default=STATUS.PUBLISHED)

    class Meta:
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]

    def get_files(self):
        return PostFiles.objects.filter(post=self)

    def get_absolute_url(self):
        return reverse('posts:post', kwargs={'post_slug': self.slug})

    def get_edit_url(self):
        return reverse('posts:edit_post', kwargs={'post_slug': self.slug})

    def get_delete_url(self):
        return reverse('posts:delete_post', kwargs={'slug': self.slug})

    def get_author_url(self):
        return reverse('user_profiles:author_profile', kwargs={'author_post_user': self.author.pk})


class PostFiles(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    file = models.FileField(upload_to='upload_posts_files/%Y/%m/%d/')
