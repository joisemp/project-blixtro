from django.http import HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import generic, View
from . models import Item, Lab, Group, Category, GroupItem
from .forms import LabCreateForm, GroupItemCreateForm
from . mixins import StaffAccessCheckMixin, AdminOnlyAccessMixin
from core.models import Org, UserProfile
from django.contrib.auth.mixins import LoginRequiredMixin


class LabListView(LoginRequiredMixin, generic.ListView):
    template_name = "lab/labs-list.html"
    model = Lab
    ordering = ['-id']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["labs"] = Lab.objects.all()
        return context
    

class LabCreateView(generic.CreateView):
    model = Lab
    form_class = LabCreateForm
    template_name = "lab/lab-create.html"
    
    def get_success_url(self):
        lab = self.object
        org_id = self.kwargs['org_id']
        return reverse('lab:item-list', kwargs={'org_id':org_id, 'lab_id': lab.pk})
    
    def form_valid(self, form):
        selected_users = form.cleaned_data['users']
        org_id = self.kwargs["org_id"]
        org = Org.objects.get(pk=org_id)
        lab = form.save(commit=False)
        lab.org = org
        lab.save()
        lab.user.set(selected_users)
        return super().form_valid(form)
    

class UpdateLabView(generic.UpdateView):
    template_name = 'lab/lab-update.html'
    model = Lab
    form_class = LabCreateForm
    
    def get_object(self, queryset=None):
        lab_id = self.kwargs['lab_id']
        queryset = self.get_queryset()
        return queryset.get(pk=lab_id)
    
    def get_form(self):
        form = super().get_form()
        lab = self.get_object()
        form.fields['users'].initial = lab.user.all()
        return form
    
    def form_valid(self, form):
        selected_users = form.cleaned_data['users']
        lab = form.save(commit=False)
        lab.user.set(selected_users)
        lab.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        lab = self.object
        return reverse('lab:item-list', kwargs={'lab_id': lab.pk})
    
    
class DeleteLabView(generic.DeleteView):
    model = Lab
    template_name = "lab/lab-delete.html"
    
    def get_object(self, queryset=None):
        lab_id = self.kwargs['lab_id']
        queryset = self.get_queryset()
        return queryset.get(pk=lab_id)
    
    def get_success_url(self):
        return reverse('lab:lab-list')


class GroupCreateView(generic.CreateView):
    template_name = 'lab/create-group.html'
    model = Group
    fields = ["title"]
    
    def form_valid(self, form):
        item_group = form.save(commit=False)
        labid = self.kwargs["lab_id"]
        lab = Lab.objects.get(pk=labid)
        item_group.lab = lab
        item_group.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        lab_pk = self.kwargs["lab_id"]
        org_id = self.kwargs["org_id"]
        return reverse('lab:group-list', kwargs={'lab_id': lab_pk, 'org_id':org_id})
    

class GroupListView(generic.ListView):
    template_name = "lab/group-list.html"
    model = Group
    ordering = ['-id']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lab = get_object_or_404(Lab, pk=self.kwargs['lab_id'])
        groups = Group.objects.filter(lab=lab)
        context["groups"] = groups
        context["lab"] = lab
        return context


class GroupDetailView(generic.TemplateView):
    template_name = "lab/group-detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group = get_object_or_404(Group, pk=self.kwargs['group'])
        lab = get_object_or_404(Lab, pk=self.kwargs['lab_id'])
        group_items = GroupItem.objects.filter(group = group)
        context['group'] = group
        context['lab'] = lab
        context['group_items'] = group_items
        return context


class GroupDeleteView(View):
    model = Group

    def get(self, request, *args, **kwargs):
        group_id = self.kwargs["group"]
        group = get_object_or_404(self.model, pk=group_id)
        group.delete()
        lab_id = self.kwargs["lab_id"]
        org_id = self.kwargs["org_id"]
        return redirect(reverse('lab:group-list', kwargs={'lab_id': lab_id, 'org_id':org_id}))
        

class GroupUpdateView(generic.UpdateView):
    ...
  
    
class CreateItemView(generic.CreateView):
    template_name = 'lab/add-item.html'
    model = Item    
    fields = ["item_name", "total_qty", "unit_of_measure", "category"]
    
    def form_valid(self, form):
        item = form.save(commit=False)
        labid = self.kwargs["lab_id"]
        lab = Lab.objects.get(pk=labid)
        item.lab = lab
        item.save()
        return super().form_valid(form)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        lab = get_object_or_404(Lab, pk=self.kwargs['lab_id'])
        form.fields['category'].queryset = Category.objects.filter(lab=lab)
        return form

    def get_success_url(self):
        lab_pk = self.kwargs["lab_id"]
        org_id = self.kwargs["org_id"]
        return reverse('lab:item-list', kwargs={'org_id':org_id, 'lab_id': lab_pk})
    
    
