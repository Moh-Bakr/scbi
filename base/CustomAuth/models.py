from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers.CustomUserManager import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    isEmailVerified = models.BooleanField(default=False)
    first_name = models.CharField(_("first name"), max_length=100)
    last_name = models.CharField(_("last name"), max_length=100)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [first_name, last_name]

    objects = CustomUserManager()

    def __str__(self):
        return self.email