from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls', namespace='main')),
    path('users/', include('users.urls', namespace='users')),
    path('profiles/', include('user_profiles.urls', namespace='user_profiles')),
    path('posts/', include('posts.urls', namespace='posts')),
]
