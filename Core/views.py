from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import datetime


@login_required
def dashboard(request):
    context = {

    }
    return render(request, 'core/dashboard.html', context)
