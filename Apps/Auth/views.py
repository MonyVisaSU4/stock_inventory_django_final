from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages


def login_view(request):
    if request.user.is_authenticated:
        return redirect('inventory:dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.status == 'ACTIVE':
                auth_login(request, user)
                messages.success(request, f"Welcome back, {user.username} ({user.get_role_display()})!")
                next_url = request.GET.get('next') or request.POST.get('next') or 'inventory:dashboard'
                return redirect(next_url)
            else:
                messages.error(request, "Your account is currently inactive. Contact your administrator.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'auth/login.html')


def logout_view(request):
    auth_logout(request)
    messages.info(request, "You have been safely logged out.")
    return redirect('auth:login')