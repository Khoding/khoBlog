from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    captcha = CaptchaField()

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name',)

        widgets = {
            'username': forms.TextInput(),
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'email': forms.EmailInput(),
        }


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'bio', 'welcome_message', 'profile_pic',
                  'slug', 'default_theme',)

        widgets = {
            'username': forms.TextInput(),
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'bio': forms.Textarea(),
            'email': forms.EmailInput(),
            'slug': forms.TextInput(),
            'welcome_message': forms.TextInput(),
            'default_theme': forms.Select(),
        }
