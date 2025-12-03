from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('my-location/', views.my_location_view, name='my_location'),
]