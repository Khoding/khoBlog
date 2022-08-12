from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from captcha.fields import CaptchaField

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """CustomUserCreationForm Form Class"""

    captcha = CaptchaField()

    class Meta:
        """Meta class for CustomUserCreationForm Form"""

        model = CustomUser
        fields = ("username", "email")


class CustomUserChangeForm(UserChangeForm):
    """CustomUserChangeForm Form Class"""

    class Meta:
        """Meta class for CustomUserChangeForm Form"""

        model = CustomUser
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "bio",
            "welcome_message",
            "profile_pic",
            "slug",
            "display_github",
        )


class ChangeSecureModeStatusForm(forms.ModelForm):
    """ChangeSecureModeStatusForm Form Class"""

    class Meta:
        """Meta class for ChangeSecureModeStatusForm Form"""

        model = CustomUser
        fields = ("secure_mode",)
