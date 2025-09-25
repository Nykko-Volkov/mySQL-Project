from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path('new/', views.create_order, name='create_order'),
    path('', views.order_list, name='order_list'),
    path('change_status', views.change_status, name='change_status'),
    # Add more paths as needed
]