from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def dashboard(request):
    context = {
        'total_products': 0,
        'total_units': 0,
        'total_locations': 0,
        'low_stock_count': 0
    }
    return render(request, 'core/dashboard.html', context)

