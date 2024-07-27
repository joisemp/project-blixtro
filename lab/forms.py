from django import forms
from django.urls import reverse
from lab.models import Lab, LabSettings, Category, Item
from core.models import UserProfile
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from django.forms import ModelMultipleChoiceField, CheckboxSelectMultiple

User = get_user_model()


class AddSystemComponetForm(forms.Form):
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

    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
    item = forms.ModelChoiceField(queryset=Item.objects.all(), required=True)
    component_type = forms.ChoiceField(choices=COMPONENT_TYPES, required=True)
    serial_no = forms.CharField(max_length=255, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "category" in self.data:
            try:
                category_id = int(self.data.get("category"))
                self.fields["item"].queryset = Item.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                self.fields["item"].queryset = Item.objects.all()
        else:
            self.fields["item"].queryset = Item.objects.all()


class LabCreateForm(ModelForm):
    lab_name = forms.CharField(max_length=255, label="Lab Name")
    room_no = forms.IntegerField(label="Room Number")
    users = ModelMultipleChoiceField(
        queryset=UserProfile.objects.filter(is_lab_staff=True),
        label="Users",
        widget=CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
    )
    
    class Meta:
        model = Lab
        fields = ['lab_name','room_no', 'users']
        

class BrandCreateForm(forms.Form):
    brand_name = forms.CharField(max_length=255, label="Brand Name")
    

class LabSettingsForm(ModelForm):
  class Meta:
    model = LabSettings
    fields = ["items_tab", "sys_tab", "categories_tab", "brands_tab"]
    labels = {
            "items_tab": "Items tab",
            "sys_tab": "Systems tab",
            "categories_tab": "Categories tab",
            "brands_tab": "Brands tab",
        }
    widgets = {
      'items_tab': forms.CheckboxInput(attrs={'class': 'form-check-input ms-auto', 'role':'switch'}),
      'sys_tab': forms.CheckboxInput(attrs={'class': 'form-check-input ms-auto'}),
      'categories_tab': forms.CheckboxInput(attrs={'class': 'form-check-input ms-auto'}),
      'brands_tab': forms.CheckboxInput(attrs={'class': 'form-check-input ms-auto'}),
    }

        
        