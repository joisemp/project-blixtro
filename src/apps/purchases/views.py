from django.http import HttpResponseRedirect
from django.http.response import HttpResponse as HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from apps.org.models import Department
from apps.lab.models import Lab, Item
from apps.purchases.models import Purchase, Vendor
from . forms import PurchaseCreateForm, PurchaseUpdateForm, VendorCreateFrom
from django.db import transaction


class PurchaseListView(generic.ListView):
    template_name = 'purchases/purchase-list.html'
    model = Purchase
    context_object_name = 'purchases'
    
    def get_queryset(self):
        self.lab_id = self.kwargs["lab_id"]
        return Purchase.objects.filter(lab_id = self.lab_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lab"] = get_object_or_404(Lab, pk=self.lab_id)
        return context
    

class PurchaseCreateView(generic.CreateView):
    model = Purchase
    template_name = "purchases/create-purchase.html"
    form_class = PurchaseCreateForm
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class or self.get_form_class())
        self.lab = get_object_or_404(Lab, pk=self.kwargs["lab_id"])
        form.fields['item'].queryset = Item.objects.filter(lab_id=self.lab.pk, is_listed=True)
        return form
    
    def form_valid(self, form):
        org = self.request.user.profile.org
        new_item = self.request.GET.get('new_item')
        dept = get_object_or_404(Department, pk=self.kwargs["dept_id"])
        with transaction.atomic():
            purchase = form.save(commit=False)
            purchase.org = org
            purchase.dept = dept
            purchase.lab = self.lab
            purchase.requested = True
            
            if new_item:
                new_item_name = form.cleaned_data.get('new_item')
                new_item_obj = Item.objects.create(item_name = new_item_name, is_listed=False, lab = self.lab)
                purchase.item = new_item_obj
            
            purchase.save()
        
        return super().form_valid(form)
    
    def get_success_url(self):
        lab_id = self.kwargs['lab_id']
        org_id = self.kwargs['org_id']
        dept_id = self.kwargs['dept_id']
        return reverse('org:lab:purchases:purchase-list', kwargs={'org_id':org_id, 'lab_id': lab_id, 'dept_id':dept_id})


class PurchaseDetailView(generic.DetailView):
    model = Purchase
    template_name = "purchases/purchase-detail.html"
    context_object_name = 'purchase'
    
    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        return queryset.get(pk=self.kwargs['purchase_id'])
    
 
class PurchaseUpdateView(generic.UpdateView):
    template_name = "purchases/purchase-update.html"
    model = Purchase
    form_class = PurchaseUpdateForm
    
    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        return queryset.get(pk=self.kwargs["purchase_id"]) 

    def get_success_url(self):
        lab_id = self.kwargs['lab_id']
        org_id = self.kwargs['org_id']
        dept_id = self.kwargs['dept_id']
        return reverse('org:lab:purchases:purchase-detail', kwargs={'org_id':org_id, 'lab_id': lab_id, 'dept_id':dept_id, 'purchase_id':self.object.pk})
    

class PurchaseDeleteView(generic.View):
    model = Purchase
    
    def get(self, request, *args, **kwargs):
        purchase_item = get_object_or_404(Purchase, pk = self.kwargs["purchase_id"])
        if purchase_item.item.is_listed:
            purchase_item.delete()
        else:
            purchase_item.item.delete()
        return HttpResponsePermanentRedirect(reverse('org:lab:purchases:purchase-list', kwargs={
            'org_id':self.kwargs["org_id"], 
            'dept_id':self.kwargs["dept_id"], 
            'lab_id':self.kwargs["lab_id"]
            }))


class PurchaseCompleteView(generic.View):
    def get(self, request, *args, **kwargs):
        purchase = get_object_or_404(Purchase, pk=self.kwargs["purchase_id"])
        
        try:
            with transaction.atomic():
                purchase.completed = True
                purchase.save()
        except Exception as e:
            return HttpResponse("An error occurred while completing the purchase.", status=500)

        org_id = request.user.profile.org.pk
        return HttpResponseRedirect(
            reverse(
                'org:lab:purchases:purchase-detail', 
                kwargs={
                    'org_id': org_id,
                    'dept_id':purchase.lab.dept.pk,
                    'lab_id': purchase.lab.pk,
                    'purchase_id': purchase.pk
                }
            )
        )
        
        
class PurchaseAddToStockView(generic.View):
    def get(self, request, *args, **kwargs):
        purchase = get_object_or_404(Purchase, pk=self.kwargs["purchase_id"])
        
        try:
            with transaction.atomic():
                purchase.added_to_stock = True
                item = purchase.item
                if not item.is_listed:
                    item.is_listed = True
                    item.total_qty = purchase.qty
                else:
                    item.total_qty += purchase.qty
                item.save()
                purchase.save()
        except Exception as e:
            return HttpResponse("An error occurred while completing the purchase.", status=500)

        org_id = request.user.profile.org.pk
        return HttpResponseRedirect(
            reverse(
                'org:lab:purchases:purchase-detail', 
                kwargs={
                    'org_id': org_id,
                    'dept_id':purchase.lab.dept.pk,
                    'lab_id': purchase.lab.pk,
                    'purchase_id': purchase.pk
                }
            )
        )        


class VendorCreateView(generic.CreateView):
    model = Vendor   
    template_name = 'purchases/add-vendor.html'
    form_class = VendorCreateFrom   
    
    def form_valid(self, form):
        org = self.request.user.profile.org
        vendor_details = form.save(commit=False)
        vendor_details.org = org
        vendor_details.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        org_id = self.request.user.profile.org.pk
        return reverse('org:vendors-list', kwargs={'org_id':org_id})
    

class VendorDeleteView(generic.View):
    model = Vendor
    
    def get(self, request, *args, **kwargs):
        vendor = get_object_or_404(Vendor, pk = self.kwargs["vendor_id"])
        vendor.delete()
        org_id = self.request.user.profile.org.pk
        return HttpResponsePermanentRedirect(reverse('org:vendors-list', kwargs={'org_id':org_id}))