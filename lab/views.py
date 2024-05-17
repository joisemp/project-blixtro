from typing import Any
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import generic, View
from . models import Item, Lab, Category, System, Brand, LabSettings
from core.models import Department
from .forms import LabCreateForm, BrandCreateForm, LabSettingsForm
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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["org_id"] = self.kwargs["org_id"]
        context["dept_id"] = self.kwargs["dept_id"]
        return context
    
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
        org_id = self.kwargs["org_id"]
        dept_id = self.kwargs["dept_id"]
        return reverse('lab:lab-list', kwargs={'org_id':org_id, 'dept_id':dept_id})
    
    
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
    fields = ["item_name", "total_qty", "unit_of_measure", "brand", "category"]
    
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
        form.fields['brand'].queryset = Brand.objects.filter(lab=lab)
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
        try:
            context["lab_settings"] = LabSettings.objects.get(lab=lab)
        except LabSettings.DoesNotExist:
            pass
        return context    

    
class ItemUpdateView(generic.UpdateView):
    model = Item
    template_name = "lab/item-update.html"
    fields = ["item_name", "total_qty", "brand", "category", "unit_of_measure"]
    
    def get_object(self, queryset=None):
        item_id = self.kwargs['item_id']
        queryset = self.get_queryset()
        return queryset.get(pk=item_id)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        item = self.get_object()
        form.fields['category'].queryset = Category.objects.filter(lab=item.lab)
        form.fields['brand'].queryset = Brand.objects.filter(lab=item.lab)
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
        try:
            context["lab_settings"] = LabSettings.objects.get(lab=lab)
        except LabSettings.DoesNotExist:
            pass
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
        org_id = self.kwargs["org_id"]
        dept_id = self.kwargs["dept_id"]
        return HttpResponsePermanentRedirect(reverse('lab:category-list', kwargs={'lab_id': lab_pk, 'org_id':org_id, 'dept_id':dept_id}))
    

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
        try:
            context["lab_settings"] = LabSettings.objects.get(lab=lab)
        except LabSettings.DoesNotExist:
            pass
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
        return reverse('lab:system-list', kwargs={'org_id':org_id, 'dept_id':dept_id, 'lab_id': lab_pk})
    
class SystemDeleteView(View):
    model = System

    def get(self, request, *args, **kwargs):
        system = System.objects.get(pk = self.kwargs["sys_id"])
        system.delete()
        lab_pk = self.kwargs["lab_id"]
        dept_id = self.kwargs["dept_id"]
        org_id = self.kwargs["org_id"]
        return HttpResponsePermanentRedirect(reverse('lab:system-list', kwargs={'org_id':org_id, 'dept_id':dept_id, 'lab_id': lab_pk}))


class BrandListView(generic.ListView):
    template_name = 'lab/brand-list.html'
    model = Brand
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lab_id = self.kwargs["lab_id"]
        lab = Lab.objects.get(pk=lab_id)
        context["brands"] = Brand.objects.filter(lab = lab)
        context["org_id"] = self.kwargs["org_id"]
        context["dept_id"] = self.kwargs["dept_id"]
        context["lab_id"] = lab_id
        context["lab"] = lab
        try:
            context["lab_settings"] = LabSettings.objects.get(lab=lab)
        except LabSettings.DoesNotExist:
            pass
        return context


class BrandCreateView(generic.FormView):
    model = Brand
    form_class = BrandCreateForm
    
    def form_valid(self, form):
        brand_name = form.cleaned_data.get('brand_name')
        lab_id = self.kwargs["lab_id"]
        lab = Lab.objects.get(pk=lab_id)
        
        Brand.objects.create(
            brand_name = brand_name,
            lab = lab
        )
        
        return super().form_valid(form)
        
    def get_success_url(self):
        org_id = self.kwargs["org_id"]
        dept_id = self.kwargs["dept_id"]
        lab_id = self.kwargs["lab_id"]
        return reverse('lab:brand-list', kwargs={'org_id':org_id, 'dept_id':dept_id, 'lab_id':lab_id})
    
    
class LabSettingsView(generic.CreateView, generic.UpdateView):
    model = LabSettings
    template_name = 'lab/lab_settings.html'
    form_class = LabSettingsForm

    def get_object(self, queryset=None):
        lab_id = self.kwargs['lab_id']
        queryset = self.get_queryset()
        try:
            return queryset.get(pk=lab_id)
        except LabSettings.DoesNotExist:
            return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lab_id = self.kwargs['lab_id']
        lab_settings = self.get_object()
        lab = get_object_or_404(Lab, pk=lab_id)
        context["org"] = Org.objects.get(pk=self.kwargs["org_id"])
        context["dept"] = Department.objects.get(pk=self.kwargs["dept_id"])
        try:
            context["lab_settings"] = LabSettings.objects.get(lab=lab)
        except LabSettings.DoesNotExist:
            pass

        if lab_settings:
            context['lab'] = lab_settings.lab
        else:
            lab = get_object_or_404(Lab, pk=lab_id)
            context['lab'] = lab

        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        lab_settings = self.get_object()

        if lab_settings:
            kwargs['instance'] = lab_settings
        else:
            lab_id = self.kwargs['lab_id']
            lab = Lab.objects.get(pk=lab_id)
            kwargs['instance'] = LabSettings(lab=lab)

        return kwargs

    def form_valid(self, form):
        form.save()
        # No redirection in form_valid, render the same page
        return self.render_to_response(self.get_context_data(form=form))
        
    def get_success_url(self):
        org_id = self.kwargs["org_id"]
        dept_id = self.kwargs["dept_id"]
        lab_id = self.kwargs["lab_id"]
        return HttpResponsePermanentRedirect(reverse('lab:lab-settings', kwargs={'org_id':org_id, 'dept_id':dept_id, 'lab_id':lab_id}))    
    
    