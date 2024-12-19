from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, ListView

from .forms import ProfileSettingsForm
from posts.models import Post
from users.models import UserPreferences


class ProfilePage(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'user_profiles/profile.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_name'] = self.request.user.get_username()

        context['title'] = self.request.user.get_username()
        context['them'] = UserPreferences.objects.get(user=self.request.user).them
        context['language'] = UserPreferences.objects.get(user=self.request.user).language
        context['is_owner'] = True

        return context

    def get_queryset(self):
        try:
            return Post.published.filter(author=self.kwargs['author_post_user'])
        except KeyError:
            return Post.objects.filter(author=self.request.user)
