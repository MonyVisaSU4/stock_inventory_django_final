from django.shortcuts import render

# Create your views here.
def product_list(request):
    return render(request, 'customer/product_list.html', context={
        'title': 'Welcome',
        'role': 'Customer',
        'desc': 'buy as much as you wanted.'
    })

def product_detail(request):
    return render(request, 'customer/product_detail.html', context={
        'title': 'Welcome',
        'role': 'Customer',
        'desc': 'buy as much as you wanted.'
    })