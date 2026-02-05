from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Employee
from .forms import EmployeeForm

def employee_list(request):

    employees = Employee.objects.all()
    return render(request, 'employees/list.html', {'employees': employees})

def employee_add(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'employees/add.html', {'form': form})

def employee_edit(request, id):
    employee = get_object_or_404(Employee, id=id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employees/edit.html', {'form': form})

def employee_delete(request, id):
    employee = get_object_or_404(Employee, id=id)
    deleted_employee_id = employee.employee_id
    employee.delete()
    messages.success(request, f'Employee {deleted_employee_id} has been deleted. ID {deleted_employee_id} is now available for reassignment.')
    return redirect('employee_list')

def check_employee_id(request):
    """AJAX endpoint to check if employee ID is available"""
    employee_id = request.GET.get('employee_id', '')
    exists = Employee.objects.filter(employee_id=employee_id).exists()
    return render(request, 'employees/check_id.html', {
        'employee_id': employee_id,
        'exists': exists,
        'available': not exists
    })

def get_available_ids(request):
    """View to show all used and suggest available employee IDs"""
    used_ids = list(Employee.objects.values_list('employee_id', flat=True).order_by('employee_id'))
    
    # Generate suggestions for new IDs
    suggestions = []
    if used_ids:
        # Try to find gaps in numeric IDs
        numeric_ids = []
        for eid in used_ids:
            try:
                numeric_ids.append(int(eid))
            except ValueError:
                pass
        
        if numeric_ids:
            max_id = max(numeric_ids)
            # Suggest next 5 available IDs
            for i in range(1, 6):
                suggestions.append(str(max_id + i))
    
    return render(request, 'employees/available_ids.html', {
        'used_ids': used_ids,
        'suggestions': suggestions,
        'total_employees': len(used_ids)
    })
