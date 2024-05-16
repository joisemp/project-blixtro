from django.http import HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import generic, View
from . models import Item, Lab, Category, System
from core.models import Department
from .forms import LabCreateForm
from . mixins import StaffAccessCheckMixin, AdminOnlyAccessMixin
from core.models import Org
from django.contrib.auth.mixins import LoginRequiredMixin


class LabListView(LoginRequiredMixin, generic.ListView):
    template_name = "lab/labs-list.html"
    model = Lab
    ordering = ['-id']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        org = Org.objects.get(pk=self.kwargs["org_id"])
        dept = Department.objects.get(pk=self.kwargs["dept_id"])
        context["org"] = org
        context["dept"] = dept
        context["labs"] = Lab.objects.filter(org=org, dept=dept)
        return context
    

class LabCreateView(generic.CreateView):
    model = Lab
    form_class = LabCreateForm
    template_name = "lab/lab-create.html"
    
    def get_success_url(self):
        lab = self.object
        org_id = self.kwargs['org_id']
        dept_id = self.kwargs['dept_id']
        return reverse('lab:item-list', kwargs={'org_id':org_id, 'lab_id': lab.pk, 'dept_id':dept_id})
    
    def form_valid(self, form):
        selected_users = form.cleaned_data['users']
        org_id = self.kwargs["org_id"]
        dept_id = self.kwargs["dept_id"]
        org = Org.objects.get(pk=org_id)
        dept = Department.objects.get(pk=dept_id)
        lab = form.save(commit=False)
        lab.org = org
        lab.dept = dept
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
        org_id = self.kwargs["org_id"]
        dept_id = self.kwargs["dept_id"]
        return reverse('lab:lab-list', kwargs={'org_id':org_id, 'dept_id':dept_id})
  
    
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
        dept_id = self.kwargs["dept_id"]
        return reverse('lab:item-list', kwargs={'org_id':org_id, 'lab_id': lab_pk, 'dept_id':dept_id})
    
    
class ItemListView(generic.ListView):
    template_name = "lab/item-list.html"
    model = Item
    ordering = ['-id']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lab = get_object_or_404(Lab, pk=self.kwargs['lab_id'])
        items = Item.objects.filter(lab=lab)
        systems = System.objects.filter(lab=lab)
        context["org"] = Org.objects.get(pk=self.kwargs["org_id"])
        context["dept"] = Department.objects.get(pk=self.kwargs["dept_id"])
        context["systems"] = systems
        context["items"] = items
        context["lab"] = lab
        return context    

    
class ItemUpdateView(generic.UpdateView):
    model = Item
    template_name = "lab/item-update.html"
    fields = ["item_name", "total_qty", "category", "unit_of_measure"]
    
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
        dept_id = self.kwargs["dept_id"]
        return reverse('lab:item-list', kwargs={'lab_id': lab_pk, 'org_id':org_id, 'dept_id':dept_id})
    

class ItemDeleteView(View):
    model = Item

    def get(self, request, *args, **kwargs):
        item_id = self.kwargs["item_id"]
        lab_pk = self.kwargs["lab_id"]
        org_id = self.kwargs["org_id"]
        dept_id = self.kwargs["dept_id"]
        item = get_object_or_404(self.model, pk=item_id)
        item.delete()
        return HttpResponsePermanentRedirect(reverse('lab:item-list', kwargs={'lab_id': lab_pk, 'org_id':org_id, 'dept_id':dept_id}))
    
    
class CategoryListView(generic.ListView):
    template_name = "lab/category-list.html"
    model = Category
    ordering = ['-id']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lab = get_object_or_404(Lab, pk=self.kwargs['lab_id'])
        categories = Category.objects.filter(lab=lab)
        context["categories"] = categories
        context["org"] = Org.objects.get(pk=self.kwargs["org_id"])
        context["dept"] = Department.objects.get(pk=self.kwargs["dept_id"])
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
        org_id = self.kwargs["org_id"]
        dept_id = self.kwargs["dept_id"]
        return reverse('lab:category-list', kwargs={'lab_id': lab_pk, 'org_id':org_id, 'dept_id':dept_id})
    

class CategoryDeleteView(View):
    model = Category

    def get(self, request, *args, **kwargs):
        category = Category.objects.get(pk = self.kwargs["category"])
        category.delete()
        lab_pk = self.kwargs["lab_id"]
        return HttpResponsePermanentRedirect(reverse('lab:category-list', kwargs={'lab_id': lab_pk}))
    

class SystemCreateView(generic.CreateView):
    model = System    
    fields = ['sys_name', 'processor', 'ram', 'hdd', 'os', 'monitor', 'mouse', 'keyboard', 'cpu_cabin', 'status']
    template_name = "lab/system-create.html"
    
    def form_valid(self, form):
        item = form.save(commit=False)
        labid = self.kwargs["lab_id"]
        lab = Lab.objects.get(pk=labid)
        item.lab = lab
        item.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        lab_pk = self.kwargs["lab_id"]
        dept_id = self.kwargs["dept_id"]
        org_id = self.kwargs["org_id"]
        return reverse('lab:system-list', kwargs={'org_id':org_id, 'dept_id':dept_id, 'lab_id': lab_pk})
    

class SystemListView(generic.ListView):
    template_name = "lab/system-list.html"
    model = Item
    ordering = ['-id']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lab = get_object_or_404(Lab, pk=self.kwargs['lab_id'])
        systems = System.objects.filter(lab=lab)
        context["org"] = Org.objects.get(pk=self.kwargs["org_id"])
        context["dept"] = Department.objects.get(pk=self.kwargs["dept_id"])
        context["systems"] = systems
        context["lab"] = lab
        return context 
    

class SystemUpdateView(generic.UpdateView):
    model = System    
    fields = ['sys_name', 'processor', 'ram', 'hdd', 'os', 'monitor', 'mouse', 'keyboard', 'cpu_cabin', 'status']
    template_name = "lab/system-update.html"
    
    def get_object(self, queryset=None):
        sys_id = self.kwargs['sys_id']
        queryset = self.get_queryset()
        return queryset.get(pk=sys_id)
    
    def get_success_url(self):
        lab_pk = self.kwargs["lab_id"]
        dept_id = self.kwargs["dept_id"]
        org_id = self.kwargs["org_id"]
        return reverse('lab:item-list', kwargs={'org_id':org_id, 'dept_id':dept_id, 'lab_id': lab_pk})