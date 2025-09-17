from django.db import models

# # Create your models here.
from django.conf import settings

class StaffRole(models.Model):
    name = models.CharField(max_length=100)
    roles_options = (
        ('MANAGER', 'Manager'), 
        ('CHEF', 'Chef'), 
        ('WAITER', 'Waiter'), 
        ('CLEANER', 'Cleaner'),
        ('CASHIER', 'Cashier')
    )
    role = models.CharField(max_length=20, choices=roles_options, default='WAITER')

    GENDER  = (("M","Male"),("F","Female"))
    gender = models.CharField(max_length=1, choices=GENDER,blank=True, null=True)
    hired_on = models.DateField(auto_now_add=True,blank=True, null=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.name} - {self.role}"
    
