from django.db import models
from core.models import UserProfile, Org


class Lab(models.Model):
    user = models.ManyToManyField(UserProfile)
    org = models.ForeignKey(Org, on_delete=models.CASCADE)
    lab_name = models.CharField(max_length=255)
    room_no = models.IntegerField(unique=True)
    
    def __str__(self):
        return f"{str(self.lab_name)} | {str(self.room_no)}"
    

class Category(models.Model):
    category_name = models.CharField(max_length=255)
    lab = models.ForeignKey(Lab, blank=False, null=False, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.category_name)


class Item(models.Model):
    item_name = models.CharField(max_length=255)
    total_qty = models.IntegerField(default=1)
    unit_of_measure = models.CharField(max_length=255, blank=True, null=True)
    lab = models.ForeignKey(Lab, blank=False, null=False, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return str(self.item_name)
    
    