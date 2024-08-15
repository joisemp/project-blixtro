from django.db import models
from apps.lab.models import Item, Lab
from apps.org.models import Org, Department


class Vendor(models.Model):
    org = models.ForeignKey(Org, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.TextField()
    
    def __str__(self):
        return f"{self.name}"
    

class Purchase(models.Model):
    org = models.ForeignKey(Org, on_delete=models.CASCADE)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE, blank=True, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
    qty = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    created_on = models.DateTimeField(auto_now_add=True)
    requested = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    added_to_stock = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.item} | {self.org} | {self.lab}"
    
    