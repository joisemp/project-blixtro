from django import forms
from inventory.models import Category, Brand, Item, System

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name']

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['brand_name']

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_name', 'category', 'brand']

class SystemForm(forms.ModelForm):
    class Meta:
        model = System
        fields = ['system_name', 'status']