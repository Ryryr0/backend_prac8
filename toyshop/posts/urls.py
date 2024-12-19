from django.urls import path
from . import views


app_name = 'posts'


urlpatterns = [
    path('post-creation/', views.PostCreator.as_view(), name='post_creation'),
    path('post/<slug:post_slug>', views.ShowPost.as_view(), name='post'),
    path('edit-post/<slug:post_slug>', views.EditPost.as_view(), name='edit_post'),
    path('delete-post/<slug:slug>', views.DeletePost.as_view(), name='delete_post'),
]
