from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path('new/', views.create_order, name='create_order'),
    # Add more paths as needed
]