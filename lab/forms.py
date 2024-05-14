from django import forms
from . models import Lab, GroupItem
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
        

class GroupItemCreateForm(ModelForm):
    class Meta:
        model = GroupItem
        fields = ["item", "qty"]
        
    def clean(self):
        super(GroupItemCreateForm, self).clean()
        item = self.cleaned_data.get('item')
        qty = self.cleaned_data.get('qty')
        
        if qty > item.total_qty:
            self.errors['qty'] = self.error_class(
                [f"Only {item.total_qty} {item.unit_of_measure} of {item} left"]
            )