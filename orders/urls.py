from django.urls import path
from . import views

urlpatterns = [
    path('new/', views.create_order, name='create_order'),
    # Add more paths as needed
]