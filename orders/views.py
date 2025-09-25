from django.shortcuts import render, redirect
from .forms import OrderForm, OrderItemForm
from .models import Order, OrderItem
# Create your views here.


def create_order(request):
    if request.method == "POST":
        order_form = OrderForm(request.POST)
        order_item_form = OrderItemForm(request.POST)

        if order_form.is_valid() and order_item_form.is_valid():
            order = order_form.save()
            order_item = order_item_form.save(commit=False)
            order_item.order = order
            # Auto-fill price & total
            order_item.unit_price = order_item.product.price
            order_item.line_total = order_item.quantity * order_item.unit_price
            order_item.save()
            return redirect("/")  # stay on same page
    else:
        order_form = OrderForm()
        order_item_form = OrderItemForm()

    return render(
        request,
        "orders/create_order.html",
        {"order_form": order_form, "item_form": order_item_form},
    )



def order_list(request):
    all_orders = Order.objects.all().order_by('-created_at')
    return render(request, "orders/order_list.html", {"orders": all_orders})


def change_status(request):
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        new_status = request.POST.get("new_status")
        try:
            order = Order.objects.get(id=order_id)
            order.status = new_status
            order.save()
        except Order.DoesNotExist:
            pass  # Handle error as needed
    return redirect("orders:order_list")