from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """User accounts for staff to login to the restaurant system"""
    
    class Role(models.TextChoices):
        """Different permission levels for staff"""
        ADMIN = 'ADMIN', 'Admin'         # Can do everything
        MANAGER = 'MANAGER', "Manager"   # Can manage orders and staff
        CASHIER = 'CASHIER', 'Cashier'   # Can take orders and payments
        STAFF = 'STAFF', 'Staff'         # Basic access
    
    # Each user has a role that determines what they can do
    role = models.CharField(max_length=10, choices=Role.choices)
    
    def __str__(self):
        """Show username and role when displaying in admin"""
        return f"{self.username} : {self.role}"
