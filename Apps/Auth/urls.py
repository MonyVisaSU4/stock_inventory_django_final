from django.urls import path

from Apps.Auth import views

app_name = 'auth'

urlpatterns = [
    path('/login', views.login_view, name='login'),
    path('/logout', views.logout_view, name='logout'),
    path('/register', views.register, name='register'),
    path('/verify-email', views.verify_email, name='verify-email'),
    path('/verify-otp', views.otp, name='otp'),
    path('/done', views.done_verify, name='done')
]