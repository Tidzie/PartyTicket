from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('', views.message_list, name='list'),
    path('send/', views.message_send, name='send'),
]
