from django.shortcuts import render
from .models import Staff

def staff_list(request):
	staff_members = Staff.objects.all()
	return render(request, 'staff_list.html', {'staff_members': staff_members})
