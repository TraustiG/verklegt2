from django.http import HttpResponse
from django.shortcuts import render,redirect
from babel.numbers import format_currency
import copy
import json
import datetime
from .models import Property, Offer, PropertyImages, Payment
from users.models import Buyer, Seller

# Create your views here.
def index(request):
    if request.method == "GET":
        # þarf að fa listings og tegundir og postnumer í boði

        listings = Property.objects.all()
        areas = sorted(list(set([f"{x.postal_code} {x.city}" for x in listings])))
        types = sorted(list(set([f"{x.property_type}" for x in listings])))
        filters = []
        for item in listings:
            item.listing_price = format_currency(item.listing_price, "", locale="is_is")[:-4]
        return render(request, "home.html", {"listings": listings, "areas": areas, "types": types, "filters": filters})

def getRealEstateById(request, id):
    # get realestate from database - make object to send in render
    # get list of similar real estates - by zip, size, rooms... put in listings

    try:
        property_obj = Property.objects.get(id=id)
    except Property.DoesNotExist:
        return redirect('real-estates')
    similars = getSimilars(property_obj)
    images = PropertyImages.objects.filter(property=property_obj)
    listings = Property.objects.all()

    property_obj.listing_price = format_currency(property_obj.listing_price, "", locale="is_is")[:-4]
    property_obj.description = property_obj.description.splitlines()

    return render(request, "real_estates/real_estate.html", { "property": property_obj, "images":images, "seller": property_obj.seller, "listings": listings})
    

def imageGallery(request, id):
    # get realestate from database - make object to send in render
    try:
        property_obj = Property.objects.get(id=id)
    except Property.DoesNotExist:
        return redirect('real-estates')
    
    images = PropertyImages.objects.filter(property=property_obj)
    if request.method == "GET":
        return render(request, "real_estates/gallery.html", {"images": images})
    
def search(request):
    if request.method == "GET":
        
        listings = Property.objects.all()
        areas = sorted(list(set([f"{x.postal_code} {x.city}" for x in listings])))
        types = sorted(list(set([f"{x.property_type}" for x in listings])))
        filter = {"areaSelect": 300,
                "typeSelect": "Fjölbýlishús",
                "priceInput": "80000000-110000000",
                "descInput": "bjark"}
        filters = [{"name": "Bjarkissssssss", "filters": json.dumps(filter)}]

        for key in request.GET.keys():
            value = request.GET.get(key)
            if not value:
                print(key)
                continue
            listings = filterListings(key, value, listings)

        for item in listings:
            item.listing_price = format_currency(item.listing_price, "", locale="is_is")[:-4]

        return render(request, "home.html", {"listings": listings, "areas": areas, "types": types, "filters": filters})
      
#### Breyta object paths þegar model er komið ####
def filterListings(key: str, value: str, listings: list[Property]):
    filters = {"areaSelect": "postal_code",
               "typeSelect": "property_type",
               "priceInput": "listing_price",
               "descInput": "description"}
    if key in filters.keys():
        key = filters[key]

    print(key, value, )
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
    ...

def createOffer(request, id):

    if request.method == 'POST':
        
        amount = request.POST.get("amount")
        expiry = request.POST.get("expiry")

        property_obj = Property.objects.get(id=id)
        buyer_obj = Buyer.objects.get(user=request.user)


        Offer.objects.create(
            property = property_obj,
            buyer = buyer_obj,
            offer_amount = amount,
            offer_expiry = expiry
        )
        
        return redirect('real-estate-by-id', id=id)
    
    return redirect('real-estates')


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
        images = request.POST.get("images").replace(" ","").split(",")


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
            image = imageURL,
            listing_date = datetime.date.today()
        )

        PropertyImages.objects.create(
            property = newProperty,
            image_url = imageURL,
            image_description = "main"
        )

        for image in images:
            try:
                PropertyImages.objects.create(
                    property = newProperty,
                    image_url = image,
                    image_description = ""
                )
            except Exception:
                continue

        
        return redirect(f"real-estates/{newProperty.id}")
    
    return redirect('my-properties')

def selectPayment(request, offer_id):
    if request.method == 'POST':
        offer = Offer.objects.get(id=offer_id)
        
        payment_option = request.POST.get("payment_option")

        Payment.objects.create(
            offer = offer,
            payment_option = payment_option
        )
        return redirect('profile')
    return redirect('profile')