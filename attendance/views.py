from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Attendance
import csv

@login_required
def attendance_list(request):
    if request.user.role != 'admin':
        return redirect('core:home')
    attendances = Attendance.objects.all().order_by('-timestamp')
    return render(request, 'attendance/attendance_list.html', {'attendances': attendances})

@login_required
def attendance_export(request):
    if request.user.role != 'admin':
        return redirect('core:home')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="attendance.csv"'
    writer = csv.writer(response)
    writer.writerow(['User', 'Timestamp'])
    for attendance in Attendance.objects.all().order_by('-timestamp'):
        writer.writerow([attendance.user.email, attendance.timestamp])
    return response
