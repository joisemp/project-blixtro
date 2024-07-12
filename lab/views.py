from django.http import HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import generic, View

from lab.mixins import LabAccessMixin, DeptAdminOnlyAccessMixin
from . models import Item, Lab, Category, LabRecord, System, Brand, LabSettings
from core.models import Department
from .forms import LabCreateForm, BrandCreateForm, LabSettingsForm
from org.models import Org
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import ForeignKey, ManyToManyField 
from core.models import UserProfile
from .utils import generate_unique_code



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
        userprofile = UserProfile.objects.get(user = self.request.user)
        context["userprofile"] = userprofile
        if userprofile.is_lab_staff:
            context["labs"] = userprofile.lab_set.all()
        else:
            context["labs"] = Lab.objects.filter(org = org, dept = dept)
        return context
    
    
class LabCreateView(LoginRequiredMixin, DeptAdminOnlyAccessMixin, generic.CreateView):
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
        return reverse('lab:lab-settings', kwargs={'org_id':org_id, 'lab_id': lab.pk, 'dept_id':dept_id})
    
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
    

class UpdateLabView(LoginRequiredMixin, LabAccessMixin, DeptAdminOnlyAccessMixin, generic.UpdateView):
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
    
class DeleteLabView(LoginRequiredMixin, LabAccessMixin, DeptAdminOnlyAccessMixin, View):
    model = Lab

    def get(self, request, *args, **kwargs):
        lab_pk = self.kwargs["lab_id"]
        lab = Lab.objects.get(pk=lab_pk)
        lab.delete()
        org_id = self.kwargs["org_id"]
        dept_id = self.kwargs["dept_id"]
        return HttpResponsePermanentRedirect(reverse('lab:lab-list', kwargs={'org_id':org_id, 'dept_id':dept_id}))
  
    
class CreateItemView(LoginRequiredMixin, LabAccessMixin, generic.CreateView):
    template_name = 'lab/add-item.html'
    model = Item    
    fields = ["item_name", "total_qty", "unit_of_measure", "brand", "category", "date_of_purchase"]
    
    def form_valid(self, form):
        item = form.save(commit=False)
        item.total_available_qty = item.total_qty
        labid = self.kwargs["lab_id"]
        lab = Lab.objects.get(pk=labid)
        item.lab = lab
        item.unique_code = generate_unique_code(Item)
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
    
    
class ItemListView(LoginRequiredMixin, LabAccessMixin, generic.ListView):
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

    
class ItemUpdateView(LoginRequiredMixin, LabAccessMixin, generic.UpdateView):
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
    

class ItemDeleteView(LoginRequiredMixin, LabAccessMixin, View):
    model = Item

    def get(self, request, *args, **kwargs):
        item_id = self.kwargs["item_id"]
        lab_pk = self.kwargs["lab_id"]
        org_id = self.kwargs["org_id"]
        dept_id = self.kwargs["dept_id"]
        item = get_object_or_404(self.model, pk=item_id)
        item.delete()
        return HttpResponsePermanentRedirect(reverse('lab:item-list', kwargs={'lab_id': lab_pk, 'org_id':org_id, 'dept_id':dept_id}))
    
    
class CategoryListView(LoginRequiredMixin, LabAccessMixin, generic.ListView):
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
    
class CategoryCreateView(LoginRequiredMixin, LabAccessMixin, generic.CreateView):
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
    

class CategoryDeleteView(LoginRequiredMixin, LabAccessMixin, View):
    model = Category

    def get(self, request, *args, **kwargs):
        category = Category.objects.get(pk = self.kwargs["category"])
        category.delete()
        lab_pk = self.kwargs["lab_id"]
        org_id = self.kwargs["org_id"]
        dept_id = self.kwargs["dept_id"]
        return HttpResponsePermanentRedirect(reverse('lab:category-list', kwargs={'lab_id': lab_pk, 'org_id':org_id, 'dept_id':dept_id}))
    

class SystemCreateView(LoginRequiredMixin, LabAccessMixin, generic.CreateView):
    model = System    
    fields = ['sys_name',]
    template_name = "lab/system-create.html"
    
    def form_valid(self, form):
        system = form.save(commit=False)
        labid = self.kwargs["lab_id"]
        lab = Lab.objects.get(pk=labid)
        system.lab = lab
        system.status = 'not_working'
        system.unique_code = generate_unique_code(System)
        
        # with transaction.atomic():
        #     for field_name, value in form.cleaned_data.items():
        #         if field_name in ['processor', 'ram', 'hdd', 'os', 'monitor', 'mouse', 'keyboard', 'cpu_cabin']:
        #             item = getattr(system, field_name)
        #             if item:
        #                 item.in_use_qty += 1
        #                 item.total_available_qty -= 1
        #                 item.save()
            
        system.save()
        
        return super().form_valid(form)
    
    def get_success_url(self):
        lab_pk = self.kwargs["lab_id"]
        dept_id = self.kwargs["dept_id"]
        org_id = self.kwargs["org_id"]
        return reverse('lab:system-list', kwargs={'org_id':org_id, 'dept_id':dept_id, 'lab_id': lab_pk})
    

