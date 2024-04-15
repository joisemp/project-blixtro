from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from . models import Lab


class StaffAccessCheckMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff and not request.user.is_superuser and not request.user.is_admin:
                lab_id = self.kwargs['pk']
                lab = Lab.objects.get(pk = lab_id)
                if not request.user in lab.user.all():
                    return redirect('lab:lab-list')
        return super().dispatch(request, *args, **kwargs)
    

class RedirectLoggedInUserMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('lab:lab-list')
        return super().dispatch(request, *args, **kwargs)
        

class AdminOnlyAccessMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.is_superuser and not request.user.is_admin:
                return redirect('landing-page')
        return super().dispatch(request, *args, **kwargs)