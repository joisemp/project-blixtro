from django import forms
from inventory.models import StudentIssueReport

class IssueReportForm(forms.ModelForm):
    reg_no = forms.CharField(max_length=255, required=False, label="Registration No")
    admission_no = forms.CharField(max_length=255, required=False, label="Admission No")

    class Meta:
        model = StudentIssueReport
        fields = ['reg_no', 'admission_no', 'description', 'room']

    def clean(self):
        cleaned_data = super().clean()
        reg_no = cleaned_data.get("reg_no")
        admission_no = cleaned_data.get("admission_no")

        if not reg_no and not admission_no:
            raise forms.ValidationError("Please provide either Registration No or Admission No.")
        return cleaned_data
