from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import OrderForm, OrderItemFormSet
from .models import Order
from menu.models import Product
from django.http import JsonResponse, HttpResponseBadRequest

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
            # Show validation errors to the user so they can fix input
            # collect non-field and field errors from both forms
            form_errors = []
            if order_form.errors:
                form_errors.append(order_form.errors.as_json())
            if formset.errors:
                form_errors.append(str(formset.errors))
            messages.error(request, 'There were errors with the order form. Please correct them and try again.')
            # fall through to re-render the page with the invalid forms
    else:
        # Create empty forms for GET request
        order_form = OrderForm()
        formset = OrderItemFormSet()

    return render(request, 'orders/create_order.html', {
        'order_form': order_form,
        'formset': formset,
        'products': Product.objects.all()  # All products for adding items

    })



def order_list(request):
    """Show all orders, newest first"""
    # Support POST to change status from inline forms that post to the same URL
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('new_status')
        if order_id and new_status:
            try:
                order = Order.objects.get(id=order_id)
                order.status = new_status
                order.save()
                messages.success(request, f'Order #{order.order_number} status updated to {new_status}.')
            except Order.DoesNotExist:
                messages.error(request, 'Order not found.')
        else:
            # Not a recognized POST for this view
            return HttpResponseBadRequest('Invalid request')
        return redirect('orders:order_list')

    all_orders = Order.objects.all().order_by('-created_at')  # Newest orders first
    all_products = Product.objects.all()  # All products for adding items
    return render(request, "orders/order_list.html", {"orders": all_orders, "products": all_products})


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





def add_item_to_order(request):
    """Add an item to an existing order via AJAX (expects X-Requested-With header)

    Request must be POST and have headers['x-requested-with'] == 'XMLHttpRequest'
    """
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if request.method == "POST" and is_ajax:
        order_id = request.POST.get("order_id")        # Which order to update
        product_id = request.POST.get("product_id")    # Which product to add
        try:
            quantity = int(request.POST.get("quantity", 1))  # How many (default 1)
        except (TypeError, ValueError):
            quantity = 1

        try:
            order = Order.objects.get(id=order_id)         # Find the order
            product = Product.objects.get(id=product_id)    # Find the product

            # Create new order item
            from .models import OrderItem  # Import here to avoid circular import
            order_item = OrderItem(order=order, product=product, quantity=quantity)
            order_item.save()  # Prices will be calculated automatically

            return JsonResponse({
                "success": True,
                "message": f'Added {quantity} x {product.name} to Order #{order.order_number}.'
            })
        except (Order.DoesNotExist, Product.DoesNotExist):
            return JsonResponse({"success": False, "message": "Order or Product not found."})

    return JsonResponse({"success": False, "message": "Invalid request."})