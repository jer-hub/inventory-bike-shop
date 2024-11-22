from django import forms
from .models import Supplier, Product

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['supplier_name', 'contact_name', 'phone', 'email', 'address', 'city', 'state', 'postal_code', 'country']
        widgets = {
            'supplier_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Supplier Name'}),
            'contact_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Current Address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal Code'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'category', 'supplier', 'quantity_in_stock', 'reorder_level', 'cost_price', 'selling_price']
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Name'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category'}),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'quantity_in_stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity in Stock'}),
            'reorder_level': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Reorder Level'}),
            'cost_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cost Price', 'step': '0.01'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Selling Price', 'step': '0.01'}),
        }
