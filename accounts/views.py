from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.http import require_POST
from .forms import LoginForm, RegistrationForm
from .models import DeviceLog
from attendance.models import Attendance

def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user:
                # Check device fingerprint
                if user.device_fingerprint:
                    if not user.check_device_fingerprint(request):
                        messages.error(request, 'Access denied: new device not registered.')
                        return render(request, 'accounts/login.html', {'form': form})
                else:
                    # First login, set fingerprint
                    user.set_device_fingerprint(request)
                    DeviceLog.objects.create(user=user, device_fingerprint=user.device_fingerprint)

                login(request, user)
                Attendance.objects.create(user=user)
                messages.success(request, f'Welcome back, {user.email}!')
                return redirect('core:home')
            else:
                messages.error(request, 'Invalid email or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in immediately after registration
            login(request, user)
            # Set device fingerprint for first login
            user.set_device_fingerprint(request)
            DeviceLog.objects.create(user=user, device_fingerprint=user.device_fingerprint)
            # Log attendance
            Attendance.objects.create(user=user)
            messages.success(request, f'Welcome to Weekend 🌟 Events, {user.email}!')
            return redirect('core:home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

@require_POST
def logout_view(request):
    logout(request)
    return redirect('accounts:login')
