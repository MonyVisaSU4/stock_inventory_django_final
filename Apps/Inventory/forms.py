from django import forms
from .models import StockTransaction, Product


class StockAdjustmentForm(forms.Form):
    transaction_type = forms.ChoiceField(
        choices=StockTransaction.TransactionType.choices,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    quantity = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter units (e.g., 25)'
        })
    )
    reason = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., Received shipment PO-901 or Damaged in warehouse'
        })
    )

    def clean_quantity(self):
        qty = self.cleaned_data.get('quantity')
        if qty is None or qty <= 0:
            raise forms.ValidationError("Quantity must be a positive integer greater than zero.")
        return qty


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['sku', 'name', 'category', 'price', 'description', 'quantity', 'low_stock_threshold']
        widgets = {
            'sku': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'low_stock_threshold': forms.NumberInput(attrs={'class': 'form-control'}),
        }
