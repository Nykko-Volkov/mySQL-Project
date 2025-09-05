from django.contrib import admin

# Register your models here.
from .models import Customer,DiningTable,Reservation

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'address', 'date_of_birth', 'arrival_time', 'leaving_time', 'created_at')
    search_fields = ('name', 'email', 'phone')
    ordering = ('name',)
    list_per_page = 20
    
@admin.register(DiningTable)    
class DiningTableAdmin(admin.ModelAdmin):
    list_display = ('table_number', 'capacity', 'is_available')
    list_filter = ('is_available',)
    search_fields = ('table_number',)
    ordering = ('table_number',)
    list_per_page = 20  


@admin.register(Reservation)    
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('customer', 'table', 'reservation_time', 'number_of_guests', 'special_requests', 'created_at')
    list_filter = ('reservation_time',)
    search_fields = ('customer__name', 'table__table_number')
    ordering = ('-reservation_time',)
    list_per_page = 20
