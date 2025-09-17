from django.shortcuts import render, redirect
from .models import StaffRole
from .forms import StaffForm

def staff_list(request):
	staff_members = StaffRole.objects.all()
	if request.method == 'POST':
		form = StaffForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('staff_list')
	else:
		form = StaffForm()

	return render(request, 'staff_list.html', {'staff_members': staff_members, 'form': form})
	

def staff_edit(request, staff_id):
	staff_member = StaffRole.objects.get(id=staff_id)
	if request.method == 'POST':
		form = StaffForm(request.POST, instance=staff_member)
		if form.is_valid():
			form.save()
			return redirect('staff_list')
	else:
		form = StaffForm(instance=staff_member)
	return render(request, 'staff_edit.html', {'form': form, 'staff_member': staff_member})

def staff_delete(request, staff_id):
	staff_member = StaffRole.objects.get(id=staff_id)
	if request.method == 'POST':
		staff_member.delete()
		return redirect('staff_list')
	return render(request, 'staff_delete_confirm.html', {'staff_member': staff_member})