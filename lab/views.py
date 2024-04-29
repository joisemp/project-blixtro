from django.http import HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import generic, View
from . models import Item, Lab, Group, Category, GroupItem
from .forms import LabCreateForm, GroupItemCreateForm
from . mixins import StaffAccessCheckMixin, AdminOnlyAccessMixin
from django.contrib.auth.mixins import LoginRequiredMixin


class LabListView(LoginRequiredMixin, generic.ListView):
    template_name = "lab/labs-list.html"
    model = Lab
    ordering = ['-id']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            if self.request.user.is_staff and not self.request.user.is_superuser and not self.request.user.is_admin:
                labs = Lab.objects.all()
                lab_list = []
                for lab in labs:
                    if self.request.user in lab.user.all():
                        lab_list.append(lab)
                context["labs"] = lab_list
            else:
                context["labs"] = Lab.objects.all()
        return context
    

class LabCreateView(LoginRequiredMixin, AdminOnlyAccessMixin, generic.CreateView):
    model = Lab
    form_class = LabCreateForm
    template_name = "lab/lab-create.html"
    
    def get_success_url(self):
        lab = self.object
        return reverse('lab:item-list', kwargs={'pk': lab.pk})
    
    def form_valid(self, form):
        selected_users = form.cleaned_data['users']
        lab = form.save(commit=False)
        lab.save()
        lab.user.set(selected_users)
        return super().form_valid(form)
    

class UpdateLabView(LoginRequiredMixin, AdminOnlyAccessMixin, generic.UpdateView):
    template_name = 'lab/lab-update.html'
    model = Lab
    form_class = LabCreateForm
    
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
        return reverse('lab:lab-detail', kwargs={'pk': lab.pk})
    
    
class DeleteLabView(LoginRequiredMixin, AdminOnlyAccessMixin, generic.DeleteView):
    model = Lab
    template_name = "lab/lab-delete.html"
    
    def get_success_url(self):
        return reverse('lab:lab-list')


class GroupCreateView(LoginRequiredMixin, StaffAccessCheckMixin, generic.CreateView):
    template_name = 'lab/create-group.html'
    model = Group
    fields = ["title"]
    
    def form_valid(self, form):
        item_group = form.save(commit=False)
        labid = self.kwargs["pk"]
        lab = Lab.objects.get(pk=labid)
        item_group.lab = lab
        item_group.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        lab_pk = self.kwargs["pk"]
        return reverse('lab:group-list', kwargs={'pk': lab_pk})
    

class GroupListView(LoginRequiredMixin, StaffAccessCheckMixin, generic.ListView):
    template_name = "lab/group-list.html"
    model = Group
    ordering = ['-id']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lab = get_object_or_404(Lab, pk=self.kwargs['pk'])
        groups = Group.objects.filter(lab=lab)
        context["groups"] = groups
        context["lab"] = lab
        return context


class GroupDetailView(LoginRequiredMixin, StaffAccessCheckMixin, generic.TemplateView):
    template_name = "lab/group-detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group = get_object_or_404(Group, pk=self.kwargs['group'])
        lab = get_object_or_404(Lab, pk=self.kwargs['pk'])
        group_items = GroupItem.objects.filter(group = group)
        context['group'] = group
        context['lab'] = lab
        context['group_items'] = group_items
        return context


class GroupDeleteView(LoginRequiredMixin, StaffAccessCheckMixin, View):
    model = Group

    def get(self, request, *args, **kwargs):
        group_id = self.kwargs["group"]
        group = get_object_or_404(self.model, pk=group_id)
        group.delete()
        return redirect(reverse('lab:group-list', kwargs={'pk': self.kwargs["pk"]}))
    

class GroupUpdateView(generic.UpdateView):
    ...
  
    
class CreateItemView(LoginRequiredMixin, StaffAccessCheckMixin, generic.CreateView):
    template_name = 'lab/add-item.html'
    model = Item    
    fields = ["item_name", "total_qty", "unit_of_measure", "category"]
    
    def form_valid(self, form):
        item = form.save(commit=False)
        labid = self.kwargs["pk"]
        lab = Lab.objects.get(pk=labid)
        item.lab = lab
        item.save()
        return super().form_valid(form)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        lab = get_object_or_404(Lab, pk=self.kwargs['pk'])
        form.fields['category'].queryset = Category.objects.filter(lab=lab)
        return form

    def get_success_url(self):
        lab_pk = self.kwargs["pk"]
        return reverse('lab:item-list', kwargs={'pk': lab_pk})
    
    
class ItemListView(LoginRequiredMixin, StaffAccessCheckMixin, generic.ListView):
    template_name = "lab/item-list.html"
    model = Item
    ordering = ['-id']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lab = get_object_or_404(Lab, pk=self.kwargs['pk'])
        items = Item.objects.filter(lab=lab)
        context["items"] = items
        context["lab"] = lab
        return context    

    
    
class ItemUpdateView(LoginRequiredMixin, StaffAccessCheckMixin, generic.UpdateView):
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
        lab_pk = self.kwargs["pk"]
        return reverse('lab:item-list', kwargs={'pk': lab_pk})
    

class ItemDeleteView(LoginRequiredMixin, StaffAccessCheckMixin, View):
    model = Item

    def get(self, request, *args, **kwargs):
        item_id = self.kwargs["item_id"]
        lab_pk = self.kwargs["pk"]
        item = get_object_or_404(self.model, pk=item_id)
        item.delete()
        return redirect(reverse('lab:item-list', kwargs={'pk': lab_pk}))


class GroupItemCreateView(generic.CreateView):
    template_name = 'lab/add-group-item.html'
    model = GroupItem    
    form_class = GroupItemCreateForm
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        lab = get_object_or_404(Lab, pk=self.kwargs['pk'])
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
        lab_pk = self.kwargs["pk"]
        group_id = self.kwargs["group"]
        return reverse('lab:group-detail', kwargs={'pk': lab_pk, 'group':group_id})


class GroupItemDeleteView(LoginRequiredMixin, View):
    model = GroupItem

    def get(self, request, *args, **kwargs):
        group_item = GroupItem.objects.get(pk = self.kwargs["group_item"])
        group_item.delete()
        lab_pk = self.kwargs["pk"]
        group_id = self.kwargs["group"]
        return HttpResponsePermanentRedirect(reverse('lab:group-detail', kwargs={'pk': lab_pk, 'group':group_id}))
    
    