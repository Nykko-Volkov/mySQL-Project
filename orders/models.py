from django.db import models
from django.conf import settings
from customers.models import Customer, DiningTable
from menu.models import Product


class Order(models.Model):
    """Simple order model for restaurant orders - supports both member and walk-in customers"""
    
    # Order type choices - how customer wants the order
    ORDER_TYPE = (
        ("DINE_IN", "Dine In"),      # Customer eats at restaurant
        ("TAKEAWAY", "Takeaway"),    # Customer takes food home
        ("DELIVERY", "Delivery")     # Food delivered to customer
    )
    
    # Order status choices - current state of order
    STATUS = (
        ("PENDING", "Pending"),          # Order just placed
        ("IN_PROGRESS", "In Progress"),  # Kitchen is preparing
        ("COMPLETED", "Completed"),      # Order ready/delivered
        ("CANCELLED", "Cancelled")       # Order was cancelled
    )
    
    # Basic order information
    order_number = models.IntegerField(unique=True, default=1000)  # Unique number for each order
    
    # Customer information - can be registered customer OR walk-in
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)  # Registered customer (optional)
    customer_name = models.CharField(max_length=100, blank=True)  # Walk-in customer name
    customer_phone = models.CharField(max_length=15, blank=True)  # Walk-in customer phone
    
    # Table and service details
    table = models.ForeignKey(DiningTable, on_delete=models.SET_NULL, null=True, blank=True)  # Which table (if dine-in)
    order_type = models.CharField(max_length=20, choices=ORDER_TYPE)  # Dine-in, takeaway, or delivery
    status = models.CharField(max_length=20, choices=STATUS, default="PENDING")  # Current order status
    
    # Staff and timing
    placed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)  # Which staff took order
    created_at = models.DateTimeField(auto_now_add=True)  # When order was created
    updated_at = models.DateTimeField(auto_now=True)  # When order was last updated
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Total cost
    
    def get_customer_name(self):
        """Get customer name - either from registered customer or walk-in name"""
        if self.customer:  # If registered customer
            return self.customer.name
        elif self.customer_name:  # If walk-in customer
            return self.customer_name
        else:  # If no customer info
            return "Walk-in Customer"
    
    def get_customer_phone(self):
        """Get customer phone - either from registered customer or walk-in phone"""
        if self.customer:  # If registered customer
            return self.customer.phone
        elif self.customer_phone:  # If walk-in customer
            return self.customer_phone
        else:  # If no phone info
            return "No phone"
    
    def calculate_total(self):
        """Calculate total amount from all order items"""
        return sum(item.line_total or 0 for item in self.items.all())
    
    def __str__(self):
        """Show order as: Order 1001 - John Doe - Pending"""
        return f"Order {self.order_number} - {self.get_customer_name()} - {self.status}"
    
    class Meta:
        """Optimize queries by status, order type, and creation date."""
        indexes = [models.Index(fields=["status", "order_type", "created_at"])]


class OrderItem(models.Model):
    """Each item in an order - like "2x Burger" or "1x Pizza" """
    
    # Which order this item belongs to
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    
    # Which menu item was ordered
    product = models.ForeignKey(Product, on_delete=models.PROTECT)  # Don't delete products that were ordered
    
    # How many of this item
    quantity = models.PositiveIntegerField()  # Must be 1 or more
    
    # Price when ordered (saves historical pricing)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Price per item
    line_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Total for this line
    
    def save(self, *args, **kwargs):
        """Automatically calculate prices when saving"""
        # If no unit price set, use current product price
        if not self.unit_price:
            self.unit_price = self.product.price
            
        # Calculate total for this line (quantity × price)
        self.line_total = self.quantity * self.unit_price
        
        # Save to database
        super().save(*args, **kwargs)
    
    def __str__(self):
        """Show as: 2x Burger @ $10.00 each"""
        return f"{self.quantity}x {self.product.name} @ ${self.unit_price} each"