from django.urls import path

from . import views

urlpatterns  = [
    path('payments/<int:id>', views.selectPayment, name='payment'),
]