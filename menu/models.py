from django.db import models


class Product(models.Model):
    """Menu items that customers can order (burgers, pizzas, drinks, etc.)"""
    
    # Basic product information
    name = models.CharField(max_length=100)                                # Product name (like "Cheeseburger")
    sku = models.CharField(max_length=50, unique=True)                     # Product code (like "BURGER001")
    category = models.CharField(max_length=100)                            # Category (like "Burgers", "Drinks", "Desserts")
    
    # Pricing information
    price = models.DecimalField(max_digits=10, decimal_places=2)           # Base price (like 12.99)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # Tax percentage (like 8.5 for 8.5%)
    
    # Additional details
    description = models.TextField(blank=True, null=True)                  # Description of the item (optional)
    is_active = models.BooleanField(default=True)                          # Is this item available to order?
    
    def get_price_with_tax(self):
        """Calculate final price including tax"""
        return self.price * (1 + self.tax_rate / 100)
    
    def __str__(self):
        """Show product info when displaying in admin or forms"""
        return f"{self.name} - ${self.price}"
    
    class Meta:
        """Make queries faster when filtering by category and availability"""
        indexes = [models.Index(fields=["category", "is_active"])]