from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Product, StockTransaction
from .forms import StockAdjustmentForm, ProductForm


def product_list_view(request):
    """Catalog dashboard listing all products with search and low-stock filters."""
    search_query = request.GET.get('search', '').strip()
    low_stock_filter = request.GET.get('low_stock', '')

    products_qs = Product.objects.select_related('category').all()

    if search_query:
        products_qs = products_qs.filter(
            Q(name__icontains=search_query) | Q(sku__icontains=search_query)
        )

    all_products = list(products_qs)

    if low_stock_filter == '1':
        display_products = [p for p in all_products if p.is_low_stock]
    else:
        display_products = all_products

    # KPI counts across full catalog
    total_skus = Product.objects.count()
    low_stock_count = sum(1 for p in Product.objects.all() if p.is_low_stock)

    context = {
        'products': display_products,
        'search_query': search_query,
        'low_stock_filter': low_stock_filter,
        'total_skus': total_skus,
        'low_stock_count': low_stock_count,
    }
    return render(request, 'inventory/product_list.html', context)


def adjust_stock_view(request, pk):
    """
    Atomic stock adjustment view.
    Utilizes transaction.atomic() and select_for_update() to guarantee
    race-condition free inventory mutations and an immutable audit trail.
    """
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = StockAdjustmentForm(request.POST)
        if form.is_valid():
            tx_type = form.cleaned_data['transaction_type']
            qty = form.cleaned_data['quantity']
            reason = form.cleaned_data['reason']

            # Determine signed delta
            if tx_type in [StockTransaction.TransactionType.RESTOCK, StockTransaction.TransactionType.RETURN]:
                delta = qty
            else:
                delta = -qty

            try:
                with transaction.atomic():
                    # Acquire row lock in database until transaction completes
                    locked_product = Product.objects.select_for_update().get(pk=product.pk)
                    previous_stock = locked_product.quantity
                    new_stock = previous_stock + delta

                    if new_stock < 0:
                        messages.error(
                            request,
                            f"Adjustment rejected: Insufficient stock. On-hand is {previous_stock}, cannot deduct {qty}."
                        )
                        return render(request, 'inventory/adjust_stock.html', {'form': form, 'product': locked_product})

                    # Update on-hand count
                    locked_product.quantity = new_stock
                    locked_product.save(update_fields=['quantity', 'updated_at'])

                    # Create immutable audit record
                    user = request.user if request.user.is_authenticated else None
                    StockTransaction.objects.create(
                        product=locked_product,
                        user=user,
                        transaction_type=tx_type,
                        quantity_delta=delta,
                        previous_stock=previous_stock,
                        new_stock=new_stock,
                        reason=reason
                    )

                messages.success(
                    request,
                    f"Successfully recorded {tx_type} for {product.sku}. New stock: {new_stock} units."
                )
                return redirect('inventory:product_list')

            except Exception as e:
                messages.error(request, f"Database error during stock adjustment: {str(e)}")
    else:
        form = StockAdjustmentForm()

    return render(request, 'inventory/adjust_stock.html', {
        'form': form,
        'product': product
    })


def transaction_list_view(request):
    """Immutable audit trail view displaying all historical stock movements."""
    transactions_qs = StockTransaction.objects.select_related('product', 'user').all()

    product_sku = request.GET.get('sku', '').strip()
    if product_sku:
        transactions_qs = transactions_qs.filter(product__sku__icontains=product_sku)

    paginator = Paginator(transactions_qs, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'inventory/transaction_list.html', {
        'page_obj': page_obj,
        'product_sku': product_sku,
    })
