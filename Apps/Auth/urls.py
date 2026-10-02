from django.urls import path

from Apps.Auth import views

app_name = 'auth'

urlpatterns = [
    path('login/', views.login, name='login'),
]