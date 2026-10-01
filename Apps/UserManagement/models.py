from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrator'
        CUSTOMER = 'CUSTOMER', 'Customer'

    role = models.CharField(max_length=10 ,choices=Role, default=Role.CUSTOMER)

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    @property
    def is_customer(self):
        return self.role == self.Role.CUSTOMER