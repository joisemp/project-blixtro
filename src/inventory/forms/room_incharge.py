from django import forms
from inventory.models import Category, Brand

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name']

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['brand_name']