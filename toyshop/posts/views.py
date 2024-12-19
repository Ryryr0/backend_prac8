from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from .forms import PostCreationForm
from .models import Post, PostFiles


class PostCreator(CreateView, LoginRequiredMixin):
    model = Post
    form_class = PostCreationForm
    template_name = 'posts/post_creation.html'
    success_url = reverse_lazy('user_profiles:profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = self.get_data()
        context['title'] = 'Post Creation'
        context['user_name'] = self.request.user.get_username()
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()

        uploaded_file = self.request.FILES.get('file')
        if uploaded_file:
            PostFiles.objects.create(post=post, file=uploaded_file)

        return super().form_valid(form)

    def get_data(self):
        data = {
            'title': 'Post Creation',
            'user_name': self.request.user.get_username()
        }
        return data


class ShowPost(LoginRequiredMixin, DetailView):
    template_name = 'posts/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post'].title
        context['user_name'] = self.request.user.get_username()
        context['files'] = context['post'].get_files()
        context['is_owner'] = self.request.user == context['post'].author
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Post, slug=self.kwargs[self.slug_url_kwarg])


class EditPost(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostCreationForm
    template_name = 'posts/edit_post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'
    success_url = reverse_lazy('user_profiles:profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post'].title
        context['user_name'] = self.request.user.get_username()
        if self.request.user != context['post'].author:
            context['post'] = Post()
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Post, slug=self.kwargs[self.slug_url_kwarg])


class DeletePost(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('user_profiles:profile')
