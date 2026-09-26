from django.shortcuts import render

# Create your views here.
title = 'Inventory'
desc = 'all inventory item is here.'


def inventory_list(request):
    return render(request, 'inventory/inventory_list.html', context={
        'title': title,
        'desc': desc
    })


def inventory_detail(request):
    return render(request, 'inventory/inventory_detail.html', context={
        'title': title,
        'desc': desc
    })


def edit_inventory(request):
    context = {
        'title': 'Edit Product'
    }
    return render(request, 'inventory/inventory_form.html', context)


def delete_inventory(request):
    return None


def add_inventory(request):
    context = {
        'title': 'Add Product'
    }
    return render(request, 'inventory/inventory_form.html', context)


# ── Customer-facing shop views ──

def shop_list(request):
    """Customer-facing product list (no exact quantities, no admin controls)."""
    return render(request, 'inventory/product_shop_list.html', context={
        'title': 'Products'
    })


def shop_detail(request):
    """Customer-facing product detail with Buy button."""
    return render(request, 'inventory/product_shop_detail.html', context={
        'title': 'Product Detail'
    })

