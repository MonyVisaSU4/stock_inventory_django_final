from django.shortcuts import render
from pyexpat.errors import messages
from django.contrib.auth.views import LoginView

from .forms import LoginForm

# Create your views here.
def CustomLoginView(LoginView):
    template_name = 'usermanagement/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, f"Welcome back, {form.get_user().get_full_name() or form.get_user().username}!")
        return super().form_valid(form)

def register(request):
    return render(request, 'userManagement/register.html')