from django.urls import path

from Apps.Inventory import views

app_name = 'shop'

urlpatterns = [
    path('', views.shop_list, name='list'),
    path('/detail', views.shop_detail, name='detail'),
]
