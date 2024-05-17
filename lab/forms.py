from django import forms
from . models import Lab, LabSettings
from core.models import UserProfile
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from django.forms import ModelMultipleChoiceField, CheckboxSelectMultiple

User = get_user_model()

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
    widgets = {
      'items_tab': forms.CheckboxInput(attrs={'class': 'form-check-input ms-auto', 'role':'switch'}),
      'sys_tab': forms.CheckboxInput(attrs={'class': 'form-check-input ms-auto'}),
      'categories_tab': forms.CheckboxInput(attrs={'class': 'form-check-input ms-auto'}),
      'brands_tab': forms.CheckboxInput(attrs={'class': 'form-check-input ms-auto'}),
    }

        
        