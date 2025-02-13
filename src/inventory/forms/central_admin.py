from django import forms
from inventory.models import Department,Rooms,Vendors,Purchase,Issues,Category,Brand

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


class Purchase(forms.ModelForm):

    class Meta:
        model = Purchase
        fields = ['item_name','item','quantity','unit_of_measure','vendor','brand','category','status']


class Issues(forms.ModelForm):

    class Meta:
        model = Issues
        fields = ['subject','description','resolved']


class Category(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['category_name']



class Brand(forms.ModelForm):

    class Meta:
        model = Brand
        fields = ['brand_name']