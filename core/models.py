from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from . user_manager import UserManager
from org.models import Org
    

class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique = True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    org = models.ForeignKey(Org, on_delete=models.CASCADE)
    is_org_admin = models.BooleanField(_('is admin'), default=False)
    is_dept_incharge = models.BooleanField(_('is department incharge'), default=False)
    is_lab_staff = models.BooleanField(_('is lab staff'), default=False)
    
    def __str__(self):
        return f"{str(self.first_name)} {str(self.last_name)}"
    
    
class Department(models.Model):
    org = models.ForeignKey(Org, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    incharge = models.OneToOneField(UserProfile, on_delete=models.DO_NOTHING)
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

    