from django.shortcuts import HttpResponse
from django.views.decorators.http import require_POST, require_http_methods

from real_estates.views import fetchNotifications, notify
from .models import Payment
from real_estates.models import Offer

# Create your views here.

      
@require_POST
@fetchNotifications
def selectPayment(request, id):
    offer = Offer.objects.get(id=id)
    offer.offer_status = "PROCESSED" 
    notify(user=offer.property.seller.user, offer=offer)
    offer.save()
    payment_option = request.POST["payment-option"]

    Payment.objects.create(
        offer = offer,
        payment_option = payment_option
    )
    return HttpResponse(200)
