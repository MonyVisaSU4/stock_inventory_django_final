from django.db import models


class Product(models.Model):
    """
    Represents a physical product tracked in the inventory.

    Rules:
    - `quantity` always starts at 0 and is NEVER directly editable.
      It is updated exclusively through StockTransaction records.
    - `reorder_level` is the threshold below which the product is
      considered "low stock" and visible to customers.
    """

    class Category(models.TextChoices):
        # Values match the <option value="..."> in the existing templates.
        DRINK = 'electronics', 'Drink'
        ACCESSORIES = 'groceries', 'Accessories'
        CLOTHING = 'clothing', 'Clothing'
        OTHER = 'other', 'Other'

    name = models.CharField(max_length=200)
    category = models.CharField(
        max_length=50,
        choices=Category.choices,
        default=Category.OTHER,
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # quantity is managed exclusively by StockTransaction — never edited directly.
    quantity = models.PositiveIntegerField(default=0, editable=False)

    reorder_level = models.PositiveIntegerField(default=10)
    barcode = models.CharField(max_length=100, unique=True, null=True, blank=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name

    @property
    def stock_status(self):
        """
        Returns a human-readable stock status string.
        Used by both admin and customer-facing views.
        """
        if self.quantity == 0:
            return 'Out of Stock'
        if self.quantity <= self.reorder_level:
            return f'Only {self.quantity} left'
        return 'In Stock'

    @property
    def is_low_stock(self):
        """True when quantity is at or below the reorder level (but > 0)."""
        return 0 < self.quantity <= self.reorder_level

    @property
    def is_out_of_stock(self):
        """True when no units are available."""
        return self.quantity == 0
