from django import forms
from .models import StockTransaction, Product


class StockAdjustmentForm(forms.Form):
    transaction_type = forms.ChoiceField(
        choices=StockTransaction.TransactionType.choices,
        widget=forms.Select(attrs={
            'style': 'width: 100%; padding: 10px 12px; font-size: 14px; border: 1px solid #cbd5e1; border-radius: 6px; box-sizing: border-box; background-color: #ffffff; color: #0f172a; outline: none;'
        })
    )
    quantity = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={
            'style': 'width: 100%; padding: 10px 12px; font-size: 14px; border: 1px solid #cbd5e1; border-radius: 6px; box-sizing: border-box; background-color: #ffffff; color: #0f172a; outline: none;',
            'placeholder': 'Enter units (e.g., 25)'
        })
    )
    reason = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'style': 'width: 100%; padding: 10px 12px; font-size: 14px; border: 1px solid #cbd5e1; border-radius: 6px; box-sizing: border-box; background-color: #ffffff; color: #0f172a; outline: none;',
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
            'sku': forms.TextInput(attrs={'style': 'width: 100%; padding: 8px 12px; border: 1px solid #cbd5e1; border-radius: 6px; box-sizing: border-box;'}),
            'name': forms.TextInput(attrs={'style': 'width: 100%; padding: 8px 12px; border: 1px solid #cbd5e1; border-radius: 6px; box-sizing: border-box;'}),
            'category': forms.Select(attrs={'style': 'width: 100%; padding: 8px 12px; border: 1px solid #cbd5e1; border-radius: 6px; box-sizing: border-box;'}),
            'price': forms.NumberInput(attrs={'style': 'width: 100%; padding: 8px 12px; border: 1px solid #cbd5e1; border-radius: 6px; box-sizing: border-box;'}),
            'description': forms.Textarea(attrs={'rows': 3, 'style': 'width: 100%; padding: 8px 12px; border: 1px solid #cbd5e1; border-radius: 6px; box-sizing: border-box;'}),
            'quantity': forms.NumberInput(attrs={'style': 'width: 100%; padding: 8px 12px; border: 1px solid #cbd5e1; border-radius: 6px; box-sizing: border-box;'}),
            'low_stock_threshold': forms.NumberInput(attrs={'style': 'width: 100%; padding: 8px 12px; border: 1px solid #cbd5e1; border-radius: 6px; box-sizing: border-box;'}),
        }
