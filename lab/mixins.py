from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponsePermanentRedirect
from django.urls import reverse
from . models import Lab
from core.models import UserProfile, Department, Org
from django.http import Http404

    

class RedirectLoggedInUserMixin(AccessMixin):
    ...
        

class AdminOnlyAccessMixin(AccessMixin):
    ...
    

class DeptAdminOnlyAccessMixin(AccessMixin):
    ...
        

class LabAccessMixin(AccessMixin):
    ...


