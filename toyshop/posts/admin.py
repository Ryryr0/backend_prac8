from django.contrib import admin

from .models import Post, PostFiles


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'title', 'time_create', 'is_published')
    list_display_links = ('id', 'title')
