from django import forms
from core.models import User, UserProfile
from inventory.models import Department, Room, Vendor, Purchase, Issue, Category, Brand

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['department_name']


class RoomForm(forms.ModelForm):
    class Meata:
        model = Room
        fields = ['label','room_name','incharge']


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['vendor_name','contact_number','alternate_number','address']  


class Purchase(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['item_name','item','quantity','unit_of_measure','vendor','brand','category','status']


class Issues(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['subject','description','resolved']


class Category(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name']


class Brand(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['brand_name']
        
        
class PeopleCreateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = UserProfile
        fields = ['email', 'first_name', 'last_name', 'is_central_admin', 'is_incharge']  
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email


class RoomCreateForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['label', 'room_name', 'department', 'incharge']  # Adjust fields as necessary