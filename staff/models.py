from django.db import models

# # Create your models here.
from django.conf import settings

class StaffRole(models.Model):
    name = models.CharField(max_length=100,unique=True)
    def __str__(self):
        return self.name
    

class Staff(models.Model):
    GENDER  = (("M","Male"),("F","Female"))
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='staff_profile')
    role = models.ForeignKey(StaffRole, on_delete=models.PROTECT,related_name='staff_members',default=1)
    gender = models.CharField(max_length=1, choices=GENDER,blank=True, null=True)
    hired_on = models.DateField(auto_now_add=True,blank=True, null=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.user.username} - {self.role.name}"