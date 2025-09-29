from django.db import models
from django.conf import settings
from customers.models import Customer, DiningTable
from menu.models import Product

# Create your models here.
class Order(models.Model):
    ORDER_TYPE = (("DINE_IN","Dine In"),("TAKEAWAY","Takeaway"),("DELIVERY","Delivery"))
    STATUS = (("PENDING","Pending"),("IN_PROGRESS"," In Progress"),("COMPLETED","Completed"),("CANCELLED","Cancelled"))
    order_number = models.IntegerField(unique=True) 
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    table = models.ForeignKey(DiningTable, on_delete=models.SET_NULL, null=True, blank=True)
    order_type = models.CharField(max_length=20, choices=ORDER_TYPE)
    status = models.CharField(max_length=20, choices=STATUS, default="PENDING")
    placed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    class Meta:
        indexes = [models.Index(fields=["status","order_type","created_at"])]

    def __str__(self):
        return f"Order {self.id} - {self.status} - {self.order_type}"
        def total_amount(self):
            return sum(item.line_total for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    line_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    def __str__(self):
        return f"{self.quantity} x {self.product.name} @ {self.unit_price} each"
    

    
class Payment(models.Model):
    PAYMENT_METHODS = (("CASH","Cash"),("CARD","Card"),("ONLINE","Online"))
    STAUS = (("PENDING","Pending"),("COMPLETED","Completed"),("FAILED","Failed"))
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, choices=STAUS, default="PENDING")
    txn_id = models.CharField(max_length=100, blank=True, null=True)
    paid_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Payment of {self.amount} for Order {self.order.id} via {self.method}"
    
   
