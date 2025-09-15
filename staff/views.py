from django.shortcuts import render, redirect
from .models import Staff
from .forms import StaffForm

def staff_list(request):
	staff_members = Staff.objects.all()
	if request.method == 'POST':
		form = StaffForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('staff_list')
	else:
		form = StaffForm()
	return render(request, 'staff_list.html', {'staff_members': staff_members, 'form': form})
	