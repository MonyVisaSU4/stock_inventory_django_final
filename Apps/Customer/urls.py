from django.urls import path

from . import views

app_name = 'customer'

urlpatterns = [
    path('', views.product_list, name='list'),
    path('/id', views.product_detail, name='detail'),
]