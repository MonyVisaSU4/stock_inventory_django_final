from django.shortcuts import render

# Create your views here.
def inventory_list(request):
    return render(request, 'inventory/inventory_list.html')

def inventory_detail(request):
    return render(request, 'inventory/inventory_detail.html')

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