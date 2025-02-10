from django.views.generic.base import TemplateView

class DashboardView(TemplateView):
    template_name = 'central_admin/dashboard.html'
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        return context

class PeopleListView(TemplateView):
    template_name = 'central_admin/peoplelist.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

class RoomListView(TemplateView):
    template_name = 'central_admin/room.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
    
class VendorListView(TemplateView):
    template_name = 'central_admin/vendor.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)