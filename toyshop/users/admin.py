from django.contrib import admin

# Register your models here.
from .models import UserPreferences


@admin.register(UserPreferences)
class UserPreferencesAdmin(admin.ModelAdmin):
    list_display = ('user', 'language', 'them')
