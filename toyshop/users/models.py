from django.db import models
from django.contrib.auth.models import User


class UserPreferences(models.Model):
    class THEMES(models.TextChoices):
        LIGHT = 'light'
        DARK = 'dark'

    class LANGUAGE(models.TextChoices):
        RU = 'Russian'
        ENG = 'English'

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    language = models.CharField(max_length=10, choices=LANGUAGE.choices, default=LANGUAGE.RU)
    them = models.CharField(max_length=10, choices=THEMES.choices, default=THEMES.LIGHT)
