from django.shortcuts import HttpResponse
from django.views.decorators.http import require_POST

from real_estates.views import fetchNotifications, notify
from .models import Payment
from real_estates.models import Offer


# Create your views here.

      
@require_POST
@fetchNotifications
def selectPayment(request, id: int):
    offer = Offer.objects.get(id=id)

    property = offer.property
    property.status = "PROCESSED"
    property.save()
    
    offers = Offer.objects.filter(property=property)
    for of in offers:
        if of.id == id:
            of.offer_status = "PROCESSED"
        else:
            of.offer_status = "REJECTED"
        of.save()

    payment_option = request.POST["payment-option"]
    Payment.objects.create(
        offer = offer,
        payment_option = payment_option
    )
    notify(user=offer.property.seller.user, property=property)
    return HttpResponse(200)
