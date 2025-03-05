from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponsePermanentRedirect
from inventory.models import Room
from django.urls import reverse
from django.http import Http404
    

class RedirectLoggedInUsersMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not getattr(request.user, "profile", None):
                raise Http404("User profile not found.")

            if request.user.profile.is_central_admin:
                return HttpResponsePermanentRedirect(reverse('central_admin:dashboard'))
            if request.user.profile.is_incharge:
                room = Room.objects.get(incharge=request.user.profile)
                return HttpResponsePermanentRedirect(reverse('room_incharge:room_dashboard', kwargs={'room_slug': room.slug}))

        return super().dispatch(request, *args, **kwargs)