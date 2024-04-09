from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from . models import Item, Lab, ItemGroup
from . utils import get_total_item_qty
from .forms import LabCreateForm


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


class LabItemsListView(generic.ListView):
    template_name = "lab/items-list.html"
    model = Item
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lab_id = self.kwargs['pk']
        item_name = self.kwargs['item_name']
        items = Item.objects.filter(lab__pk=lab_id, item_name=item_name)
        context["items"] = items
        return context
    

class LabCreateView(generic.CreateView):
    model = Lab
    form_class = LabCreateForm
    template_name = "lab/lab-create.html"
    
    def get_success_url(self):
        lab = self.object
        return reverse('lab:lab-detail', kwargs={'pk': lab.pk})
    
    def form_valid(self, form):
        selected_users = form.cleaned_data['users']
        lab = form.save(commit=False)
        lab.save()
        lab.user.set(selected_users)
        return super().form_valid(form)