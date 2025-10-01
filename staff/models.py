from django.db import models
from datetime import date


class StaffRole(models.Model):
    """Restaurant staff members and their job roles"""
    
    # Available job roles in the restaurant
    ROLES_OPTIONS = (
        ('MANAGER', 'Manager'),      # Manages restaurant operations
        ('CHEF', 'Chef'),            # Cooks food in kitchen
        ('WAITER', 'Waiter'),        # Serves customers, takes orders
        ('CLEANER', 'Cleaner'),      # Keeps restaurant clean
        ('CASHIER', 'Cashier')       # Handles payments
    )
    
    # Gender options (optional information)
    GENDER_CHOICES = (("M", "Male"), ("F", "Female"))
    
    # Basic staff information
    name = models.CharField(max_length=100)                                # Staff member's full name
    role = models.CharField(max_length=20, choices=ROLES_OPTIONS, default='WAITER')  # Their job role
    
    # Optional personal information  
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)  # Gender (optional)
    
    # Employment information
    hired_on = models.DateField(auto_now_add=True, blank=True, null=True)  # Date they were hired
    is_active = models.BooleanField(default=True)                          # Are they currently working?
    
    def get_years_of_service(self):
        """Calculate how many years they've been working here"""
        if not self.hired_on:
            return 0
        today = date.today()
        return today.year - self.hired_on.year - ((today.month, today.day) < (self.hired_on.month, self.hired_on.day))
    
    def __str__(self):
        """Show staff info when displaying in admin or forms"""
        return f"{self.name} - {self.role}"
    
