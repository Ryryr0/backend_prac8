from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.models import UserManager

from .models import UserPreferences


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Login',
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        field = ['username', 'password']


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.CharField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        labels = {
            'first_name': 'First name',
            'last_name': 'Last name',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }


    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Entered e-mail is already exist!')
        return email


class UserPreferencesForm(forms.ModelForm):
    class Meta:
        model = UserPreferences
        fields = ['language', 'them']
        labels = {
            'language': 'Language',
            'them': 'Them',
        }
        widgets = {
            'language': forms.Select(attrs={'class': 'form-input'}),
            'them': forms.Select(attrs={'class': 'form-input'}),
        }
