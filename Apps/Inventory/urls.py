from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.product_list_view, name='product_list'),
    path('products/<int:pk>/adjust/', views.adjust_stock_view, name='adjust_stock'),
    path('transactions/', views.transaction_list_view, name='transaction_list'),
]
