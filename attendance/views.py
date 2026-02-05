from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from employees.models import Employee
from .models import Attendance
from .forms import AttendanceForm
from datetime import datetime, timedelta
import calendar
from django.http import JsonResponse


def view_attendance(request, id):
    employee = get_object_or_404(Employee, id=id)
    attendance_records = Attendance.objects.filter(employee=employee).order_by('-date')
    return render(request, 'attendance/list.html', {
        'employee': employee,
        'attendance_records': attendance_records
    })

def weekly_attendance(request):
    # Get filter parameters
    department = request.GET.get('department', '')
    employee_id = request.GET.get('employee_id', '')
    year = request.GET.get('year')
    month = request.GET.get('month')
    week_offset = int(request.GET.get('week_offset', 0))
    
    # Calculate current week dates
    today = datetime.now().date()
    
    # If year and month provided, use them; otherwise use current
    if year and month:
        try:
            base_date = datetime(int(year), int(month), 1).date()
        except (ValueError, TypeError):
            base_date = today.replace(day=1)
    else:
        base_date = today
    
    # Calculate week start (Monday) and end (Sunday)
    # Adjust for week offset
    current_week_start = base_date - timedelta(days=base_date.weekday()) + timedelta(weeks=week_offset)
    week_dates = [current_week_start + timedelta(days=i) for i in range(7)]
    
    # Get all departments for filter dropdown
    departments = Employee.objects.values_list('department', flat=True).distinct().order_by('department')
    
    # Build employee query
    employees_query = Employee.objects.all()
    if department:
        employees_query = employees_query.filter(department=department)
    if employee_id:
        employees_query = employees_query.filter(
            Q(employee_id__icontains=employee_id) | 
            Q(full_name__icontains=employee_id)
        )
    
    employees = employees_query.order_by('full_name')
    
    # Get attendance data for the week
    # Structure: {employee_id: {date_string: status}}
    attendance_data = {}
    for employee in employees:
        employee_id_str = str(employee.id)
        attendance_data[employee_id_str] = {}
        for date in week_dates:
            date_str = date.strftime('%Y-%m-%d')
            try:
                record = Attendance.objects.get(employee=employee, date=date)
                attendance_data[employee_id_str][date_str] = record.status
            except Attendance.DoesNotExist:
                attendance_data[employee_id_str][date_str] = None

    
    # Calculate previous and next week offsets
    prev_week_offset = week_offset - 1
    next_week_offset = week_offset + 1
    
    # Get current month calendar for date picker
    current_month_calendar = calendar.Calendar()
    month_days = current_month_calendar.monthdayscalendar(base_date.year, base_date.month)
    
    context = {
        'week_dates': week_dates,
        'employees': employees,
        'attendance_data': attendance_data,
        'departments': departments,
        'selected_department': department,
        'selected_employee_id': employee_id,
        'current_year': base_date.year,
        'current_month': base_date.month,
        'current_month_name': base_date.strftime('%B'),
        'today': today,
        'prev_week_offset': prev_week_offset,
        'next_week_offset': next_week_offset,
        'week_offset': week_offset,
        'month_days': month_days,
        'years': range(2020, 2031),  # Year range for selector
    }
    
    return render(request, 'attendance/weekly.html', context)

def mark_bulk_attendance(request):
    if request.method == 'POST':
        # Check if this is an AJAX request for individual cell update
        employee_id = request.POST.get('employee_id')
        date_str = request.POST.get('date')
        status = request.POST.get('status')
        
        # Handle bulk selection from checkboxes
        bulk_status = request.POST.get('bulk_status')
        employee_ids = request.POST.get('employee_ids')
        bulk_date = request.POST.get('bulk_date')
        
        # Individual cell update (AJAX)
        if employee_id and date_str and status is not None:
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
                employee = Employee.objects.get(id=employee_id)
                
                if status == '':
                    # Delete attendance record if status is empty
                    Attendance.objects.filter(employee=employee, date=date).delete()
                else:
                    # Update or create attendance record
                    Attendance.objects.update_or_create(
                        employee=employee,
                        date=date,
                        defaults={'status': status}
                    )
                
                # Return JSON response for AJAX
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': True})
                return redirect('weekly_attendance')
            except (ValueError, Employee.DoesNotExist):
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'error': 'Invalid data'})
                pass
        
        # Bulk update from checkboxes
        elif bulk_status is not None and employee_ids and bulk_date:
            try:
                date = datetime.strptime(bulk_date, '%Y-%m-%d').date()
                ids = employee_ids.split(',')
                
                for emp_id in ids:
                    try:
                        employee = Employee.objects.get(id=emp_id)
                        if bulk_status == '':
                            Attendance.objects.filter(employee=employee, date=date).delete()
                        else:
                            Attendance.objects.update_or_create(
                                employee=employee,
                                date=date,
                                defaults={'status': bulk_status}
                            )
                    except Employee.DoesNotExist:
                        continue
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': True})
                return redirect('weekly_attendance')
            except (ValueError, Employee.DoesNotExist):
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'error': 'Invalid data'})
                pass
    
    return redirect('weekly_attendance')
