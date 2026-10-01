from django.db import models

from Apps.Inventory.models import Inventory
from StockInventory import settings


# Create your models here.
class Customer(models.Model):
    id = models.BigAutoField(primary_key=True)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='customers'
    )

class Order(models.Model):
    id = models.BigAutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')

class OrderDetail(models.Model):
    id = models.BigAutoField(primary_key=True)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='order_details')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_details')
