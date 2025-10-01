from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import OrderForm, OrderItemFormSet
from .models import Order

def create_order(request):
    """Create new order - supports both registered and walk-in customers"""
    
    if request.method == "POST":
        # Get the main order form
        order_form = OrderForm(request.POST)
        
        # Get all the order items (multiple products in one order)
        formset = OrderItemFormSet(request.POST)

        if order_form.is_valid() and formset.is_valid():
            # Save the main order first
            order = order_form.save(commit=False)
            
            # Set the staff member who created this order
            if request.user.is_authenticated:
                order.placed_by = request.user
            
            # Handle customer type logic
            customer_type = order_form.cleaned_data.get('customer_type')
            if customer_type == 'registered':
                # Keep the selected customer, clear walk-in fields
                order.customer_name = ''
                order.customer_phone = ''
            else:  # walk-in customer
                # Clear registered customer, keep walk-in fields
                order.customer = None
            
            order.save()  # Save order to database
            
            # Save all the order items
            formset.instance = order  # Connect items to this order
            formset.save()  # Prices will be calculated automatically
            
            # Show success message
            messages.success(request, f'Order #{order.order_number} created successfully!')
            return redirect('orders:order_list')
            
    else:
        # Create empty forms for GET request
        order_form = OrderForm()
        formset = OrderItemFormSet()

    return render(request, 'orders/create_order.html', {
        'order_form': order_form,
        'formset': formset,
    })



def order_list(request):
    """Show all orders, newest first"""
    all_orders = Order.objects.all().order_by('-created_at')  # Newest orders first
    return render(request, "orders/order_list.html", {"orders": all_orders})


def change_status(request):
    """Change order status (Pending -> In Progress -> Completed)"""
    if request.method == "POST":
        order_id = request.POST.get("order_id")        # Which order to update
        new_status = request.POST.get("new_status")    # New status to set
        
        try:
            order = Order.objects.get(id=order_id)     # Find the order
            order.status = new_status                  # Update status
            order.save()                               # Save to database
            messages.success(request, f'Order #{order.order_number} status updated to {new_status}')
        except Order.DoesNotExist:
            messages.error(request, 'Order not found')
            
    return redirect("orders:order_list")  # Go back to order list