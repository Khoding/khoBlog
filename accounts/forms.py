from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from captcha.fields import CaptchaField


class CustomUserCreationForm(UserCreationForm):
    captcha = CaptchaField()

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name',)

        widgets = {
            'username': forms.TextInput(attrs={'class': 'bg-dark text-light'}),
            'first_name': forms.TextInput(attrs={'class': 'bg-dark text-light'}),
            'last_name': forms.TextInput(attrs={'class': 'bg-dark text-light'}),
            'email': forms.EmailInput(attrs={'class': 'bg-dark text-light'}),
        }


class CustomUserChangeForm(UserChangeForm):
    captcha = CaptchaField()

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'bio', 'welcome_message', 'profile_pic',
                  'slug',)

        widgets = {
            'username': forms.TextInput(attrs={'class': 'bg-dark text-light'}),
            'first_name': forms.TextInput(attrs={'class': 'bg-dark text-light'}),
            'last_name': forms.TextInput(attrs={'class': 'bg-dark text-light'}),
            'bio': forms.Textarea(attrs={'class': 'bg-dark text-light'}),
            'email': forms.EmailInput(attrs={'class': 'bg-dark text-light'}),
            'slug': forms.TextInput(attrs={'class': 'bg-dark text-light'}),
            'welcome_message': forms.TextInput(attrs={'class': 'bg-dark text-light'}),
        }
