from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from . manager import CustomUserManager


class CustomUser(AbstractUser):
    objects = CustomUserManager()

    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email