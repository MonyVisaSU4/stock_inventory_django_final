from django.urls import path
from . import views

app_name = 'auth'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit_view, name='profile-edit'),
    path('profile/change-password/', views.change_password_view, name='change-password'),
    path('settings/', views.settings_view, name='settings'),
    path('users/', views.user_list_view, name='user-list'),
    path('users/create/', views.user_create_view, name='user-create'),
    path('users/<int:pk>/edit/', views.user_edit_view, name='user-edit'),
    path('users/<int:pk>/toggle-status/', views.user_toggle_status_view, name='user-toggle-status'),
]
