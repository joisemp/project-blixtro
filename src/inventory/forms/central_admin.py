from django import forms
from inventory.models import Department,Rooms,Vendors

class DepartmentForm(forms.ModelForm):

    class Meta:
        model = Department
        fields = ['department_name']


class RoomForm(forms.ModelForm):

    class Meata:
        model = Rooms
        fields = ['label','room_name','incharge']


class VendorForm(forms.ModelForm):

    class Meta:
        model = Vendors
        fields = ['vendor_name','contact_number','alternate_number','address']  



