from django.db import models
from core.models import User


class Lab(models.Model):
    user = models.ManyToManyField(User)
    lab_name = models.CharField(max_length=255)
    room_no = models.IntegerField(unique=True)
    
    def __str__(self):
        return f"{str(self.lab_name)} | {str(self.room_no)}"
    

class Category(models.Model):
    category_name = models.CharField(max_length=255)
    lab = models.ForeignKey(Lab, blank=False, null=False, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.category_name)
    

class Group(models.Model):
    title = models.CharField(max_length=255)
    date_created = models.DateField(auto_now_add=True)
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.title)


class Item(models.Model):
    item_name = models.CharField(max_length=255)
    total_qty = models.IntegerField(default=1)
    unit_of_measure = models.CharField(max_length=255, blank=True, null=True)
    lab = models.ForeignKey(Lab, blank=False, null=False, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return str(self.item_name)


class GroupItem(models.Model):
    item = models.ForeignKey(Item, blank=False, null=False, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, blank=False, null=False, on_delete=models.CASCADE)
    qty = models.IntegerField()
    
    def __str__(self):
        return f"{str(self.item)} | {str(self.qty)}"
    
    