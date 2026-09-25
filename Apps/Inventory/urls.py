from django.urls import path

from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.inventory_list, name='list'),
    path('/detail', views.inventory_detail, name='detail'),
    path('/add', views.add_inventory, name='add'),
    path('/edit', views.edit_inventory, name='edit')
]