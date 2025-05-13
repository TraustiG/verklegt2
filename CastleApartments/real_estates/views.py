from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from django.core.files.storage import default_storage
from django.db.models import Q
from django.views.decorators.http import require_http_methods, require_safe, require_POST
from django.contrib import messages
from babel.numbers import format_currency
from io import BytesIO
import base64
import json
import datetime
from .models import Property, Offer, PropertyImages
from payments.models import Payment
from users.models import Buyer, Seller, Notification

# Create your views here.

def fetchNotifications(view_func):
    def _decorated(request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                notifs = Notification.objects.filter(user=request.user, count__gt=0)
                request.user.notifications = notifs
                return view_func(request, *args, **kwargs)
            except Exception:
                pass
        return view_func(request, *args, **kwargs)

    return _decorated

@require_safe
@fetchNotifications
def index(request):
    # þarf að fa listings og tegundir og postnumer í boði

    listings = Property.objects.all()

    areas = sorted(list(set([f"{x.postal_code} {x.city}" for x in listings])))
    types = sorted(list(set([f"{x.property_type}" for x in listings])))
    prices = getPrices()
    filters = []
    for item in listings:
        item.listing_price = format_currency(item.listing_price, "", locale="is_is")[:-4]
    return render(request, "home.html", {"listings": listings, "areas": areas, "types": types, "prices": prices, "filters": filters})


@require_http_methods(["GET", "POST"])
@fetchNotifications
def getRealEstateById(request, id):
    if request.method == "GET":
        try:
            propertyObj = Property.objects.get(id=id)
        except Property.DoesNotExist:
            return redirect('real-estates')
        similars = getSimilars(propertyObj)
        images = PropertyImages.objects.filter(property=propertyObj)
        for prop in similars:
            prop.listing_price = format_currency(prop.listing_price, "", locale="is_is")[:-4]
        

        #making sure offer returns None for seller / unauthenticated users
        offer = None
        if request.user.is_authenticated:
            if request.user.is_buyer:
                offer = Offer.objects.filter(buyer=request.user.buyer, property=propertyObj).first()
                request.user.has_offer = bool(offer)

        propertyObj.listing_price = format_currency(propertyObj.listing_price, "", locale="is_is")[:-4]
        propertyObj.description = propertyObj.description.splitlines()

        return render(request, "real_estates/real_estate.html", { "property": propertyObj, "images":images, "listings": similars, "offer": offer})

    if request.method == "POST":
        propertyObj = Property.objects.get(id=id)
        if not propertyObj:
            return HttpResponse(404)
        if propertyObj.seller != request.user.seller:
            return HttpResponse(403)
        
        if request.POST["action"] == "DELETE":
            try:
                propertyObj.delete()
            except Exception:
                return HttpResponse(403)
        else:
            propertyObj = Property.objects.get(id=id)
            
            propertyObj.street_name = request.POST.get("streetname")
            propertyObj.city = request.POST.get("city_input")
            propertyObj.postal_code = request.POST.get("zip")
            propertyObj.description = request.POST.get("desc")
            propertyObj.number_of_bedrooms = request.POST.get("bedrooms")
            propertyObj.number_of_bathrooms = request.POST.get("bathrooms")
            propertyObj.square_meters = request.POST.get("sqm")
            propertyObj.property_type = request.POST.get("type")
            propertyObj.listing_price = request.POST.get("price")
            images = request.POST.get("hidden-images-list")

            createImages(images, propertyObj)
            try:
                propertyObj.save()
            except Exception:
                return HttpResponse(500)
            
        return HttpResponse(status=200)

@require_safe
@fetchNotifications
def imageGallery(request, id):
    # get realestate from database - make object to send in render
    try:
        propertyObj = Property.objects.get(id=id)
    except Property.DoesNotExist:
        return redirect('real-estates')
    
    images = PropertyImages.objects.filter(property=propertyObj)
    if request.method == "GET":
        return render(request, "real_estates/gallery.html", {"images": images})
    
@require_safe
@fetchNotifications
def search(request):
    
    listings = Property.objects.all()
    areas = sorted(list(set([f"{x.postal_code} {x.city}" for x in listings])))
    types = sorted(list(set([f"{x.property_type}" for x in listings])))
    prices = getPrices()
    filter = {"areaSelect": 300,
            "typeSelect": "Fjölbýlishús",
            "priceInput": "80000000-110000000",
            "descInput": "bjark"}
    filters = [{"name": "Bjarkissssssss", "filters": json.dumps(filter)}]

    for key in request.GET.keys():
        value = request.GET.get(key)
        if not value:
            continue
        listings = filterListings(key, value, listings)

    for item in listings:
        item.listing_price = format_currency(item.listing_price, "", locale="is_is")[:-4]

    return render(request, "home.html", {"listings": listings, "areas": areas, "types": types, "prices": prices, "filters": filters})

@require_POST
@fetchNotifications
def createOffer(request, id):
    
    amount = request.POST.get("amount")
    expiry = request.POST.get("expiry")

    propertyObj = Property.objects.get(id=id)
    buyerObj = Buyer.objects.get(user=request.user)

    #check if user has existing offer for this property, delete that first and then create the new one
    existing_offer = Offer.objects.filter(property = propertyObj , buyer=buyerObj)
    if existing_offer:
        existing_offer.delete()

    Offer.objects.create(
        property = propertyObj,
        buyer = buyerObj,
        offer_amount = amount,
        offer_expiry = expiry,
        offer_date = datetime.date.today()
    )

    notify(user=propertyObj.seller.user, prop=propertyObj)

    messages.success(request, "Tilboð hefur verið sent!")
    
    return redirect('real-estate-by-id', id=id)

@require_POST
@fetchNotifications
def deleteOffer(request, id):
    try:
        action = request.POST["action"]
    except Exception:
        return HttpResponse(403)
    offer = Offer.objects.get(id=id)
    if not offer:
        return HttpResponse(404)
    if request.user not in [offer.buyer.user, offer.property.seller.user]:
        return HttpResponse(403)
    
    if action == "DELETE":
        try:
            offer.delete()
        except Exception:
            return HttpResponse(403)
    if action in ["ACCEPT", "REJECT"]:
        try:
            offer.offer_status = f"{action}ED" 
            notify(user=offer.buyer.user, offer=offer)
            offer.save()
        except Exception:
            return HttpResponse(500)
    if action == "CONTINGENT":
        try:
            offer.offer_status = "CONTINGENT"
            offer.offer_contingency_message = request.POST["message"]
            notify(user=offer.buyer.user, offer=offer)
            offer.save()
        except Exception:
            return HttpResponse(500)
    return HttpResponse(200)
    



@require_POST
@fetchNotifications
def createProperty(request):
    streetname = request.POST.get("streetname")
    city_input = request.POST.get("city_input")
    zip = request.POST.get("zip")
    desc = request.POST.get("desc")
    bedrooms = request.POST.get("bedrooms")
    bathrooms = request.POST.get("bathrooms")
    sqm = request.POST.get("sqm")
    type = request.POST.get("type")
    price = request.POST.get("price")
    images = request.POST.get("hidden-images-list")
        
    seller_obj = Seller.objects.get(user=request.user)
    newProperty = Property.objects.create(
        seller = seller_obj,
        street_name = streetname,
        city= city_input,
        postal_code = zip,
        description = desc,
        property_type = type,
        listing_price = price,
        number_of_bedrooms = bedrooms,
        number_of_bathrooms = bathrooms,
        square_meters = sqm,
        status = "Open",
        image = "ee",
        listing_date = datetime.date.today()
    )
    
    newProperty.image = createImages(images, newProperty, 0)
    newProperty.save()
    
    return redirect(f"/real-estates/{newProperty.id}")

def createImages(images, property, main=False):
    front = "/none"
    if not images:
        return front
    images = json.loads(images)

    for i, image in enumerate(images):
        newImage = BytesIO(base64.b64decode(str(image["url"]).split(",")[1]))
        fileName = default_storage.save(f"{image['desc']}.png", newImage)

        PropertyImages.objects.create(
            property = property,
            image_url = f"/media/{fileName}",
            image_description = image["desc"]
        )
        if i == main:
            front = f"/media/{fileName}"

    return front



@require_POST
@fetchNotifications
def selectPayment(request, offer_id):
    offer = Offer.objects.get(id=offer_id)
    
    payment_option = request.POST.get("payment_option")

    Payment.objects.create(
        offer = offer,
        payment_option = payment_option
    )
    return redirect('profile')

def filterListings(key: str, value: str, listings: list[Property]):
    filters = {"areaSelect": "postal_code",
               "typeSelect": "property_type",
               "priceInput": "listing_price",
               "descInput": "description"}
    if key in filters.keys():
        key = filters[key]

    if key == "postal_code":
        value = value.split()[0]
    if key == "description":
        temp = [x for x in listings if checkDesc(value, x)]
    elif key == "listing_price":
        values = value.split("-")
        if len(values) == 2:
            min, max = values
            if not min.isnumeric():
                min = 0
            if not max.isnumeric():
                max = 999999999999999
            temp = [x for x in listings if int(getattr(x, key)) >= int(min) and int(getattr(x, key)) <= int(max)]
        
    else:
        temp = [x for x in listings if getattr(x, key) == value]
    return temp


def checkDesc(search: str, listing: Property):
    words = search.split()
    for word in words:
        if word.lower() in listing.description.lower():
            return True
        if word.lower() in listing.street_name.lower():
            return True
    return False

def getSimilars(prop):
    listings = Property.objects.all()
    i = 10
    while len(listings) > 3 and i > 0:
        filtered = getSimilarListings(prop, i)
        listings = [x for x in listings if x in filtered]
        i -= 1

    return listings[:3]

def getSimilarListings(prop: Property, level: int):
    postalQ = Q(postal_code__gte=prop.postal_code-level, postal_code__lte=prop.postal_code+level)
    priceQ = Q(listing_price__gte=prop.listing_price-level*1000000, listing_price__lte=prop.listing_price+level*1000000)
    sqmQ = Q(square_meters__gte=prop.square_meters-level*3, square_meters__lte=prop.square_meters+level*3)

    listings = Property.objects.filter(~Q(id=prop.id), postalQ|priceQ|sqmQ)
    
    return listings

def getPrices():
    bigs = [75,85,95,105,115]
    nums = [x for x in range(25, 111) if x%5==0 and x not in bigs]
    nums.extend([125, 150, 175, 200, 250, 300])
    prices = {}
    for num in nums:
        prices[num] = {"visual": f"{num} mkr.", "value": str(num*1000000)}
    return prices

def notify(user, prop: Property = False, offer: Offer = False):
    try:
        kwargs = {"user": user, "property": prop, "offer": offer}
        kwargs = {k: v for k, v in kwargs.items() if v}
        notifUser = Notification.objects.get(**kwargs)
        notifUser.count += 1
        notifUser.save()
    except Exception:
        kwargs["count"] = 1
        notifUser = Notification.objects.create(**kwargs)
