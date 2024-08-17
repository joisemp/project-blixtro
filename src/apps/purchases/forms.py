from django import forms
from apps.purchases.models import Purchase, Vendor

class PurchaseCreateForm(forms.ModelForm):
    new_item = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="New Item"
    )

    class Meta:
        model = Purchase
        fields = ["new_item", "item", "vendor", "qty", "price"]
        
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(PurchaseCreateForm, self).__init__(*args, **kwargs)
        self.label_suffix = ''

        self.fields['item'].widget.attrs.update({'class': 'form-control'})
        self.fields['vendor'].widget.attrs.update({'class': 'form-control'})
        self.fields['qty'].widget.attrs.update({'class': 'form-control'})
        self.fields['price'].widget.attrs.update({'class': 'form-control'})

        self.fields['item'].label = "Item"
        self.fields['vendor'].label = "Vendor"
        self.fields['qty'].label = "Quantity"
        self.fields['price'].label = "Price"

        if request and request.GET.get('new_item') == 'true':
            self.fields['new_item'].required = True
            self.fields['item'].required = False
            self.fields['new_item'].widget.attrs.update({'class': 'form-control'})
            self.fields['item'].widget = forms.HiddenInput()  # Hide the item field
        else:
            # Hide the new_item field and make it not required
            self.fields['new_item'].required = False
            self.fields['new_item'].widget = forms.HiddenInput()
            self.fields['item'].required = True

        
        
        
        
class PurchaseUpdateForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ["vendor", "qty", "price"]
        
    def __init__(self, *args, **kwargs):
        super(PurchaseUpdateForm, self).__init__(*args, **kwargs)
        self.label_suffix = ''
        
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
        self.label_suffix = ''
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['address'].widget.attrs.update({'class': 'form-control'})

        self.fields['name'].label = "Vendor Name"
        self.fields['address'].label = "Address"
