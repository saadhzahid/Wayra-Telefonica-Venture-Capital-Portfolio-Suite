from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.core.validators import validate_image_file_extension
from django.db import models

from portfolio.models.manager import UserManager


# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name='Email address',
                              max_length=255,
                              unique=True,
                              validators=[EmailValidator()],
                              )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    profile_picture = models.ImageField(blank=True, validators=[validate_image_file_extension])
    is_active = models.BooleanField(default=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']
