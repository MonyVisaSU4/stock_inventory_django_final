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
        'title': 'Edit Inventory'
    }
    return render(request, 'inventory/inventory_form.html', context)


def delete_inventory(request):
    return None


def add_inventory(request):
    context = {
        'title': 'Add Inventory'
    }
    return render(request, 'inventory/inventory_form.html', context)
