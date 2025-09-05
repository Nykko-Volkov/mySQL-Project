from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00) # tax rate as percentage
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        indexes = [models.Index(fields=["category","is_active"]      )] # to optimize queries filtering by category and is_active]
    def __str__(self):
        return f"{self.name} ({self.sku}) - ${self.price}"