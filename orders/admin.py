from django.contrib import admin
from .models import Order, OrderItem, Payment
# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'status', 'total_amount', 'created_at', 'updated_at')
    def total_amount(self, obj):
        return obj.total_amount()
    total_amount.short_description = 'Total Amount'
    list_filter = ('status', 'created_at')
    search_fields = ('customer__name', 'id')
    ordering = ('-created_at',)
    list_per_page = 20

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):   
    list_display = ('order', 'product', 'quantity', 'unit_price', 'line_total')
    search_fields = ('order__id', 'product__name')
    ordering = ('-order__created_at',)
    list_per_page = 20

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'amount', 'method', 'status', 'paid_at')
    list_filter = ('status', 'method', 'paid_at')
    search_fields = ('order__id', 'txn_id')
    ordering = ('-paid_at',)
    list_per_page = 20
