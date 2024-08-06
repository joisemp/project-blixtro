from django import forms
from purchases.models import Purchase

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