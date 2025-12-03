from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from events.models import Event
from accounts.models import User
from messaging.models import Message
from attendance.models import Attendance
from django.db.models import Count
from django.utils import timezone

def home(request):
    # Get the next upcoming event
    next_event = Event.objects.filter(is_active=True, date__gte=timezone.now().date()).order_by('date', 'time').first()
    upcoming_events = Event.objects.filter(is_active=True).order_by('date')[:3]
    return render(request, 'core/home.html', {
        'next_event': next_event,
        'upcoming_events': upcoming_events
    })

@login_required
def contact(request):
    return render(request, 'core/contact.html')

@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('core:home')
    users = User.objects.all()
    events = Event.objects.all()
    messages = Message.objects.all()
    attendances = Attendance.objects.all()
    user_count = users.count()
    event_count = events.count()
    message_count = messages.count()
    attendance_count = attendances.count()
    return render(request, 'admin/dashboard.html', {
        'users': users,
        'events': events,
        'messages': messages,
        'attendances': attendances,
        'user_count': user_count,
        'event_count': event_count,
        'message_count': message_count,
        'attendance_count': attendance_count,
    })

def my_location_view(request):
    return render(request, "core/mylocation.html")
