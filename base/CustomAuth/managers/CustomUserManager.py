from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
   
    # def create_user(self, email, password,  **extra_fields):
        
    #     if not email:
    #         raise ValueError(_('The Email must be set'))
    #     email = self.normalize_email(email)
    #     user = self.model(email=email, **extra_fields)
    #     user.set_password(password)
    #     user.save()
    #     return user

    # def create_superuser(self, email, password,  **extra_fields):
    #     extra_fields.setdefault('is_staff', True)
    #     extra_fields.setdefault('is_superuser', True)
    #     extra_fields.setdefault('is_active', True)

    #     if extra_fields.get('is_staff') is not True:
    #         raise ValueError(_('Superuser must have is_staff=True.'))
    #     if extra_fields.get('is_superuser') is not True:
    #         raise ValueError(_('Superuser must have is_superuser=True.'))
    #     return self.create_user(email, password, **extra_fields)

    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not first_name:
            raise ValueError("Users must have an userusername")
        if not last_name:
            raise ValueError("Users must have an userusername")

        user = self.model(
                    email=self.normalize_email(email),
                    first_name=first_name,
                    last_name=last_name,
                )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,first_name, last_name, password):
        user = self._create_user(
                email=self.normalize_email(email),
                password=password,
                first_name= first_name,
                last_name=last_name,
            )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True 
        user.save(using=self._db)
        return user