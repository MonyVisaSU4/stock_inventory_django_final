from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, Count, F
from django.core.exceptions import ValidationError
from Apps.Auth.decorators import role_required
from .models import Product, Location, ProductLocation, InventoryLog, Supplier
from .services import InventoryService


@role_required('ADMIN', 'MANAGER', 'CASHIER')
def dashboard_view(request):
    total_products = Product.objects.count()
    total_locations = Location.objects.count()
    
    # Calculate low stock products across all locations
    low_stock_products = []
    for product in Product.objects.prefetch_related('stocks', 'stocks__location').all():
        total_qty = sum(stock.quantity for stock in product.stocks.all())
        if total_qty <= product.low_stock_alert:
            low_stock_products.append({
                'product': product,
                'total_qty': total_qty,
                'threshold': product.low_stock_alert
            })

    # Recent Telemetry Logs
    recent_logs = InventoryLog.objects.select_related(
        'product', 'source_location', 'destination_location'
    ).order_by('-created_at')[:10]

    # Inventory Valuation
    stock_aggregates = ProductLocation.objects.select_related('product').aggregate(
        total_units=Sum('quantity')
    )

    context = {
        'total_products': total_products,
        'total_locations': total_locations,
        'low_stock_count': len(low_stock_products),
        'low_stock_products': low_stock_products[:5],
        'recent_logs': recent_logs,
        'total_units': stock_aggregates['total_units'] or 0,
        'user_role': getattr(request.user, 'role', 'GUEST')
    }
    return render(request, 'inventory/dashboard.html', context)


@role_required('ADMIN', 'MANAGER', 'CASHIER')
def product_list_view(request):
    query = request.GET.get('q', '').strip()
    products = Product.objects.prefetch_related('stocks__location', 'supplier').all()

    if query:
        products = products.filter(name__icontains=query) | products.filter(sku__icontains=query)

    context = {
        'products': products,
        'query': query,
    }
    return render(request, 'inventory/product_list.html', context)


@role_required('ADMIN', 'MANAGER')
def stock_transfer_view(request):
    products = Product.objects.all()
    locations = Location.objects.all()

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        source_id = request.POST.get('source_location_id')
        dest_id = request.POST.get('destination_location_id')
        quantity_str = request.POST.get('quantity')
        reason = request.POST.get('reason', '').strip()

        try:
            if not all([product_id, source_id, dest_id, quantity_str]):
                raise ValidationError("All fields are required.")

            quantity = int(quantity_str)
            result = InventoryService.transfer_stock(
                product_id=product_id,
                source_location_id=source_id,
                destination_location_id=dest_id,
                quantity=quantity,
                user=request.user,
                reason=reason
            )
            messages.success(
                request,
                f"Successfully transferred {quantity} units. Source stock now: {result['source_remaining']}, Destination stock now: {result['dest_total']}."
            )
            return redirect('inventory:transfer')

        except ValidationError as e:
            messages.error(request, str(e.message if hasattr(e, 'message') else e))
        except Exception as e:
            messages.error(request, f"Transfer System Interrupted: {str(e)}")

    context = {
        'products': products,
        'locations': locations,
    }
    return render(request, 'inventory/stock_transfer.html', context)


@role_required('ADMIN', 'MANAGER', 'CASHIER')
def stock_checkout_view(request):
    products = Product.objects.all()
    locations = Location.objects.filter(location_type='STORE')

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        location_id = request.POST.get('location_id')
        quantity_str = request.POST.get('quantity')
        reason = request.POST.get('reason', '').strip()

        try:
            if not all([product_id, location_id, quantity_str]):
                raise ValidationError("Product, Store Location, and Quantity are required.")

            quantity = int(quantity_str)
            result = InventoryService.checkout_stock(
                product_id=product_id,
                location_id=location_id,
                quantity=quantity,
                user=request.user,
                reason=reason
            )
            messages.success(
                request,
                f"Checkout sale processed. Remaining store stock: {result['remaining_quantity']} units."
            )
            return redirect('inventory:checkout')

        except ValidationError as e:
            messages.error(request, str(e.message if hasattr(e, 'message') else e))
        except Exception as e:
            messages.error(request, f"Checkout failed: {str(e)}")

    context = {
        'products': products,
        'locations': locations,
    }
    return render(request, 'inventory/stock_checkout.html', context)


@role_required('ADMIN', 'MANAGER')
def stock_intake_view(request):
    products = Product.objects.all()
    locations = Location.objects.all()

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        location_id = request.POST.get('location_id')
        quantity_str = request.POST.get('quantity')
        reason = request.POST.get('reason', '').strip()

        try:
            if not all([product_id, location_id, quantity_str]):
                raise ValidationError("All fields are required.")

            quantity = int(quantity_str)
            result = InventoryService.intake_stock(
                product_id=product_id,
                location_id=location_id,
                quantity=quantity,
                user=request.user,
                reason=reason
            )
            messages.success(
                request,
                f"Stock intake recorded. Updated location quantity: {result['current_quantity']} units."
            )
            return redirect('inventory:intake')

        except ValidationError as e:
            messages.error(request, str(e.message if hasattr(e, 'message') else e))
        except Exception as e:
            messages.error(request, f"Intake operation failed: {str(e)}")

    context = {
        'products': products,
        'locations': locations,
    }
    return render(request, 'inventory/stock_intake.html', context)


@role_required('ADMIN', 'MANAGER')
def inventory_logs_view(request):
    log_type = request.GET.get('type')
    logs = InventoryLog.objects.select_related(
        'product', 'source_location', 'destination_location'
    ).order_by('-created_at')

    if log_type:
        logs = logs.filter(log_type=log_type)

    context = {
        'logs': logs[:100],
        'selected_type': log_type,
        'log_types': InventoryLog.LOG_TYPES,
    }
    return render(request, 'inventory/logs.html', context)
