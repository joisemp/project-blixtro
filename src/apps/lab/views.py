from django.http import HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import generic, View
from . models import Item, Lab, Category, SystemComponent, System, Brand, LabSettings, Archive, ItemAdditionalInfo
from apps.core.models import Department
from .forms import LabCreateForm, BrandCreateForm, LabSettingsForm, AddSystemComponetForm, ArchiveForm, SystemCreateForm, SystemUpdateForm, ItemCreateFrom, AdditionalItemInfoForm
from apps.org.models import Org
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from apps.core.models import UserProfile
from .utils import generate_unique_code
from django.db.models import Q



class LabListView(LoginRequiredMixin, generic.ListView):
    template_name = "lab/labs-list.html"
    model = Lab
    ordering = ['-id']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        org = get_object_or_404(Org, pk=self.kwargs["org_id"])
        dept = get_object_or_404(Department, pk=self.kwargs["dept_id"])
        context["org"] = org
        context["dept"] = dept
        userprofile = get_object_or_404(UserProfile, user = self.request.user)
        context["userprofile"] = userprofile
        if userprofile.is_lab_staff:
            context["labs"] = userprofile.labs.all()
        else:
            context["labs"] = Lab.objects.filter(org = org, dept = dept)
        return context
    
    
class LabCreateView(LoginRequiredMixin, generic.CreateView):
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
        return reverse('org:lab:lab-settings', kwargs={'org_id':org_id, 'lab_id': lab.pk, 'dept_id':dept_id})
    
    def form_valid(self, form):
        selected_users = form.cleaned_data['users']
        org_id = self.kwargs["org_id"]
        dept_id = self.kwargs["dept_id"]
        org = get_object_or_404(Org, pk=org_id)
        dept = get_object_or_404(Department, pk=dept_id)
        lab = form.save(commit=False)
        lab.org = org
        lab.dept = dept
        lab.save()
        lab.user.set(selected_users)
        return super().form_valid(form)
    

class UpdateLabView(LoginRequiredMixin, generic.UpdateView):
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
        return reverse('org:lab:lab-list', kwargs={'org_id':org_id, 'dept_id':dept_id})
    
class DeleteLabView(LoginRequiredMixin, View):
    model = Lab

    def get(self, request, *args, **kwargs):
        lab_pk = self.kwargs["lab_id"]
        lab = get_object_or_404(Lab, pk=lab_pk)
        lab.delete()
        org_id = self.kwargs["org_id"]
        dept_id = self.kwargs["dept_id"]
        return HttpResponsePermanentRedirect(reverse('org:lab:lab-list', kwargs={'org_id':org_id, 'dept_id':dept_id}))
  
    
class CreateItemView(LoginRequiredMixin, generic.CreateView):
    template_name = 'lab/add-item.html'
    model = Item    
    form_class = ItemCreateFrom
    
    def form_valid(self, form):
        item = form.save(commit=False)
        item.total_available_qty = item.total_qty
        labid = self.kwargs["lab_id"]
        lab = get_object_or_404(Lab, pk=labid)
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
        lab_id = self.kwargs["lab_id"]
        org_id = self.kwargs["org_id"]
        dept_id = self.kwargs["dept_id"]
        return reverse('org:lab:item-list', kwargs={'org_id':org_id, 'lab_id': lab_id, 'dept_id':dept_id})
    
    
