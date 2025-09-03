from django.db import models

# # Create your models here.
# from django.conf import settings

# class StaffProfile(models.Model):
#     name = models.CharField(max_length=100,unique=True)
#     def __str__(self):
#         return self.name
    

# class staff (models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     role = models.ForeignKey('accounts.User.Role', on_delete=models.CASCADE)
#     gender = models.CharField(max_length=10)
#     shift_time = models.CharField(max_length=50)
#     contact_number = models.CharField(max_length=15)
#     hire_date = models.DateField(auto_now_add=True)
#     is_active = models.BooleanField(default=True)

#     def __str__(self):
#         return f"{self.user.username} - {self.profile.name}"