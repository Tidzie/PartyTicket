from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from .models import Message
from accounts.models import User

@login_required
def message_list(request):
    messages = Message.objects.filter(target_users=request.user).order_by('-created_at')
    return render(request, 'messaging/message_list.html', {'messages': messages})

class MessageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label='Message Content')
    target_users = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(role='user'),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Target Users (leave empty for broadcast)'
    )
    is_broadcast = forms.BooleanField(required=False, label='Broadcast to all users')

@login_required
def message_send(request):
    if request.user.role != 'admin':
        return redirect('core:home')
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            target_users = form.cleaned_data['target_users']
            is_broadcast = form.cleaned_data['is_broadcast']
            if is_broadcast:
                target_users = User.objects.filter(role='user')
            message = Message.objects.create(
                sender=request.user,
                content=content,
                is_broadcast=is_broadcast
            )
            message.target_users.set(target_users)
            messages.success(request, 'Message sent successfully.')
            return redirect('messaging:message_list')
    else:
        form = MessageForm()
    return render(request, 'messaging/message_send.html', {'form': form})
