from django.urls import path

from . import views

app_name = 'auth'

urlpatterns = [
    path('', views.CustomLoginView, name='login'),
    path('/register', views.register, name='register'),
]