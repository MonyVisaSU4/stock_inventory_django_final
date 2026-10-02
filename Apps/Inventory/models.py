from django.db import models


class Supplier(models.Model):
    name = models.CharField(max_length=150, unique=True)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    TYPE_CHOICES = (
        ('WAREHOUSE', 'Warehouse Node'),
        ('STORE', 'Retail Store Front'),
    )
    name = models.CharField(max_length=100, unique=True)
    location_type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.get_location_type_display()})"


class Product(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    retail_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    low_stock_alert = models.IntegerField(default=5)

    def __str__(self):
        return f"{self.sku} - {self.name}"

    @property
    def total_stock(self):
        return sum(stock.quantity for stock in self.stocks.all())


class ProductLocation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stocks')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='stocks')
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('product', 'location')

    def __str__(self):
        return f"{self.product.name} @ {self.location.name}: {self.quantity}"


class InventoryLog(models.Model):
    LOG_TYPES = (
        ('STOCK_IN', 'Intake'),
        ('STOCK_OUT', 'Sale Checkout'),
        ('TRANSFER', 'Internal Relocation'),
        ('ADJUSTMENT', 'Manual Check'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='logs')
    quantity_changed = models.IntegerField()
    log_type = models.CharField(max_length=20, choices=LOG_TYPES)
    source_location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='log_sources'
    )
    destination_location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='log_destinations'
    )
    reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.log_type}] {self.product.sku} ({self.quantity_changed}) at {self.created_at:%Y-%m-%d %H:%M}"
