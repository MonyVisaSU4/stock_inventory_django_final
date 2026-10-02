from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('products/', views.product_list_view, name='product-list'),
    path('transfer/', views.stock_transfer_view, name='transfer'),
    path('checkout/', views.stock_checkout_view, name='checkout'),
    path('intake/', views.stock_intake_view, name='intake'),
    path('logs/', views.inventory_logs_view, name='logs'),
]
