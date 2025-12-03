from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
import hashlib

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, role='user', **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        # Remove fields handled by PermissionsMixin
        extra_fields.pop('is_staff', None)
        extra_fields.pop('is_superuser', None)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    device_fingerprint = models.CharField(max_length=128, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def set_device_fingerprint(self, request):
        # Simple fingerprint: hash of IP + User-Agent
        ip = self.get_client_ip(request)
        ua = request.META.get('HTTP_USER_AGENT', '')
        fingerprint = f"{ip}:{ua}"
        self.device_fingerprint = hashlib.sha256(fingerprint.encode()).hexdigest()
        self.save()

    def check_device_fingerprint(self, request):
        ip = self.get_client_ip(request)
        ua = request.META.get('HTTP_USER_AGENT', '')
        fingerprint = f"{ip}:{ua}"
        return self.device_fingerprint == hashlib.sha256(fingerprint.encode()).hexdigest()

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def __str__(self):
        return self.email

class DeviceLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device_fingerprint = models.CharField(max_length=128)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.email} - {self.device_fingerprint} - {self.timestamp}"
