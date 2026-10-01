from django.shortcuts import render

from Apps.Inventory.models import Product, StockTransaction


def dashboard(request):
    """Landing page: catalog KPIs plus the most recent stock movements."""
    total_skus = Product.objects.count()
    low_stock_count = sum(1 for p in Product.objects.all() if p.is_low_stock)
    recent_transactions = StockTransaction.objects.select_related('product', 'user')[:5]

    return render(request, 'core/dashboard.html', {
        'total_skus': total_skus,
        'low_stock_count': low_stock_count,
        'recent_transactions': recent_transactions,
    })
