from django.shortcuts import render

# Create your views here.
title = 'Stock'
desc = 'You can tracking stock--in and stock-out here'


def list(request):
    return render(request, 'stock/stock_list.html', context={
        'title': title,
        'desc': desc
    })
