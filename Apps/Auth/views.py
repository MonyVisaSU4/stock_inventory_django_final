from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def verify_email(request):
    return render(request, 'verify-email.html')

def otp(request):
    return render(request, 'otp.html')

def done_verify(request):
    return render(request, 'done-verify.html', context={
        'status': 'success'
    })