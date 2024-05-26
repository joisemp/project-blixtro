from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import redirect
from django.urls import reverse
from . models import Lab
from core.models import UserProfile, Department, Org
from django.http import Http404

    

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
                org = userprofile.org
                lab = userprofile.lab_set.all()[0]
                dept = lab.dept
                return HttpResponsePermanentRedirect(reverse('lab:lab-list', kwargs={'org_id':org.pk, 'dept_id':dept.pk}))
        else:
            return HttpResponsePermanentRedirect(reverse('core:login'))
        return super().dispatch(request, *args, **kwargs)
        

class AdminOnlyAccessMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            userprofile = UserProfile.objects.get(user = request.user)
            org = Org.objects.get(pk = kwargs.get("org_id"))
            if not userprofile.is_org_admin:
                raise Http404("Only access to organisation admin")
            elif not userprofile.org == org:
                raise Http404("You are not in this Orgaisation")
        return super().dispatch(request, *args, **kwargs)
    

class DeptAdminOnlyAccessMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            userprofile = UserProfile.objects.get(user = request.user)
            if not userprofile.is_dept_incharge:
                raise Http404("Departement Admin Only Access")
            else:
                departement = Department.objects.get(pk = kwargs.get("dept_id"))
                if not departement.incharge == userprofile:
                    raise Http404("You are not in this department")
            return super().dispatch(request, *args, **kwargs)
        

class LabAccessMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            userprofile = UserProfile.objects.get(user = request.user)
            lab = Lab.objects.get(pk = kwargs.get("lab_id"))
            org = Org.objects.get(pk = kwargs.get("org_id"))
            if not userprofile.org == org:
                raise Http404("You are not in this organisation")
            if userprofile.is_lab_staff:
                if not lab in userprofile.lab_set.all():
                    raise Http404("You are not assigned to this lab")
            if userprofile.is_dept_incharge:
                departement = Department.objects.get(pk = kwargs.get("dept_id"))
                if not departement.incharge == userprofile:
                    raise Http404("You are not in this department")
        return super().dispatch(request, *args, **kwargs)


