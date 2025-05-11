from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST, require_http_methods

from real_estates.views import fetchNotifications
from .models import Payment
from real_estates.models import Offer

# Create your views here.

# Create your views here.


def payment(request):
    offer = Offer.objects.get(id=request.POST.get("offer-id"))
    
    payment_option = request.POST.get("payment-option")

    Payment.objects.create(
        offer = offer,
        payment_option = payment_option
    )
    return redirect('profile')

      