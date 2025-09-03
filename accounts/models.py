from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser): # inherent all properties of AbstractUser to make custom user model
    class Role(models.TextChoices): # to create a role field with 4 choices
        ADMIN = 'ADMIN', 'Admin'
        MANAGER = 'MANAGER',"Manager"
        CASHIER = 'CASHIER', 'Cashier'
        STAFF = 'STAFF', 'Staff'
    role = models.CharField(max_length=10, choices=Role.choices) # role field with max length 10 and choices from Role class
    def __str__(self):
        return f"{self.username} : {self.role}"
