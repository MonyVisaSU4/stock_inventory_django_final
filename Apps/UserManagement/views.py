from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods

from .forms import LoginForm, RegisterForm


@require_http_methods(['GET', 'POST'])
def register_view(request):
    """Create a new CUSTOMER account and sign the user straight in."""
    if request.user.is_authenticated:
        return redirect('core:dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}! Your account has been created.')
            return redirect('core:dashboard')
    else:
        form = RegisterForm()

    return render(request, 'usermanagement/register.html', {'form': form})


class UserLoginView(LoginView):
    """Sign in. Honours a safe ?next= URL, otherwise goes to the dashboard."""
    template_name = 'usermanagement/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True
    next_page = reverse_lazy('core:dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Welcome back, {form.get_user().username}!')
        return response


class UserLogoutView(LogoutView):
    """Sign out (POST only, as Django requires) and return to the login page."""
    next_page = reverse_lazy('usermanagement:login')
