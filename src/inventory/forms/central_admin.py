from django import forms
from inventory.models import Department,

class DepartmentForm(forms.ModelForm):

    class Meta:
        model = Department
        fields = ["department_name"]
