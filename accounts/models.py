from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from . user_manager import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique = True)
    is_admin = models.BooleanField(_('is admin'), default = False)
    is_staff = models.BooleanField(_('is staff'), default = False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = UserManager()