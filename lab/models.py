from django.db import models
from core.models import User


class Lab(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING)
    lab_name = models.CharField(max_length=255)
    room_no = models.IntegerField(unique=True)
    
    def __str__(self):
        return f"{str(self.lab_name)} | {str(self.room_no)}"


class Label(models.Model):
    label_name = models.CharField(max_length=255)
    lab = models.ForeignKey(Lab, blank=False, null=False, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.label_name)
    

class Category(models.Model):
    category_name = models.CharField(max_length=255)
    lab = models.ForeignKey(Lab, blank=False, null=False, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.category_name)


class Item(models.Model):
    item_name = models.CharField(max_length=255)
    qty = models.IntegerField()
    unit_of_measure = models.CharField(max_length=255, blank=True, null=True)
    lab = models.ForeignKey(Lab, blank=False, null=False, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, blank=True, null=True, on_delete=models.DO_NOTHING)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return str(self.item_name)

