from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'IT Administrator'),
        ('MANAGER', 'Warehouse Manager'),
        ('CASHIER', 'Store Cashier'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='CASHIER')
    status = models.CharField(max_length=20, default='ACTIVE')

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"