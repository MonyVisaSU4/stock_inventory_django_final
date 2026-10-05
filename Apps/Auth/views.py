from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from Apps.Auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from decouple import config
import random

# Create your views here.
custom_session = {
    'email': '',
    'otp-code': ''
}

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
    if request.method == 'POST':
        try:
            to = request.POST.get("email").strip()
            custom_session['email'] = to
            unique_numbers = random.sample(range(1, 9), 6)
            custom_session['otp-code'] = ''.join(map(str, unique_numbers))

            send_mail(
                subject='Verify OTP',
                message=f'your otp verification is: {unique_numbers}',
                from_email=config('EMAIL_HOST_USER'),
                recipient_list=[to],
                fail_silently=False
            )

            return redirect('auth:otp')
        except Exception as e:
            messages.error(
                request,
                str(e)
            )
    return render(request, 'verify-email.html')

def otp(request):
    email = custom_session['email']
    otp_code = custom_session['otp-code']

    if request.method == 'POST':
        otps = []

        for i in range(6):
            otps.append(request.POST.get(f"otp{i + 1}", ""))

        user_otp = ''.join(otps)

        if user_otp == otp_code:
            request.session['verified'] = True 
            return redirect('auth:done')
        else:
            request.session['verified'] = False
            return redirect('auth:done')

    context = {
        'email': email
    }

    return render(request, 'otp.html', context)

def done_verify(request):
    if request.session.get('verified'):
        status = 'success'
    else:
        status = 'denied'
    return render(request, 'done-verify.html', context={
        'status': status
    })

def new_password(request):
    if custom_session['otp-code'] == '':
        return redirect('auth:otp')

    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(
                request,
                "Passwords do not match."
            )
        else:
            user = User.objects.filter(email=custom_session['email']).first()
            user.set_password(password)
            user.save()
            return redirect('auth:login')
    return render(request, 'new-password.html')