from django.shortcuts import render
from .models import Product

def menu_list(request):
	products = Product.objects.all()
	return render(request, 'menu_list.html', {'products': products})
