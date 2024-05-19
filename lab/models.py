from django.db import models
from core.models import UserProfile, Org, Department


class Lab(models.Model):
    user = models.ManyToManyField(UserProfile)
    org = models.ForeignKey(Org, on_delete=models.CASCADE)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    lab_name = models.CharField(max_length=255)
    room_no = models.IntegerField(unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{str(self.lab_name)} | {str(self.room_no)}"
    

class LabSettings(models.Model):
    lab = models.OneToOneField(Lab, on_delete=models.CASCADE)
    items_tab = models.BooleanField(default=False)
    sys_tab = models.BooleanField(default=False)
    categories_tab = models.BooleanField(default=False)
    brands_tab = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.lab.lab_name} Settings"
    

class Category(models.Model):
    category_name = models.CharField(max_length=255)
    lab = models.ForeignKey(Lab, blank=False, null=False, on_delete=models.CASCADE)
    created_on = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return str(self.category_name)
    

class Brand(models.Model):
    brand_name = models.CharField(max_length=255)
    lab = models.ForeignKey(Lab, blank=True, null=True, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.brand_name)


class Item(models.Model):
    item_name = models.CharField(max_length=255)
    total_qty = models.IntegerField(default=1)
    in_use_qty = models.IntegerField(default=0)
    total_available_qty = models.IntegerField(default=0)
    unit_of_measure = models.CharField(max_length=255, blank=True, null=True)
    lab = models.ForeignKey(Lab, blank=False, null=False, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, blank=True, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.item_name)
    
    
class System(models.Model):
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    sys_name = models.CharField(max_length=255)
    processor = models.ForeignKey(Item, related_name='processor', on_delete=models.DO_NOTHING)
    ram = models.ForeignKey(Item, related_name='ram', on_delete=models.DO_NOTHING)
    hdd = models.ForeignKey(Item, related_name='hdd', on_delete=models.DO_NOTHING)
    os = models.ForeignKey(Item, related_name='os', on_delete=models.DO_NOTHING)
    monitor = models.ForeignKey(Item, related_name='monitor', on_delete=models.DO_NOTHING)
    mouse = models.ForeignKey(Item, related_name='mouse', on_delete=models.DO_NOTHING)
    keyboard = models.ForeignKey(Item, related_name='keyboard', on_delete=models.DO_NOTHING)
    cpu_cabin = models.ForeignKey(Item, related_name='cpu_cabin', on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    