from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from Apps.Auth.decorators import role_required
from .forms import ProfileEditForm, CustomPasswordChangeForm, UserCreateForm, UserEditForm, RegisterForm, OTPVerifyForm
import random
import string

User = get_user_model()


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
                messages.success(request, f"Welcome back, {user.get_full_name() or user.username}!")
                next_url = request.GET.get('next') or request.POST.get('next') or 'inventory:dashboard'
                return redirect(next_url)
            else:
                messages.error(request, "Your account is currently inactive. Contact your administrator.")
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    return render(request, 'auth/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('inventory:dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            _send_otp(request, user)
            messages.info(request, f"A 6-digit verification code was sent to {user.email}.")
            return redirect('auth:verify-email')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()
    return render(request, 'auth/register.html', {'form': form})


def logout_view(request):
    auth_logout(request)
    messages.info(request, "You have been safely logged out.")
    return redirect('auth:login')


def send_otp_view(request):
    if request.user.is_authenticated:
        user = request.user
    else:
        if request.method == 'POST':
            identifier = request.POST.get('identifier', '').strip()
            user = User.objects.filter(email__iexact=identifier).first() or User.objects.filter(username__iexact=identifier).first()
            if not user:
                messages.error(request, "No account found with that email or username.")
                return redirect('auth:verify-email')
        else:
            return redirect('auth:login')
    if not user.email:
        messages.error(request, "No email address registered for this account.")
        return redirect('auth:profile-edit' if request.user.is_authenticated else 'auth:login')
    _send_otp(request, user)
    messages.info(request, f"A verification code was sent to {user.email}.")
    return redirect('auth:verify-email')


def verify_email_view(request):
    user_pk = request.session.get('otp_user_pk')
    user = None
    if user_pk:
        user = User.objects.filter(pk=user_pk).first()
    elif request.user.is_authenticated:
        user = request.user
        _send_otp(request, user)

    if request.method == 'POST':
        if request.POST.get('action') == 'request_otp' or 'identifier' in request.POST:
            identifier = request.POST.get('identifier', '').strip()
            found_user = User.objects.filter(email__iexact=identifier).first() or User.objects.filter(username__iexact=identifier).first()
            if found_user:
                if found_user.email:
                    _send_otp(request, found_user)
                    messages.success(request, f"Verification code sent to {found_user.email}.")
                    return redirect('auth:verify-email')
                else:
                    messages.error(request, "This account does not have an email address.")
            else:
                messages.error(request, "No account found with that email or username.")
            return render(request, 'auth/verify_email.html', {'needs_email': True})

        form = OTPVerifyForm(request.POST)
        if form.is_valid():
            if _verify_otp(request, form.cleaned_data['otp']):
                target_user = user or (User.objects.filter(pk=request.session.get('otp_user_pk')).first())
                request.session.pop('otp_code', None)
                request.session.pop('otp_created_at', None)
                request.session.pop('otp_user_pk', None)
                request.session.modified = True
                request.session.save()
                if target_user and not request.user.is_authenticated:
                    auth_login(request, target_user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, "Email verified successfully! Welcome.")
                return redirect('inventory:dashboard')
            else:
                messages.error(request, "Invalid or expired code. Please try again or resend.")
    else:
        form = OTPVerifyForm()

    if not user:
        return render(request, 'auth/verify_email.html', {'needs_email': True, 'form': form})

    return render(request, 'auth/verify_email.html', {'form': form, 'email': user.email, 'needs_email': False})


def resend_otp_view(request):
    user_pk = request.session.get('otp_user_pk')
    if not user_pk and request.user.is_authenticated:
        user_pk = request.user.pk
    if not user_pk:
        messages.error(request, "Please enter your email or username to request a verification code.")
        return redirect('auth:verify-email')
    user = get_object_or_404(User, pk=user_pk)
    if not user.email:
        messages.error(request, "No email address on file.")
        return redirect('auth:settings')
    _send_otp(request, user)
    messages.info(request, f"A new verification code was sent to {user.email}.")
    return redirect('auth:verify-email')


@role_required('ADMIN', 'MANAGER', 'STAFF')
def profile_view(request):
    return render(request, 'auth/profile.html', {'user_profile': request.user})


@role_required('ADMIN', 'MANAGER', 'STAFF')
def profile_edit_view(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('auth:profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'auth/profile_edit.html', {'form': form})


@role_required('ADMIN', 'MANAGER', 'STAFF')
def change_password_view(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully.")
            return redirect('auth:profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'auth/change_password.html', {'form': form})


@role_required('ADMIN', 'MANAGER', 'STAFF')
def settings_view(request):
    return render(request, 'auth/settings.html', {'user_profile': request.user})


@role_required('ADMIN')
def user_list_view(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'auth/user_list.html', {'users': users})


@role_required('ADMIN')
def user_create_view(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"User '{user.username}' created successfully.")
            return redirect('auth:user-list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserCreateForm()
    return render(request, 'auth/user_form.html', {'form': form, 'page_title': 'Create User', 'form_action': 'Create'})


@role_required('ADMIN')
def user_edit_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f"User '{user.username}' updated successfully.")
            return redirect('auth:user-list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserEditForm(instance=user)
    return render(request, 'auth/user_form.html', {'form': form, 'user_obj': user, 'page_title': 'Edit User', 'form_action': 'Update'})


@role_required('ADMIN')
def user_toggle_status_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user == request.user:
        messages.error(request, "You cannot deactivate your own account.")
        return redirect('auth:user-list')
    if request.method == 'POST':
        if user.status == 'ACTIVE':
            user.status = 'INACTIVE'
            messages.warning(request, f"User '{user.username}' has been deactivated.")
        else:
            user.status = 'ACTIVE'
            messages.success(request, f"User '{user.username}' has been activated.")
        user.save()
    return redirect('auth:user-list')


def _send_otp(request, user):
    code = ''.join(random.choices(string.digits, k=6))
    request.session['otp_code'] = code
    request.session['otp_created_at'] = timezone.now().isoformat()
    request.session['otp_user_pk'] = user.pk
    request.session.modified = True
    request.session.save()
    send_mail(
        "Your Stock Inventory verification code",
        f"Hi {user.get_full_name() or user.username},\n\nYour verification code is:\n\n  {code}\n\nExpires in 10 minutes.\n\n— Stock Inventory Team",
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )


def _verify_otp(request, code):
    stored_code = request.session.get('otp_code')
    stored_ts = request.session.get('otp_created_at')
    if not stored_code or not stored_ts:
        return False
    if stored_code != code:
        return False
    created_at = timezone.datetime.fromisoformat(stored_ts)
    if timezone.is_naive(created_at):
        created_at = timezone.make_aware(created_at)
    return timezone.now() <= created_at + timezone.timedelta(minutes=10)