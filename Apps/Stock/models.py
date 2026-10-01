from django.db import models

from Apps.Inventory.models import Inventory
from Apps.UserManagement.models import User


# Create your models here.
class Stock(models.Model):
    class Type(models.TextChoices):
        STOCK_IN = 'Stock In'
        STOCK_OUT = 'Stock Out'

    id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=10 ,choices=Type)
    quantity = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=100, blank=True)
    perform_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stocks')
    balance_after = models.PositiveIntegerField(default=0)

    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='stocks')