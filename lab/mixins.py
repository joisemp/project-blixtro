from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import redirect
from django.urls import reverse
from . models import Lab
from core.models import UserProfile, Department




class StaffAccessCheckMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff and not request.user.is_superuser and not request.user.is_admin:
                try: 
                    lab_id = self.kwargs['pk']
                    lab = Lab.objects.get(pk = lab_id)
                    if not request.user in lab.user.all():
                        return redirect('lab:lab-list')
                except:
                    pass
        return super().dispatch(request, *args, **kwargs)
    

class RedirectLoggedInUserMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            userprofile = UserProfile.objects.get(user = request.user)
            
            if userprofile.is_org_admin:
                org = userprofile.org
                return HttpResponsePermanentRedirect(reverse('org-dashboard', kwargs={'org_id':org.pk}))
            
            elif userprofile.is_dept_incharge:
                dept = Department.objects.get(incharge = userprofile)
                org = dept.org
                return HttpResponsePermanentRedirect(reverse('lab:lab-list', kwargs={'org_id':org.pk, 'dept_id':dept.pk}))

            elif userprofile.is_lab_staff:
                # return redirect()
                ...
        else:
            return HttpResponsePermanentRedirect(reverse('core:login'))
        return super().dispatch(request, *args, **kwargs)
        

class AdminOnlyAccessMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.is_superuser and not request.user.is_admin:
                return redirect('landing-page')
        return super().dispatch(request, *args, **kwargs)