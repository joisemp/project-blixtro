from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponsePermanentRedirect
from django.urls import reverse
from apps.core.models import UserProfile, Department, Org
from django.http import Http404

    

class RedirectLoggedInUserMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            
            if request.user.profile.is_org_admin:
                return HttpResponsePermanentRedirect(
                    reverse(
                        'org:dept-list', 
                        kwargs={
                            'org_id':request.user.profile.org.pk
                            }
                        )
                    )
                
            elif request.user.profile.is_dept_incharge or request.user.profile.is_lab_staff:
                return HttpResponsePermanentRedirect(
                    reverse(
                        'org:lab:lab-list', 
                        kwargs={
                            'org_id':request.user.profile.org.pk, 
                            'dept_id':request.user.profile.dept.pk
                            }
                        )
                    )
        
        return super().dispatch(request, *args, **kwargs)    


class OrgAdminOnlyAccessMixin(AccessMixin):
    ...
    

class DeptHeadOnlyAccessMixin(AccessMixin):
    ...
        

class LabAccessMixin(AccessMixin):
    ...


