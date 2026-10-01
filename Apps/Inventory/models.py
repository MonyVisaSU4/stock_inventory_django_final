from django.db import models
from django.urls import reverse
from decimal import Decimal
from Apps.Category.models import Category
from Apps.Product.models import Product
from django.core.validators import MinValueValidator
from Apps.UserManagement.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'inventory_categories'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    sku = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        help_text="Unique Stock Keeping Unit (e.g., SKU-1001)"
    )
    name = models.CharField(max_length=200, db_index=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    description = models.TextField(blank=True, default='')
    quantity = models.PositiveIntegerField(
        default=0,
        help_text="Current physical on-hand quantity"
    )
    low_stock_threshold = models.PositiveIntegerField(
        default=5,
        help_text="Threshold below which item triggers low-stock alerts"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'inventory_products'
        ordering = ['name']

    def __str__(self):
        return f"{self.sku} - {self.name}"

    @property
    def is_low_stock(self) -> bool:
        """Returns True if current quantity is at or below the alert threshold."""
        return self.quantity <= self.low_stock_threshold

    @property
    def is_out_of_stock(self) -> bool:
        """Returns True if current quantity is depleted."""
        return self.quantity == 0

    def get_absolute_url(self):
        return reverse('inventory:product_list')


class StockTransaction(models.Model):
    class TransactionType(models.TextChoices):
        RESTOCK = 'RESTOCK', 'Restock (Add Stock)'
        SALE = 'SALE', 'Sale (Deduct Stock)'
        DAMAGE = 'DAMAGE', 'Damage / Spoilage (Deduct Stock)'
        RETURN = 'RETURN', 'Customer Return (Add Stock)'

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='inventory_transactions'
    )
    transaction_type = models.CharField(
        max_length=20,
        choices=TransactionType.choices,
        db_index=True
    )
    quantity_delta = models.IntegerField(
        help_text="Signed stock difference (+50 for restock, -2 for sale)"
    )
    previous_stock = models.PositiveIntegerField()
    new_stock = models.PositiveIntegerField()
    reason = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'inventory_stock_transactions'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.transaction_type} | {self.product.sku} | Delta: {self.quantity_delta}"

