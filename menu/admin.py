from django.contrib import admin

# Register your models here.
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'category', 'price', 'tax_rate', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'sku', 'category')
    ordering = ('name',)
    list_per_page = 20