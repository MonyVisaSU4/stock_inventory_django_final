from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from Apps.Auth.models import User
from django.contrib.auth.hashers import make_password, check_password


# Create your views here.
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")

        user = User.objects.filter(email=email).first()

        if user is None:
            messages.error(
                request,
                "Invalid email or password."
            )
            return render(
                request,
                "login.html"
            )

        if not user.check_password(password):
            messages.error(request, "Invalid email or password.")
            return render(request, "login.html")

        login(request, user)
        return redirect('core:dashboard')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('auth:login')


def register(request):
    if request.method == 'POST':
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()

        user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=make_password(password),
        )
        user.save()
    return render(request, 'register.html')

def verify_email(request):
    return render(request, 'verify-email.html')

def otp(request):
    return render(request, 'otp.html')

def done_verify(request):
    return render(request, 'done-verify.html', context={
        'status': 'success'
    })