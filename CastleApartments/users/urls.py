from django.urls import path
from .views import register
from .views import profile

urlpatterns = [
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
]