class SystemListView(LoginRequiredMixin, LabAccessMixin, generic.ListView):
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
    

class SystemUpdateView(LoginRequiredMixin, LabAccessMixin, generic.UpdateView):
    model = System    
    fields = ['sys_name', 'processor', 'ram', 'hdd', 'os', 'monitor', 'mouse', 'keyboard', 'cpu_cabin', 'status']
    template_name = "lab/system-update.html"
    
    
    def form_valid(self, form):
        system = form.save(commit=False)
        old_system = System.objects.get(pk=system.pk)

        item_updates = {}
        for field_name in self.fields:
            if field_name in ['processor', 'ram', 'hdd', 'os', 'monitor', 'mouse', 'keyboard', 'cpu_cabin']:
                old_item = getattr(old_system, field_name)
                new_item = getattr(system, field_name)

                if old_item is not None:
                    if old_item != new_item:
                        item_updates[old_item.pk] = item_updates.get(old_item.pk, 0) - 1
                        item_updates[new_item.pk] = item_updates.get(new_item.pk, 0) + 1
                        print(f"{system.sys_name} Updated : Changed item in {field_name} from {old_item} to {new_item}")
                else:
                    print(f"{system.sys_name} Updated : Added {new_item} to {field_name}")

        with transaction.atomic():
            for item_pk, update_count in item_updates.items():
                if item_pk:
                    item = Item.objects.get(pk=item_pk)
                    item.in_use_qty += update_count
                    item.total_available_qty -= update_count
                    item.save()
                    
        system.save()
        return super().form_valid(form)
    
    
    def get_object(self, queryset=None):
        sys_id = self.kwargs['sys_id']
        queryset = self.get_queryset()
        return queryset.get(pk=sys_id)
    
    def get_success_url(self):
        lab_pk = self.kwargs["lab_id"]
        dept_id = self.kwargs["dept_id"]
        org_id = self.kwargs["org_id"]
        return reverse('lab:system-list', kwargs={'org_id':org_id, 'dept_id':dept_id, 'lab_id': lab_pk})
    
class SystemDeleteView(LoginRequiredMixin, LabAccessMixin, View):
    model = System

    def get(self, request, *args, **kwargs):
        system = System.objects.get(pk = self.kwargs["sys_id"])
        system.delete()
        lab_pk = self.kwargs["lab_id"]
        dept_id = self.kwargs["dept_id"]
        org_id = self.kwargs["org_id"]
        return HttpResponsePermanentRedirect(reverse('lab:system-list', kwargs={'org_id':org_id, 'dept_id':dept_id, 'lab_id': lab_pk}))


class BrandListView(LoginRequiredMixin, LabAccessMixin, generic.ListView):
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


class BrandCreateView(LoginRequiredMixin, LabAccessMixin, generic.FormView):
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
    

class BrandDeleteView(LoginRequiredMixin, LabAccessMixin, View):
    model = Brand

    def get(self, request, *args, **kwargs):
        category = Brand.objects.get(pk = self.kwargs["brand"])
        category.delete()
        lab_pk = self.kwargs["lab_id"]
        org_id = self.kwargs["org_id"]
        dept_id = self.kwargs["dept_id"]
        return HttpResponsePermanentRedirect(reverse('lab:brand-list', kwargs={'lab_id': lab_pk, 'org_id':org_id, 'dept_id':dept_id}))
    
    
class LabSettingsView(LoginRequiredMixin, LabAccessMixin, generic.CreateView, generic.UpdateView):
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
    
    def get_object(self, queryset=None):
        try:
            lab = Lab.objects.get(pk=self.kwargs['lab_id']) 
            lab_settings = LabSettings.objects.get(lab=lab)
            queryset = self.get_queryset()
            return queryset.get(pk=lab_settings.pk)
        except (Lab.DoesNotExist, LabSettings.DoesNotExist):
            lab = Lab.objects.get(pk=self.kwargs['lab_id'])
            lab_settings = LabSettings.objects.create(lab=lab)
            return lab_settings

    def form_valid(self, form):
        form.save()
        return self.render_to_response(self.get_context_data(form=form))  
    
        
    