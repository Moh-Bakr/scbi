from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .managers.CustomUserManager import CustomUserManager
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.urls import reverse
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string, get_template
from django_rest_passwordreset.signals import reset_password_token_created
from django.contrib.auth.models import PermissionsMixin
# class CustomUser(AbstractUser):
#     username = None
#     email = models.EmailField(_('email address'), unique=True)
#     isEmailVerified = models.BooleanField(default=False)
#     first_name = models.CharField(_("first name"), max_length=100)
#     last_name = models.CharField(_("last name"), max_length=100)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = [first_name,last_name]

#     objects = CustomUserManager()

#     def __str__(self):
#         return self.email


class CustomUser(AbstractBaseUser , PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_joined = models.DateTimeField(
        verbose_name='date joined', auto_now_add=True)
    isEmailVerified = models.BooleanField(default=False)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True, blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'firstname': reset_password_token.user.first_name,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(
            instance.request.build_absolute_uri(
                reverse('password_reset:reset-password-confirm')),
            reset_password_token.key),
        'token': reset_password_token.key
    }

    # render email text
    # email_html_message = render_to_string('email/user_reset_password.html', context)
    email_html_message = get_template(
        'email/user_reset_password.html').render(context)
    email_plaintext_message = render_to_string(
        'email/user_reset_password.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="Your Account"),
        # message:
        email_plaintext_message,
        # from:
        "itmail.projects@gmail.com",
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()


def get_password_reset_token_expiry_time():
    # get token validation time
    return getattr(settings, 'DJANGO_REST_MULTITOKENAUTH_RESET_TOKEN_EXPIRY_TIME', 1)
