from django import forms
from .models import Staff
    # user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='staff_profile')
    # role = models.ForeignKey(StaffRole, on_delete=models.PROTECT,related_name='staff_members',default=1)
    # gender = models.CharField(max_length=1, choices=GENDER,blank=True, null=True)
    # hired_on = models.DateField(auto_now_add=True,blank=True, null=True)
    # is_active = models.BooleanField(default=True)
    # def __str__(self):
    #     return f"{self.user.username} - {self.role.name}"

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['user', 'role','gender', 'is_active'] # Exclude 'hired_on' as it's auto-set

