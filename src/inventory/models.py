from django.db import models
from core.models import Organisation, UserProfile


class Department(models.Model):
    organisation = models.ForeignKey(Organisation,on_delete=models.CASCADE)
    department_name = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    udpated_on = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)


class Rooms(models.Model):
    organisation = models.ForeignKey(Organisation,on_delete=models.CASCADE)
    department = models.ForeignKey(Department,on_delete=models.CASCADE)
    label = models.CharField(max_length=20)
    room_name = models.CharField(max_length=255)
    incharge = models.OneToOneField(UserProfile,on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)


class Activity(models.Model):
    organisation = models.ForeignKey(Organisation,on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    #user = models.ForeignKey()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)


class Vendors(models.Model):
    organisation = models.ForeignKey(Organisation,on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)
    alternate_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    vendor_id = models.CharField(max_length=8,unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)


class Purchase(models.Model):
    UNIT_CHOICES = [
        ('kilogram','Kilogram'),
        ('litres','Litres'),
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
    #item = models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity = models.FloatField()
    unit_of_measure = models.CharField(max_length=10,choices=UNIT_CHOICES)
    vendor = models.ForeignKey(Vendors,on_delete=models.CASCADE)
    #brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    #category = models.ForeignKey(Category,on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES)
    updated_on = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)
    

class Issues(models.Model):
    organisation = models.ForeignKey(Organisation,on_delete=models.CASCADE)
    room = models.ForeignKey(Rooms,on_delete=models.CASCADE)
    #created_by "We need to fetch from users"
    subject = models.CharField(max_length=255)
    description = models.TextField()
    resolved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)


class Category(models.Model):
    organisation = models.ForeignKey(Organisation,on_delete=models.CASCADE)
    room = models.ForeignKey(Rooms,on_delete=models.CASCADE)
    category_name = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)



class Brand(models.Model):
    organisation = models.ForeignKey(Organisation,on_delete=models.CASCADE)
    room = models.ForeignKey(Rooms,on_delete=models.CASCADE)
    brand_name = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)
    