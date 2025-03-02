from django import forms
from inventory.models import Category, Brand, Item, System, SystemComponent, Archive, Room, Purchase, Vendor, Receipt
from config.mixins import form_mixin

class CategoryForm(form_mixin.BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name']

class BrandForm(form_mixin.BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['brand_name']

class ItemForm(form_mixin.BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_name', 'category', 'brand', 'total_count']  # Include necessary fields

class SystemForm(forms.ModelForm):
    class Meta:
        model = System
        fields = ['system_name', 'status']

class SystemComponentForm(forms.ModelForm):
    class Meta:
        model = SystemComponent
        fields = ['component_item', 'component_type', 'serial_number']  # Updated field

class SystemComponentArchiveForm(forms.ModelForm):
    class Meta:
        model = Archive
        fields = ['archive_type', 'remark']

class ItemArchiveForm(forms.ModelForm):
    count = forms.IntegerField(min_value=1)

    class Meta:
        model = Archive
        fields = ['archive_type', 'remark', 'count']

class RoomUpdateForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['label', 'room_name', 'department', 'incharge']  # Adjust fields as necessary

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['item', 'quantity', 'unit_of_measure', 'vendor']  # Include necessary fields
        
        
class PurchaseUpdateForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['quantity', 'unit_of_measure', 'vendor']  # Include necessary fields

class ItemPurchaseForm(forms.ModelForm):
    item_name = forms.CharField(max_length=255)
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    brand = forms.ModelChoiceField(queryset=Brand.objects.all())
    quantity = forms.FloatField(min_value=1)
    unit_of_measure = forms.ChoiceField(choices=Purchase.UNIT_CHOICES)
    vendor = forms.ModelChoiceField(queryset=Vendor.objects.all())

    class Meta:
        model = Purchase
        fields = ['item_name', 'category', 'brand', 'quantity', 'unit_of_measure', 'vendor']

class PurchaseCompleteForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = ['receipt', 'remarks']