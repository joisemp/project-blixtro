from django import forms
from apps.purchases.models import Purchase, Vendor

class PurchaseCreateForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ["item", "vendor", "qty", "price"]
        
    def __init__(self, *args, **kwargs):
        super(PurchaseCreateForm, self).__init__(*args, **kwargs)
        self.fields['item'].widget.attrs.update({'class': 'form-control'})
        self.fields['vendor'].widget.attrs.update({'class': 'form-control'})
        self.fields['qty'].widget.attrs.update({'class': 'form-control'})
        self.fields['price'].widget.attrs.update({'class': 'form-control'})

        self.fields['item'].label = "Item"
        self.fields['vendor'].label = "Vendor"
        self.fields['qty'].label = "Quantity"
        self.fields['price'].label = "Price"
        
        
class PurchaseUpdateForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ["vendor", "qty", "price"]
        
    def __init__(self, *args, **kwargs):
        super(PurchaseUpdateForm, self).__init__(*args, **kwargs)
        self.fields['vendor'].widget.attrs.update({'class': 'form-control'})
        self.fields['qty'].widget.attrs.update({'class': 'form-control'})
        self.fields['price'].widget.attrs.update({'class': 'form-control'})

        self.fields['vendor'].label = "Vendor"
        self.fields['qty'].label = "Quantity"
        self.fields['price'].label = "Price"
        
        
class VendorCreateFrom(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name', 'address']
        
    def __init__(self, *args, **kwargs):
        super(VendorCreateFrom, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['address'].widget.attrs.update({'class': 'form-control'})

        self.fields['name'].label = "Vendor Name"
        self.fields['address'].label = "Address"
