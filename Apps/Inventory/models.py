from django.db import models

from Apps.Category.models import Category
from Apps.Product.models import Product


# Create your models here.
class Inventory(models.Model):
    id = models.BigAutoField(primary_key=True)
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='inventory')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    current_quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='inventory_photos/', blank=True, null=True)
    reorder_level = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Inventory"

