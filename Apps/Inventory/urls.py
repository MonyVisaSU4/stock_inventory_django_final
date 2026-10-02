from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('products/', views.product_list_view, name='product-list'),
    path('products/add/', views.product_add_view, name='product-add'),
    path('products/<int:product_id>/edit/', views.product_edit_view, name='product-edit'),
    path('products/<int:product_id>/delete/', views.product_delete_view, name='product-delete'),
    path('transfer/', views.stock_transfer_view, name='transfer'),
    path('checkout/', views.stock_checkout_view, name='checkout'),
    path('intake/', views.stock_intake_view, name='intake'),
    path('logs/', views.inventory_logs_view, name='logs'),
]
