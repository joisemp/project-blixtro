from django.db import models
from django.forms import ValidationError
from .utils import generate_unique_code
from apps.core.models import UserProfile
from apps.org.models import Org, Department


class Lab(models.Model):
    user = models.ManyToManyField(UserProfile, related_name='labs')
    org = models.ForeignKey(Org, on_delete=models.CASCADE)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    lab_name = models.CharField(max_length=255)
    room_no = models.IntegerField(unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{str(self.lab_name)} | {str(self.room_no)}"
    

class LabSettings(models.Model):
    lab = models.OneToOneField(Lab, on_delete=models.CASCADE, related_name="settings")
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
    unique_code = models.CharField(max_length=5, unique=True)
    item_name = models.CharField(max_length=255)
    total_qty = models.IntegerField(default=1)
    in_use_qty = models.IntegerField(default=0)
    total_available_qty = models.IntegerField(default=0)
    removed_qty = models.IntegerField(default=0)
    unit_of_measure = models.CharField(max_length=255, blank=True, null=True)
    is_listed = models.BooleanField(default=True)
    lab = models.ForeignKey(Lab, blank=False, null=False, on_delete=models.CASCADE)
    org = models.ForeignKey(Org, blank=False, null=True, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, blank=True, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code = generate_unique_code(Item)
        if not self.org and self.lab:
            self.org = self.lab.org
        super().save(*args, **kwargs)
    
    def __str__(self):
        return str(self.item_name)
    

class ItemAdditionalInfo(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    serial_no = models.CharField(max_length=255)
    price = models.DecimalField(decimal_places=4, max_digits=10, null=True, blank=True)


    def save(self, *args, **kwargs):
        if self.item:
            current_count = ItemAdditionalInfo.objects.filter(item=self.item).count()
            if current_count >= self.item.total_qty:
                raise ValidationError(
                    f"You cannot add more than {self.item.total_qty} additional info records for this item."
                )
        super().save(*args, **kwargs)

    
class System(models.Model):
    unique_code = models.CharField(max_length=5, unique=True)
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    sys_name = models.CharField(max_length=255, verbose_name="System Name")

    # System status with a custom manager for filtering/reporting
    STATUS_CHOICES = [
        ("working", "Working"),
        ("not_working", "Not working"),
        ("item_missing", "Item missing"),
    ]
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, blank=False, null=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)


class SystemComponent(models.Model):
    system = models.ForeignKey(System, null=True, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    serial_no = models.CharField(max_length=255)
    COMPONENT_TYPES = [
        ("Mouse", "Mouse"),
        ("Keyboard", "Keyboard"),
        ("Processor", "Processor"),
        ("RAM", "RAM"),
        ("Storage", "Storage"),
        ("OS", "OS"),
        ("Monitor", "Monitor"),
        ("CPU Cabin", "CPU Cabin"),
    ]
    component_type = models.CharField(max_length=255, choices=COMPONENT_TYPES)


class Archive(models.Model):
    REASON_CHOICES = [
        ("Depreciation", "Depreciation"),
        ("Consumption", "Consumption"),
    ]
    lab = models.ForeignKey(Lab, null=False, blank=False, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, null=False, blank=False, on_delete=models.CASCADE)
    reason = models.CharField(max_length=255, choices=REASON_CHOICES)
    qty = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    remarks = models.TextField(null=False, blank=False)
    
    def __str__(self):
        return f"{self.item.item_name} - {self.qty}"

