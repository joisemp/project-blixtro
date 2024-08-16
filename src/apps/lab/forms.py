from django import forms
from django.urls import reverse
from apps.lab.models import Lab, LabSettings, Category, Item, ItemRemovalRecord, System
from apps.core.models import UserProfile
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from django.forms import ModelMultipleChoiceField, CheckboxSelectMultiple

User = get_user_model()


class ItemCreateFrom(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["item_name", "total_qty", "unit_of_measure", "brand", "category"]
        
    def __init__(self, *args, **kwargs):
        super(ItemCreateFrom, self).__init__(*args, **kwargs)
        self.fields['item_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['total_qty'].widget.attrs.update({'class': 'form-control'})
        self.fields['unit_of_measure'].widget.attrs.update({'class': 'form-control'})
        self.fields['brand'].widget.attrs.update({'class': 'form-select'})
        self.fields['category'].widget.attrs.update({'class': 'form-select'})
        
        self.fields['item_name'].label = "Item name"
        self.fields['total_qty'].label = "Total Quantity"
        self.fields['unit_of_measure'].label = "Unit of measure"
        self.fields['brand'].label = "Brand"
        self.fields['category'].label = "Category"


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

        
class ItemRemovalForm(ModelForm):
    class Meta:
        model = ItemRemovalRecord
        fields = ["reason", "qty", "remarks"] 
        labels = {
            "reason":"Reason",
            "qty":"Quantity",
            "remarks":"Remarks"
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.label_suffix = ''
        
        for field_name in self.fields:
            if self.initial.get(field_name):
                self.fields[field_name].widget.attrs['readonly'] = True
                self.fields[field_name].widget.attrs['class'] = self.fields[field_name].widget.attrs.get('class', '') + ' non-editable'
                self.fields[field_name].widget = forms.HiddenInput()
                
                # For choice fields like 'reason', disable the dropdown
                if isinstance(self.fields[field_name].widget, forms.Select):
                    self.fields[field_name].widget.attrs['disabled'] = True    
        
        self.fields['reason'].widget.attrs.update({'class': 'form-select'})
        self.fields['qty'].widget.attrs.update({'class': 'form-control'})
        self.fields['remarks'].widget.attrs.update({'class': 'form-control'})
                    

class SystemUpdateForm(ModelForm):
    class Meta:
        model = System
        fields = ["sys_name", "status"]
        
    def __init__(self, *args, **kwargs):
        super(SystemUpdateForm, self).__init__(*args, **kwargs)
        self.fields['sys_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['status'].widget.attrs.update({'class': 'form-control'})

        self.fields['sys_name'].label = "System Name"
        self.fields['status'].label = "Status"