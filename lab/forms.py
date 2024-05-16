from django import forms
from . models import Lab
from core.models import UserProfile
from django.forms import ModelForm
from django.contrib.auth import get_user_model

User = get_user_model()

class LabCreateForm(ModelForm):
    lab_name = forms.CharField(max_length=255, label="Lab Name")
    room_no = forms.IntegerField(label="Room Number")
    users = forms.ModelMultipleChoiceField(queryset=UserProfile.objects.filter(is_lab_staff=True), label="Users", widget=forms.CheckboxSelectMultiple)
    
    class Meta:
        model = Lab
        fields = ['lab_name','room_no', 'users']
        

class BrandCreateForm(forms.Form):
    brand_name = forms.CharField(max_length=255, label="Brand Name")
        