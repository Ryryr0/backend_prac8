from django.urls import path, re_path, register_converter
from . import views


app_name = 'main'


urlpatterns = [
    path('', views.welcome_page, name='home'),
    path('statistics', views.Statistics.as_view(), name='statistics'),
]