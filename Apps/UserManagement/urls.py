from django.urls import path

from . import views

app_name = 'usermanagement'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('register/', views.register_view, name='register'),
]
