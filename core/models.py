from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from . user_manager import UserManager


class Org(models.Model):
    org_name = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    website_url = models.CharField(max_length=255)
    address = models.TextField()


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique = True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    org = models.ForeignKey(Org, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_org_admin = models.BooleanField(_('is admin'), default=False)
    is_dept_incharge = models.BooleanField(_('is department incharge'), default=False)
    is_lab_staff = models.BooleanField(_('is admin'), default=False)
    
    def __str__(self):
        return f"{str(self.first_name)} {str(self.last_name)}"
    
    