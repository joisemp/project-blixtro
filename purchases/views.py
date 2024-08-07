from django.http.response import HttpResponse as HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from org.models import Department
from lab.models import Lab, Item
from purchases.models import Purchase
from . forms import PurchaseCreateForm, PurchaseUpdateForm


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
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        self.lab = get_object_or_404(Lab, pk=self.kwargs["lab_id"])
        form.fields['item'].queryset = Item.objects.filter(lab_id=self.lab.pk)
        return form
    
    def form_valid(self, form):
        org = self.request.user.profile.org
        dept = get_object_or_404(Department, pk=self.kwargs["dept_id"])
        purchase = form.save(commit=False)
        purchase.org = org
        purchase.dept = dept
        purchase.lab = self.lab
        purchase.requested = True
        purchase.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        lab_id = self.kwargs['lab_id']
        org_id = self.kwargs['org_id']
        dept_id = self.kwargs['dept_id']
        return reverse('lab:purchases:purchase-list', kwargs={'org_id':org_id, 'lab_id': lab_id, 'dept_id':dept_id})


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
        return reverse('lab:purchases:purchase-detail', kwargs={'org_id':org_id, 'lab_id': lab_id, 'dept_id':dept_id, 'purchase_id':self.object.pk})
    

class PurchaseDeleteView(generic.View):
    model = Purchase
    
    def get(self, request, *args, **kwargs):
        purchase_item = get_object_or_404(Purchase, pk = self.kwargs["purchase_id"])
        purchase_item.delete()
        return HttpResponsePermanentRedirect(reverse('lab:purchases:purchase-list', kwargs={
            'org_id':self.kwargs["org_id"], 
            'dept_id':self.kwargs["dept_id"], 
            'lab_id':self.kwargs["lab_id"]
            }))
        