class ItemListView(generic.ListView):
    template_name = "lab/item-list.html"
    model = Item
    ordering = ['-id']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lab = get_object_or_404(Lab, pk=self.kwargs['lab_id'])
        items = Item.objects.filter(lab=lab)
        context["items"] = items
        context["lab"] = lab
        return context    

    
class ItemUpdateView(generic.UpdateView):
    model = Item
    template_name = "lab/item-update.html"
    fields = ["total_qty", "category", "unit_of_measure"]
    
    def get_object(self, queryset=None):
        item_id = self.kwargs['item_id']
        queryset = self.get_queryset()
        return queryset.get(pk=item_id)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        item = self.get_object()
        form.fields['category'].queryset = Category.objects.filter(lab=item.lab)
        return form
    
    def get_success_url(self):
        lab_pk = self.kwargs["lab_id"]
        org_id = self.kwargs["org_id"]
        return reverse('lab:item-list', kwargs={'lab_id': lab_pk, 'org_id':org_id})
    

class ItemDeleteView(View):
    model = Item

    def get(self, request, *args, **kwargs):
        item_id = self.kwargs["item_id"]
        lab_pk = self.kwargs["lab_id"]
        org_id = self.kwargs["org_id"]
        item = get_object_or_404(self.model, pk=item_id)
        item.delete()
        return reverse('lab:item-list', kwargs={'lab_id': lab_pk, 'org_id':org_id})


class GroupItemCreateView(generic.CreateView):
    template_name = 'lab/add-group-item.html'
    model = GroupItem    
    form_class = GroupItemCreateForm
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        lab = get_object_or_404(Lab, pk=self.kwargs['lab_id'])
        form.fields['item'].queryset = Item.objects.filter(lab=lab)
        return form
    
    def form_valid(self, form):
        group_item = form.save(commit=False)
        group_id = self.kwargs["group"]
        lab = Group.objects.get(pk=group_id)
        group_item.group = lab
        group_item.save()
        return super().form_valid(form)

    def get_success_url(self):
        lab_pk = self.kwargs["lab_id"]
        group_id = self.kwargs["group"]
        return reverse('lab:group-detail', kwargs={'lab_id': lab_pk, 'group':group_id})


class GroupItemDeleteView(View):
    model = GroupItem

    def get(self, request, *args, **kwargs):
        group_item = GroupItem.objects.get(pk = self.kwargs["group_item"])
        group_item.delete()
        lab_pk = self.kwargs["lab_id"]
        group_id = self.kwargs["group"]
        return HttpResponsePermanentRedirect(reverse('lab:group-detail', kwargs={'lab_id': lab_pk, 'group':group_id}))
    

class GroupItemUpdateView(generic.UpdateView):
    model = GroupItem
    template_name = 'lab/update-group-item.html'
    form_class = GroupItemCreateForm
    
    def get_object(self, queryset=None):
        group_item_id = self.kwargs['group_item']
        queryset = self.get_queryset()
        return queryset.get(pk=group_item_id)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        lab = get_object_or_404(Lab, pk=self.kwargs['lab_id'])
        form.fields['item'].queryset = Item.objects.filter(lab=lab)
        return form

    def get_success_url(self):
        lab_pk = self.kwargs["lab_id"]
        group_id = self.kwargs["group"]
        return reverse('lab:group-detail', kwargs={'lab_id': lab_pk, 'group':group_id})
    
    
class CategoryListView(generic.ListView):
    template_name = "lab/category-list.html"
    model = Category
    ordering = ['-id']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lab = get_object_or_404(Lab, pk=self.kwargs['lab_id'])
        categories = Category.objects.filter(lab=lab)
        context["categories"] = categories
        context["lab"] = lab
        return context 
    
class CategoryCreateView(generic.CreateView):
    template_name = 'lab/create-category.html'
    model = Category    
    fields = ["category_name"]
    
    def form_valid(self, form):
        category = form.save(commit=False)
        lab = Lab.objects.get(pk=self.kwargs["lab_id"])
        category.lab = lab
        category.save()
        return super().form_valid(form)

    def get_success_url(self):
        lab_pk = self.kwargs["lab_id"]
        return reverse('lab:category-list', kwargs={'lab_id': lab_pk})
    

class CategoryDeleteView(View):
    model = Category

    def get(self, request, *args, **kwargs):
        category = Category.objects.get(pk = self.kwargs["category"])
        category.delete()
        lab_pk = self.kwargs["lab_id"]
        return HttpResponsePermanentRedirect(reverse('lab:category-list', kwargs={'lab_id': lab_pk}))
    
    
    