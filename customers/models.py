from django.db import models


class Customer(models.Model):
    """Registered customers who visit the restaurant regularly"""
    
    # Basic customer information
    name = models.CharField(max_length=100)                                # Customer's full name
    email = models.EmailField(unique=True)                                 # Email address (must be unique)
    phone = models.CharField(max_length=15, unique=True)                   # Phone number (must be unique)
    address = models.TextField()                                           # Home address
    
    # Optional information
    date_of_birth = models.DateField(null=True, blank=True)                # Birthday (optional)
    
    # Visit tracking (for restaurant analytics)
    arrival_time = models.DateTimeField(auto_now_add=True)                 # When they first registered
    leaving_time = models.DateTimeField(null=True, blank=True)             # When they left (if tracked)
    created_at = models.DateTimeField(auto_now_add=True)                   # When customer account was created

    def __str__(self):
        """Show customer name when displaying in admin or forms"""
        return self.name
    
class DiningTable(models.Model):
    """Restaurant tables where customers sit for dine-in orders"""
    
    table_number = models.CharField(max_length=10, unique=True)            # Table identifier (like "A1", "B2", "1", "2")
    capacity = models.PositiveIntegerField()                               # How many people can sit (2, 4, 6, 8, etc.)
    is_available = models.BooleanField(default=True)                       # Is table free or occupied?

    def __str__(self):
        """Show table info when displaying in admin or forms"""
        return f"Table {self.table_number} - Capacity: {self.capacity}"



class Reservation(models.Model):
    """Table bookings made by customers in advance"""
    
    # Who is making the reservation
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)       # Which registered customer
    
    # Table and timing details
    table = models.ForeignKey(DiningTable, on_delete=models.CASCADE)       # Which table to reserve
    reservation_time = models.DateTimeField()                              # When they want to come
    number_of_guests = models.PositiveIntegerField()                       # How many people coming
    
    # Optional details
    special_requests = models.TextField(blank=True, null=True)             # Any special needs (birthday, wheelchair, etc.)
    created_at = models.DateTimeField(auto_now_add=True)                   # When reservation was made

    def __str__(self):
        """Show reservation info when displaying in admin or forms"""
        return f"Reservation for {self.customer.name} at {self.reservation_time} on Table {self.table.table_number}"
    
    class Meta:
        """Prevent double-booking the same table at the same time"""
        unique_together = ('table', 'reservation_time')