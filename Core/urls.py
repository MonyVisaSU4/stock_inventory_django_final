from django.urls import path

from Core import views

app_name = 'core'

urlpatterns = [
    path('', views.dashboard, name='dashboard')
]