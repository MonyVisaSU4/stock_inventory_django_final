from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        STAFF = "STAFF", "Staff"

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        INACTIVE = "INACTIVE", "Inactive"

    id = models.BigAutoField(primary_key=True)

    username = models.CharField(
        max_length=150,
        unique=True
    )

    email = models.EmailField(
        unique=True
    )

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STAFF
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()