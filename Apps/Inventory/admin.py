from django.contrib import admin
from .models import Category, Product, StockTransaction

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'quantity',
        'low_stock_threshold',
        'is_low_stock'
    )
    list_filter = ('category',)
    search_fields = ('sku', 'name')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(StockTransaction)
class StockTransactionAdmin(admin.ModelAdmin):
    list_display = (
        'created_at',
        'product',
        'transaction_type',
        'quantity_delta',
        'previous_stock',
        'new_stock',
        'user'
    )
    list_filter = ('transaction_type', 'created_at')
    search_fields = ('product__sku', 'product__name', 'reason', 'user__username')
    readonly_fields = (
        'product',
        'user',
        'transaction_type',
        'quantity_delta',
        'previous_stock',
        'new_stock',
        'reason',
        'created_at'
    )

    def has_add_permission(self, request):
        # Stock transactions are immutable audit logs created via stock operations
        return False

    def has_delete_permission(self, request, obj=None):
        return False
