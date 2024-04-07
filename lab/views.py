from django.shortcuts import render
from django.views import generic
from . models import Item, Lab
from . utils import get_total_item_qty


class LabListView(generic.ListView):
    template_name = "lab/labs-list.html"
    queryset = Lab.objects.all()
    context_object_name = 'labs'
    ordering = ['-id']
    
