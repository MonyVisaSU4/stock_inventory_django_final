from django.shortcuts import render

# Create your views here.
title = 'Stock'
desc = 'You can track stock-in and stock-out here'


def list(request):
    return render(request, 'stock/stock_list.html', context={
        'title': title,
        'desc': desc
    })


def movement(request):
    """Log a Stock Movement (Stock In / Stock Out)."""
    return render(request, 'stock/stock_form.html', context={
        'title': 'Log Stock Movement',
        'desc': 'Record a stock-in or stock-out transaction.'
    })


def take(request):
    """Stock Take / Audit Correction."""
    return render(request, 'stock/stock_take.html', context={
        'title': 'Stock Take / Audit',
        'desc': 'Correct a product\'s quantity to match the physical count.'
    })
