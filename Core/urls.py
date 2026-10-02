from django.urls import path

from Core import views as core_views

from Apps.UserManagement import views

app_name = 'core'

urlpatterns = [
    path('', views.CustomLoginView, name='login'),
    path('/dashboard', core_views.dashboard, name='dashboard'),
]