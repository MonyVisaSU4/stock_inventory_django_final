from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

User = get_user_model()


class RegisterForm(UserCreationForm):
    """Public sign-up form.

    Password hashing, the two-password match check and the project's
    AUTH_PASSWORD_VALIDATORS are all handled by UserCreationForm.
    The `role` field is deliberately NOT exposed: every self-registered
    account is a CUSTOMER, so nobody can sign themselves up as an admin.
    """

    email = forms.EmailField(
        required=True,
        help_text='We will use this to contact you about your account.',
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'username': 'Choose a username',
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'you@example.com',
            'password1': 'Create a password',
            'password2': 'Repeat the password',
        }
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = placeholders.get(name, '')
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['username'].widget.attrs['autofocus'] = True

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.CUSTOMER  # never trust the client with the role
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    """Sign-in form: Django's AuthenticationForm with Bootstrap styling."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Your username',
            'autofocus': True,
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Your password',
        })
