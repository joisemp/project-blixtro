from django.db import models
from core.models import Organisation, UserProfile, Department
from django.utils.text import slugify
from config.utils import generate_unique_slug, generate_unique_code


class Rooms(models.Model):
    organisation = models.ForeignKey(Organisation,on_delete=models.CASCADE)
    department = models.ForeignKey(Department,on_delete=models.CASCADE)
    label = models.CharField(max_length=20)
    room_name = models.CharField(max_length=255)
    incharge = models.OneToOneField(UserProfile,on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, max_length=255)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.room_name)
            self.slug = generate_unique_slug(self, base_slug)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.room_name


class Activity(models.Model):
    organisation = models.ForeignKey(Organisation,on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, max_length=255)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.action)
            self.slug = generate_unique_slug(self, base_slug)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.action


class Vendors(models.Model):
    organisation = models.ForeignKey(Organisation,on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)
    alternate_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    vendor_id = models.CharField(max_length=8,unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, max_length=255)
    
    def save(self, *args, **kwargs):
        if not self.vendor_id:
            self.vendor_id = generate_unique_code(self, 8, 'vendor_id')
        if not self.slug:
            base_slug = slugify(self.vendor_name)
            self.slug = generate_unique_slug(self, base_slug)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.vendor_name


class Purchase(models.Model):
    UNIT_CHOICES = [
        ('kilogram','Kilogram'),
        ('liters','Liters'),
        ('units','Units'),
    ]
    STATUS_CHOICES = [
        ('requested','Requested'),
        ('approved','Approved'),
        ('rejected','Rejected'),
        ('completed','Completed'),
    ]
    organisation = models.ForeignKey(Organisation,on_delete=models.CASCADE)
    room = models.ForeignKey(Rooms,on_delete=models.CASCADE)
    purchase_id = models.CharField(max_length=8,unique=True)
    item_name = models.CharField(max_length=255)
    item = models.ForeignKey('inventory.Item', on_delete=models.CASCADE)
    quantity = models.FloatField()
    unit_of_measure = models.CharField(max_length=10,choices=UNIT_CHOICES)
    vendor = models.ForeignKey(Vendors,on_delete=models.CASCADE)
    brand = models.ForeignKey('inventory.Brand',on_delete=models.CASCADE)
    category = models.ForeignKey('inventory.Category',on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES)
    updated_on = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, max_length=255)
    
    def save(self, *args, **kwargs):
        if not self.purchase_id:
            self.purchase_id = generate_unique_code(self, 8, 'purchase_id')
        if not self.slug:
            base_slug = slugify(self.purchase_id)
            self.slug = generate_unique_slug(self, base_slug)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.purchase_id} {self.room}"
    

class Issues(models.Model):
    organisation = models.ForeignKey(Organisation,on_delete=models.CASCADE)
    room = models.ForeignKey(Rooms,on_delete=models.CASCADE)
    created_by = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    description = models.TextField()
    resolved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, max_length=255)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.subject)
            self.slug = generate_unique_slug(self, base_slug)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.subject


class Category(models.Model):
    organisation = models.ForeignKey(Organisation,on_delete=models.CASCADE)
    room = models.ForeignKey(Rooms,on_delete=models.CASCADE)
    category_name = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, max_length=255)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.category_name)
            self.slug = generate_unique_slug(self, base_slug)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.category_name


class Brand(models.Model):
    organisation = models.ForeignKey(Organisation,on_delete=models.CASCADE)
    room = models.ForeignKey(Rooms,on_delete=models.CASCADE)
    brand_name = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, max_length=255)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.brand_name)
            self.slug = generate_unique_slug(self, base_slug)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.brand_name
    
    
class Item(models.Model):
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.CASCADE)
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, max_length=255)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.item_name)
            self.slug = generate_unique_slug(self, base_slug)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.item_name
    
    