from typing import Any
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpRequest
from django.views import generic
from org.models import Org
from lab.models import Lab
from purchases.models import Purchase


class PurchaseListView(generic.ListView):
    template_name = 'purchases/purchase-list.html'
    model = Purchase
    context_object_name = 'purchases'
    
    def dispatch(self, request, *args, **kwargs):
        self.lab_id = self.kwargs["lab_id"]
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        return Purchase.objects.filter(lab_id = self.lab_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lab"] = get_object_or_404(Lab, pk=self.lab_id)
        return context
    
