from django.urls import path

from Apps.Stock import views

app_name = 'stock'

urlpatterns = [
    path('', views.list, name='list'),
    path('/movement', views.movement, name='movement'),
    path('/take', views.take, name='take'),
]
