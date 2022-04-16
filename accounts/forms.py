from captcha.fields import CaptchaField
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """CustomUserCreationForm Form Class"""

    captcha = CaptchaField()

    class Meta:
        """Meta class for CustomUserCreationForm Form"""

        model = CustomUser
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
        )


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
            "show_github",
            "default_theme",
        )
