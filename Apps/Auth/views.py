from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth import get_user_model
from django.contrib import messages
from Apps.Auth.decorators import role_required
from .forms import ProfileEditForm, CustomPasswordChangeForm, UserCreateForm, UserEditForm, RegisterForm

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
    """Public self-registration. All self-registered users get STAFF role."""
    if request.user.is_authenticated:
        return redirect('inventory:dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, f"Welcome, {user.get_full_name() or user.username}! Your account has been created.")
            return redirect('inventory:dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()
    return render(request, 'auth/register.html', {'form': form})


def logout_view(request):
    auth_logout(request)
    messages.info(request, "You have been safely logged out.")
    return redirect('auth:login')


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
    return render(request, 'auth/settings.html')


# ─────────────────────────────────────────────
#  User Management (Admin only)
# ─────────────────────────────────────────────
@role_required('ADMIN')
def user_list_view(request):
    users = User.objects.all().order_by('-date_joined')
    context = {'users': users}
    return render(request, 'auth/user_list.html', context)


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