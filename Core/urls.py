from django.urls import path
from Core import views as core_views
from Apps.Auth import views as auth_views

app_name = 'core'

urlpatterns = [
    path('dashboard/', core_views.dashboard, name='dashboard'),
]