"""
URL configuration for rms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include

from accounts import views as accounts_views
from dashboard import views as dashboard_views
from staff import views as staff_views
from customers import views as customers_views
from menu import views as menu_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', accounts_views.home, name='home'),
    path('signin/', accounts_views.signin, name='signin'),
    path('signup/', accounts_views.signup, name='signup'),
    path('dashboard/', dashboard_views.dashboard, name='dashboard'),
    path('staff/', staff_views.staff_list, name='staff_list'),
    path('customers/', customers_views.customer_list, name='customer_list'),
    path('menu/', menu_views.menu_list, name='menu_list'),
    path('orders/', include('orders.urls')),
]
