from django.urls import path
from . import views


app_name = 'user_profiles'


urlpatterns = [
    path('', views.ProfilePage.as_view(), name='profile'),
    path('author-profile/<int:author_post_user>', views.ProfilePage.as_view(), name='author_profile'),
]
