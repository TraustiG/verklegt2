from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.core.files.storage import default_storage
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.views.decorators.http import require_http_methods, require_safe, require_POST
from babel.numbers import format_currency
from io import BytesIO
import base64
import json
import datetime
from .models import Property, Offer, PropertyImages, Payment
from users.models import Buyer, Seller, Notification

# Create your views here.

def fetchNotifications(view_func):
    def _decorated(request, *args, **kwargs):
        try:
            notifs = Notification.objects.filter(user=request.user, count__gt=0)
            request.user.notifications = notifs
            return view_func(request, *args, **kwargs)
        except Exception:
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

@require_safe
@fetchNotifications
def getRealEstateById(request, id):

    try:
        property_obj = Property.objects.get(id=id)
    except Property.DoesNotExist:
        return redirect('real-estates')
    similars = getSimilars(property_obj)
    images = PropertyImages.objects.filter(property=property_obj)
    for prop in similars:
        prop.listing_price = format_currency(prop.listing_price, "", locale="is_is")[:-4]
    
    if request.user.is_buyer:
        offer = Offer.objects.filter(buyer=request.user.buyer, property=property_obj)
        request.user.has_offer = bool(offer)
        print(request.user.has_offer)

    property_obj.listing_price = format_currency(property_obj.listing_price, "", locale="is_is")[:-4]
    property_obj.description = property_obj.description.splitlines()

    return render(request, "real_estates/real_estate.html", { "property": property_obj, "images":images, "listings": similars})
    

@require_safe
@fetchNotifications
def imageGallery(request, id):
    # get realestate from database - make object to send in render
    try:
        property_obj = Property.objects.get(id=id)
    except Property.DoesNotExist:
        return redirect('real-estates')
    
    images = PropertyImages.objects.filter(property=property_obj)
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

    property_obj = Property.objects.get(id=id)
    buyer_obj = Buyer.objects.get(user=request.user)


    Offer.objects.create(
        property = property_obj,
        buyer = buyer_obj,
        offer_amount = amount,
        offer_expiry = expiry,
        offer_date = datetime.date.today()
    )
    notify(user=property_obj.seller.user, prop=property_obj)
    
    return redirect('real-estate-by-id', id=id)



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
    if not images:
        images = "{}"
    images = json.loads(images)
        
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

    for i, image in enumerate(images):
        newImage = BytesIO(base64.b64decode(str(image["url"]).split(",")[1]))

        fileName = default_storage.save(f"{image['desc']}.png", newImage)
        PropertyImages.objects.create(
            property = newProperty,
            image_url = f"/media/{fileName}",
            image_description = image["desc"]
        )

        if i == 0:
            newProperty.image = f"/media/{fileName}"
            newProperty.save()

    
    return redirect(f"real-estates/{newProperty.id}")


@fetchNotifications
def editProperty(request, id):
    if request.method == "POST":
        property_obj = Property.objects.get(id=id)
        
        property_obj.street_name = request.POST.get("streetname")
        property_obj.city = request.POST.get("city_input")
        property_obj.postal_code = request.POST.get("zip")
        property_obj.description = request.POST.get("desc")
        property_obj.number_of_bedrooms = request.POST.get("bedrooms")
        property_obj.number_of_bathrooms = request.POST.get("bathrooms")
        property_obj.square_meters = request.POST.get("sqm")
        property_obj.image = request.POST.get("imageURL")
        property_obj.property_type = request.POST.get("type")
        property_obj.listing_price = request.POST.get("price")
        property_obj.save()

        return redirect('my-properties')

@fetchNotifications
def deleteProperty(request, id): 

    property_obj = Property.objects.get(id=id)
    property_obj.delete()

    return redirect('my-properties')


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
    listings = Property.objects.filter(~Q(id=prop.id))

    i = 10
    while len(listings) > 3 and i > 0:
        filtered = getSimilarListings(listings, prop, i)
        listings = [x for x in listings if x in filtered]
        i -= 1

    return listings[:3]

def getSimilarListings(listings, prop: Property, level: int):

    listings = listings.filter(postal_code__gte=prop.postal_code-level, postal_code__lte=prop.postal_code+level)
    if len(listings)<=3: return listings

    listings = listings.filter(listing_price__gte=prop.listing_price-level*1000000, listing_price__lte=prop.listing_price+level*1000000)
    if len(listings)<=3: return listings

    listings = listings.filter(square_meters__gte=prop.square_meters-level*3, square_meters__lte=prop.square_meters+level*3)
    return listings

def getPrices():
    bigs = [75,85,95,105,115]
    nums = [x for x in range(25, 111) if x%5==0 and x not in bigs]
    nums.extend([125, 150, 175, 200, 250, 300])
    prices = {}
    for num in nums:
        prices[num] = {"visual": f"{num} mkr.", "value": str(num*1000000)}
    return prices

def createProperty(request):

    if request.method == 'POST':
        
        streetname = request.POST.get("streetname")
        city_input = request.POST.get("city_input")
        zip = request.POST.get("zip")
        desc = request.POST.get("desc")
        bedrooms = request.POST.get("bedrooms")
        bathrooms = request.POST.get("bathrooms")
        sqm = request.POST.get("sqm")
        status_input = request.POST.get("status_input")
        imageURL = request.POST.get("imageURL")
        type = request.POST.get("type")
        price = request.POST.get("price")


        seller_obj = Seller.objects.get(user=request.user)
        


        Property.objects.create(
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
            status = status_input,
            image = imageURL,
            listing_date = datetime.date.today()

            
        )
        
        return redirect('my-properties')
    
    return redirect('my-properties')

def payment(request, offer_id):
    if request.method == 'POST':
        offer = Offer.objects.get(id=offer_id)
        
        payment_option = request.POST.get("payment_option")

        Payment.objects.create(
            offer = offer,
            payment_option = payment_option
        )
        return redirect('profile')
    return redirect('profile')

def notify(user, prop: Property = False, offer: Offer = False):
    try:
        kwargs = {"user": user, "property": prop, "offer": offer}
        kwargs = {k: v for k, v in kwargs.items() if v}
        notifUser = Notification.objects.get(**kwargs)
        notifUser.count += 1
        notifUser.save()
    except Exception:
        kwargs["count"] = 1
        Notification.objects.create(**kwargs)
