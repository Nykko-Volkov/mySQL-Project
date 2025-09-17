from django.shortcuts import render, redirect
from .forms import OrderForm, OrderItemForm
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
            return redirect("create_order")  # stay on same page
    else:
        order_form = OrderForm()
        order_item_form = OrderItemForm()

    return render(
        request,
        "orders/create_order.html",
        {"order_form": order_form, "item_form": order_item_form},
    )