class ItemListView(LoginRequiredMixin, generic.ListView):
    template_name = "lab/item-list.html"
    model = Item
    context_object_name = 'items'

    def get_queryset(self):
        lab = get_object_or_404(Lab, pk=self.kwargs['lab_id'])
        search_term = self.request.GET.get('search', '')
        queryset = Item.objects.filter(lab=lab, is_listed=True).order_by('-id')
        # If a search term is provided, filter by the relevant fields (unique_code, item_name, etc.)
        if search_term:
            queryset = queryset.filter(
                Q(unique_code__icontains=search_term) |  # Match by unique code
                Q(item_name__icontains=search_term) |    # Match by item name
                Q(category__category_name__icontains=search_term)  # Example: match by category name (if category has a 'name' field)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lab = get_object_or_404(Lab, pk=self.kwargs['lab_id'])
        context["org"] = get_object_or_404(Org, pk=self.kwargs["org_id"])
        context["dept"] = get_object_or_404(Department, pk=self.kwargs["dept_id"])
        systems = System.objects.filter(lab=lab)
        context["systems"] = systems
        context["lab"] = lab
        try:
            context["lab_settings"] = get_object_or_404(LabSettings, lab=lab)
        except LabSettings.DoesNotExist:
            pass
        context['search_term'] = self.request.GET.get('search', '')
        return context

class ItemDetailView(generic.DetailView):
    model = Item
    template_name = 'lab/item-detail.html'  
    
    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        return queryset.get(pk=self.kwargs['item_id'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = get_object_or_404(Item, pk = self.kwargs['item_id'])
        context["additional_info"] = ItemAdditionalInfo.objects.filter(item=item)
        context["add_additional_form"] = AdditionalItemInfoForm
        return context

    
class ItemUpdateView(LoginRequiredMixin, generic.UpdateView):
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
        return reverse('org:lab:item-list', kwargs={'lab_id': lab_pk, 'org_id':org_id, 'dept_id':dept_id})
    

class ItemDeleteView(LoginRequiredMixin, View):
    model = Item

    def get(self, request, *args, **kwargs):
        item_id = self.kwargs["item_id"]
        lab_pk = self.kwargs["lab_id"]
        org_id = self.kwargs["org_id"]
        dept_id = self.kwargs["dept_id"]
        item = get_object_or_404(self.model, pk=item_id)
        item.delete()
        return HttpResponsePermanentRedirect(reverse('org:lab:item-list', kwargs={'lab_id': lab_pk, 'org_id':org_id, 'dept_id':dept_id}))


class AddItemAdditionalInfoView(generic.CreateView):
    template_name = 'lab/create-item-add-info.html'   
    model = ItemAdditionalInfo
    form_class = AdditionalItemInfoForm
    
    def form_valid(self, form):
        item = get_object_or_404(Item, pk=self.kwargs["item_id"])
        add_info = form.save(commit=False)
        add_info.item = item
        
        # Your custom validation logic
        if ItemAdditionalInfo.objects.filter(item=item).count() >= item.total_qty:
            form.add_error(None, f"You cannot add more than {item.total_qty} additional info records for this item.")
            return self.form_invalid(form)
        
        add_info.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('org:lab:item-detail', kwargs={
            'lab_id': self.kwargs['lab_id'],
            'org_id': self.kwargs['org_id'],
            'dept_id': self.kwargs['dept_id'],
            'item_id': self.kwargs['item_id']
        })
    
    
class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = "lab/category-list.html"
    model = Category
    ordering = ['-id']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lab = get_object_or_404(Lab, pk=self.kwargs['lab_id'])
        categories = Category.objects.filter(lab=lab)
        context["categories"] = categories
        context["org"] = get_object_or_404(Org, pk=self.kwargs["org_id"])
        context["dept"] = get_object_or_404(Department, pk=self.kwargs["dept_id"])
        context["lab"] = lab
        try:
            context["lab_settings"] = get_object_or_404(LabSettings, lab=lab)
        except LabSettings.DoesNotExist:
            pass
        return context 
    
class CategoryCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'lab/create-category.html'
    model = Category    
    fields = ["category_name"]
    
    def form_valid(self, form):
        category = form.save(commit=False)
        lab = get_object_or_404(Lab, pk=self.kwargs["lab_id"])
        category.lab = lab
        category.save()
        return super().form_valid(form)

    def get_success_url(self):
        lab_pk = self.kwargs["lab_id"]
        org_id = self.kwargs["org_id"]
        dept_id = self.kwargs["dept_id"]
        return reverse('org:lab:category-list', kwargs={'lab_id': lab_pk, 'org_id':org_id, 'dept_id':dept_id})
    

class CategoryDeleteView(LoginRequiredMixin, View):
    model = Category

    def get(self, request, *args, **kwargs):
        category = get_object_or_404(Category, pk = self.kwargs["category"])
        category.delete()
        lab_pk = self.kwargs["lab_id"]
        org_id = self.kwargs["org_id"]
        dept_id = self.kwargs["dept_id"]
        return HttpResponsePermanentRedirect(reverse('org:lab:category-list', kwargs={'lab_id': lab_pk, 'org_id':org_id, 'dept_id':dept_id}))
    

class SystemCreateView(LoginRequiredMixin, generic.CreateView):
    model = System    
    form_class = SystemCreateForm
    template_name = "lab/system-create.html"
    
    def form_valid(self, form):
        system = form.save(commit=False)
        labid = self.kwargs["lab_id"]
        lab = get_object_or_404(Lab, pk=labid)
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
        return reverse('org:lab:system-list', kwargs={'org_id':org_id, 'dept_id':dept_id, 'lab_id': lab_pk})
    

class SystemListView(LoginRequiredMixin, generic.ListView):
    template_name = "lab/system-list.html"
    model = Item
    ordering = ['-id']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lab = get_object_or_404(Lab, pk=self.kwargs['lab_id'])
        systems = System.objects.filter(lab=lab)
        context["org"] = get_object_or_404(Org, pk=self.kwargs["org_id"])
        context["dept"] = get_object_or_404(Department, pk=self.kwargs["dept_id"])
        context["systems"] = systems
        context["lab"] = lab
        context["lab_settings"] = get_object_or_404(LabSettings, lab=lab)
        return context 

class SystemDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'lab/system-detail.html'
    model = System
    
    def get_object(self, queryset=None):
        sys_id = self.kwargs['sys_id']
        queryset = self.get_queryset()
        return queryset.get(pk=sys_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        system = get_object_or_404(System, pk = self.kwargs["sys_id"])
        lab = get_object_or_404(Lab, pk=self.kwargs["lab_id"])
        
        form = AddSystemComponetForm()
        form.fields['category'].queryset = Category.objects.filter(lab=lab)
        form.fields['item'].queryset = Item.objects.filter(lab=lab)
        context["form"] = form
        
        context["components"] = SystemComponent.objects.filter(system = system)
        context["org_id"] = self.kwargs["org_id"]
        context["dept_id"] = self.kwargs["dept_id"]
        context["lab_id"] = self.kwargs["lab_id"]
        context["sys_id"] = self.kwargs["sys_id"]
        return context


class SystemComponentCreateView(LoginRequiredMixin, generic.FormView):
    model = SystemComponent
    form_class = AddSystemComponetForm
    
    def form_valid(self, form):
        system = get_object_or_404(System, pk = self.kwargs["sys_id"])
        item = form.cleaned_data.get('item')
        component_type = form.cleaned_data.get('component_type')
        serial_no = form.cleaned_data.get('serial_no')
        with transaction.atomic():
            sys_component = SystemComponent.objects.create(system=system, item=item, component_type=component_type, serial_no=serial_no)
            item = sys_component.item
            item.in_use_qty += 1
            item.total_available_qty -= 1
            item.save()
        return super().form_valid(form)
        
    def get_success_url(self):
        org_id = self.kwargs["org_id"]
        dept_id = self.kwargs["dept_id"]
        lab_id = self.kwargs["lab_id"]
        sys_id = self.kwargs["sys_id"]
        return reverse('org:lab:system-detail', kwargs={'org_id':org_id, 'dept_id':dept_id, 'lab_id':lab_id, 'sys_id':sys_id})
    

class SystemComponentDeleteView(LoginRequiredMixin, View):
    model = SystemComponent

    def get(self, request, *args, **kwargs):
        component = get_object_or_404(SystemComponent, pk = self.kwargs["component_id"])
        component.delete()
        lab_pk = self.kwargs["lab_id"]
        org_id = self.kwargs["org_id"]
        dept_id = self.kwargs["dept_id"]
        sys_id = self.kwargs["sys_id"]
        return HttpResponsePermanentRedirect(reverse('org:lab:system-detail', kwargs={'lab_id': lab_pk, 'org_id':org_id, 'dept_id':dept_id, 'sys_id':sys_id}))

        
class LoadItemsView(generic.ListView):
  model = Item
  template_name = "lab/additionals/item-options.html"
  context_object_name = "items"

  def get_queryset(self):
    category_id = self.request.GET.get("category")
    labid = self.kwargs["lab_id"]
    lab = get_object_or_404(Lab, pk = labid)
    if category_id:
      return self.model.objects.filter(category_id = category_id, lab=lab)
  
    return self.model.objects.filter(lab = lab)
    

class SystemUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = System    
    form_class = SystemUpdateForm
    template_name = "lab/system-update.html"
    
    
    # def form_valid(self, form):
    #     system = form.save(commit=False)
    #     old_system = get_object_or_404(System, pk=system.pk)

    #     item_updates = {}
    #     for field_name in self.fields:
    #         if field_name in ['processor', 'ram', 'hdd', 'os', 'monitor', 'mouse', 'keyboard', 'cpu_cabin']:
    #             old_item = getattr(old_system, field_name)
    #             new_item = getattr(system, field_name)

    #             if old_item is not None:
    #                 if old_item != new_item:
    #                     item_updates[old_item.pk] = item_updates.get(old_item.pk, 0) - 1
    #                     item_updates[new_item.pk] = item_updates.get(new_item.pk, 0) + 1
    #                     print(f"{system.sys_name} Updated : Changed item in {field_name} from {old_item} to {new_item}")
    #             else:
    #                 print(f"{system.sys_name} Updated : Added {new_item} to {field_name}")

    #     with transaction.atomic():
    #         for item_pk, update_count in item_updates.items():
    #             if item_pk:
    #                 item = get_object_or_404(Item, pk=item_pk)
    #                 item.in_use_qty += update_count
    #                 item.total_available_qty -= update_count
    #                 item.save()
                    
    #     system.save()
    #     return super().form_valid(form)
    
    
    def get_object(self, queryset=None):
        sys_id = self.kwargs['sys_id']
        queryset = self.get_queryset()
        return queryset.get(pk=sys_id)
    
    def get_success_url(self):
        lab_pk = self.kwargs["lab_id"]
        dept_id = self.kwargs["dept_id"]
        org_id = self.kwargs["org_id"]
        return reverse('org:lab:system-list', kwargs={'org_id':org_id, 'dept_id':dept_id, 'lab_id': lab_pk})
    
class SystemDeleteView(LoginRequiredMixin, View):
    model = System

    def get(self, request, *args, **kwargs):
        system = get_object_or_404(System, pk = self.kwargs["sys_id"])
        system.delete()
        lab_pk = self.kwargs["lab_id"]
        dept_id = self.kwargs["dept_id"]
        org_id = self.kwargs["org_id"]
        return HttpResponsePermanentRedirect(reverse('org:lab:system-list', kwargs={'org_id':org_id, 'dept_id':dept_id, 'lab_id': lab_pk}))


class BrandListView(LoginRequiredMixin, generic.ListView):
    template_name = 'lab/brand-list.html'
    model = Brand
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lab = get_object_or_404(Lab, pk=self.kwargs["lab_id"])
        context["brands"] = Brand.objects.filter(lab = lab)
        context["org_id"] = self.kwargs["org_id"]
        context["dept_id"] = self.kwargs["dept_id"]
        context["lab_id"] = self.kwargs["lab_id"]
        context["lab"] = lab
        context["lab_settings"] = get_object_or_404(LabSettings, lab=lab)
        return context


class BrandCreateView(LoginRequiredMixin, generic.FormView):
    model = Brand
    form_class = BrandCreateForm
    
    def form_valid(self, form):
        brand_name = form.cleaned_data.get('brand_name')
        lab = get_object_or_404(Lab, pk=self.kwargs["lab_id"])
        
        Brand.objects.create(
            brand_name = brand_name,
            lab = lab
        )
        
        return super().form_valid(form)
        
    def get_success_url(self):
        org_id = self.kwargs["org_id"]
        dept_id = self.kwargs["dept_id"]
        lab_id = self.kwargs["lab_id"]
        return reverse('org:lab:brand-list', kwargs={'org_id':org_id, 'dept_id':dept_id, 'lab_id':lab_id})
    

class BrandDeleteView(LoginRequiredMixin, View):
    model = Brand

    def get(self, request, *args, **kwargs):
        category = get_object_or_404(Brand, pk = self.kwargs["brand"])
        category.delete()
        lab_pk = self.kwargs["lab_id"]
        org_id = self.kwargs["org_id"]
        dept_id = self.kwargs["dept_id"]
        return HttpResponsePermanentRedirect(reverse('org:lab:brand-list', kwargs={'lab_id': lab_pk, 'org_id':org_id, 'dept_id':dept_id}))
    
    
class LabSettingsView(LoginRequiredMixin, generic.CreateView, generic.UpdateView):
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
        context["org"] = get_object_or_404(Org, pk=self.kwargs["org_id"])
        context["dept"] = get_object_or_404(Department, pk=self.kwargs["dept_id"])
        context["lab_settings"] = get_object_or_404(LabSettings, lab=lab)
        context['lab'] = get_object_or_404(Lab, pk=lab_id)
        return context
    
    def get_object(self, queryset=None):
        lab = get_object_or_404(Lab, pk=self.kwargs['lab_id']) 
        try:
            lab_settings = LabSettings.objects.get(lab=lab)
            queryset = self.get_queryset()
            return queryset.get(pk=lab_settings.pk)
        except (LabSettings.DoesNotExist):
            lab_settings = LabSettings.objects.create(lab=lab)
            return lab_settings

    def form_valid(self, form):
        form.save()
        return self.render_to_response(self.get_context_data(form=form))  
    
        
class ArchiveCreateView(LoginRequiredMixin, generic.CreateView):
    model = Archive
    template_name = 'lab/create-archive.html'
    form_class = ArchiveForm
    
    def get_initial(self):
        initial = super().get_initial()
        fields = ['serial_no', 'reason', 'qty']
        for field in fields:
            value = self.request.GET.get(field)
            if value is not None:
                initial[field] = value
        return initial
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        component_id = self.request.GET.get('componentid')
        if component_id:
            component = get_object_or_404(SystemComponent, pk=component_id)
            context["component"] = component
        context["item"] = get_object_or_404(Item, pk=self.kwargs["item_id"])
        return context
    
    def form_valid(self, form):
        with transaction.atomic():
            removed_item = form.save(commit=False)
            lab = get_object_or_404(Lab, pk=self.kwargs["lab_id"])
            item = get_object_or_404(Item, pk=self.kwargs["item_id"])
            removed_item.lab = lab
            removed_item.item = item
            
            qty = form.cleaned_data["qty"]
            
            component_id = self.request.GET.get('componentid')
            
            if component_id:
                if item.in_use_qty < qty:
                    form.add_error(None, "Not enough quantity in stock to remove.")
                    return self.form_invalid(form)
                item.in_use_qty -= qty
            else:
                if item.total_available_qty < qty:
                    form.add_error(None, "Not enough quantity in stock to remove.")
                    return self.form_invalid(form)
                item.total_available_qty -= qty
                
            item.removed_qty += qty
            item.save()
            removed_item.save()
            
            lab_pk = self.kwargs["lab_id"]
            org_id = self.kwargs["org_id"]
            dept_id = self.kwargs["dept_id"]
            
            if component_id:
                component = get_object_or_404(SystemComponent, pk=component_id)
                system = component.system
                component.delete()
                return HttpResponsePermanentRedirect(reverse('org:lab:system-detail', kwargs={
                    'org_id': org_id, 'lab_id': lab_pk, 'dept_id': dept_id, 'sys_id': system.pk
                }))
            
            return HttpResponsePermanentRedirect(reverse('org:lab:item-list', kwargs={
                'org_id': org_id, 'lab_id': lab_pk, 'dept_id': dept_id
            }))
        

class ArchiveListView(LoginRequiredMixin, generic.ListView):
    model = Archive
    template_name = 'lab/archive-list.html'
    context_object_name = 'archives'
    
    def get_queryset(self):
        self.lab_id = self.kwargs["lab_id"]
        return Archive.objects.filter(lab_id = self.lab_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lab"] = get_object_or_404(Lab, pk=self.lab_id)
        return context       
     