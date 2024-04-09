from django.shortcuts import get_object_or_404, render
from django.views import generic
from . models import Item, Lab, ItemGroup
from . utils import get_total_item_qty


class LabListView(generic.ListView):
    template_name = "lab/labs-list.html"
    queryset = Lab.objects.all()
    context_object_name = 'labs'
    ordering = ['-id']
    

class LabDetailView(generic.DetailView):
    template_name = "lab/lab-detail.html"
    model = Lab
    context_object_name = "lab"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lab = get_object_or_404(Lab, pk=self.kwargs['pk'])
        items = Item.objects.filter(lab=lab)
        groups = ItemGroup.objects.filter(lab=lab)
        context["items"] = get_total_item_qty(items)
        context["groups"] = groups
        return context

