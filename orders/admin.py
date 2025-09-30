from django.contrib import admin
from .models import Order, OrderItem

# ✅ Inline for OrderItem
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    fields = ('product', 'quantity', 'unit_price', 'line_total')
    readonly_fields = ('line_total',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer', 'status', 'total_amount', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('customer__name', 'order_number')
    ordering = ('-created_at',)
    list_per_page = 20

    # ✅ Add OrderItem inline
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):   
    list_display = ('order', 'product', 'quantity')
    search_fields = ('order__order_number', 'product__name')
    ordering = ('-order__created_at',)
    list_per_page = 20


