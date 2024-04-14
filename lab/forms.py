from django import forms
from . models import Lab
from django.forms import ModelForm
from django.contrib.auth import get_user_model

User = get_user_model()

class LabCreateForm(ModelForm):
    lab_name = forms.CharField(max_length=255, label="Lab Name")
    room_no = forms.IntegerField(label="Room Number")
    users = forms.ModelMultipleChoiceField(queryset=User.objects.filter(is_superuser=False), label="Users", widget=forms.CheckboxSelectMultiple)
    
    class Meta:
        model = Lab
        fields = ['lab_name','room_no', 'users']