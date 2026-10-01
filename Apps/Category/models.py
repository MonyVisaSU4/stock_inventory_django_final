from django.db import models

# Create your models here.
class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Categories"