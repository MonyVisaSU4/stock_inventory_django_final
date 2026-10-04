"""
URL configuration for StockInventory project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Core.urls')),
    path('auth', include('Apps.Auth.urls'))
]
