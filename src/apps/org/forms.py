from django import forms
from apps.org.models import Department
from config.mixins.form_mixins import CustomFormMixin


class DepartmentCreateAndUpdateForm(CustomFormMixin, forms.ModelForm):
    class Meta:
        model = Department
        fields = ["name", "head"]
        
    def __init__(self, *args, **kwargs):
        super(DepartmentCreateAndUpdateForm, self).__init__(*args, **kwargs)
        self.label_suffix = ''
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['head'].widget.attrs.update({'class': 'form-select'})
        
        self.fields['name'].label = "Name"
        self.fields['head'].label = "Head of departement"

