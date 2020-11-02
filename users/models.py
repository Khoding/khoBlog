from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    pass
    profile_pic = models.ImageField(null=True, blank=True, upload_to="images/profile/")

