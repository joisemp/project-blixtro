from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from core.models import UserProfile
from inventory.models import Room, Vendor, Purchase, Issue

class DashboardView(TemplateView):
    template_name = 'central_admin/dashboard.html'
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PeopleListView(ListView):
    template_name = 'central_admin/people_list.html'
    model = UserProfile
    context_object_name = 'people'
    
    def get_qeryset(self):
        return super().get_queryset().filter(organisation=self.request.user.organisation)
    

class RoomListView(ListView):
    template_name = 'central_admin/room_list.html'
    model = Room
    context_object_name = 'rooms'

    def get_queryset(self):
        return super().get_queryset().filter(organisation=self.request.user.profile.org)
    
    
class VendorListView(ListView):
    template_name = 'central_admin/vendor_list.html'
    model = Vendor
    context_object_name = 'vendors'
    
    def get_queryset(self):
        return super().get_queryset().filter(organisation=self.request.user.organisation)


class PurchaseListView(ListView):
    template_name = 'central_admin/purchase_list.html'
    model = Purchase
    context_object_name = 'purchases'
    
    def get_queryset(self):
        return super().get_queryset().filter(organisation=self.request.user.organisation)


class IssueListView(ListView):
    template_name = 'central_admin/issue_list.html'
    model = Issue
    context_object_name = 'issues'
    
    def get_queryset(self):
        return super().get_queryset().filter(organisation=self.request.user.organisation)
    
    