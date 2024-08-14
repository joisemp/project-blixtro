from django import forms

from apps.org.models import Department


class DepartmentCreateAndUpdateForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ["name", "head"]
        
    def __init__(self, *args, **kwargs):
        super(DepartmentCreateAndUpdateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['head'].widget.attrs.update({'class': 'form-select'})