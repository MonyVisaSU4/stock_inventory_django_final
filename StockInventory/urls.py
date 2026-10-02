"""
URL configuration for StockInventory project.
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Apps.Inventory.urls')),
    path('', include('Apps.Auth.urls')),
    path('core/', include('Core.urls')),
]
