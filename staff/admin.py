from django.contrib import admin
from .models import StaffRole, staff
# Register your models here.

@admin.register(StaffRole)
class StaffRoleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
    list_per_page = 20

@admin.register(staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    