from django.views.generic.base import TemplateView
from core.models import UserProfile

class DashboardView(TemplateView):
    template_name = 'central_admin/dashboard.html'
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        return context

class PeopleListView(TemplateView):
    template_name = 'central_admin/people_list.html'
    model = UserProfile
    context_object_name = 'people'
    
    def get_qeryset(self):
        # Filter the queryset based on the current user organisation
        return self.model.objects.all()
    

class RoomListView(TemplateView):
    template_name = 'central_admin/room_list.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
    
    
class VendorListView(TemplateView):
    template_name = 'central_admin/vendor_list.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class PurchaseListView(TemplateView):
    template_name = 'central_admin/purchase_list.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class IssueListView(TemplateView):
    template_name = 'central_admin/issue_list.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)