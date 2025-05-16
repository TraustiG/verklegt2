from django.http import HttpResponse
import requests
import random
import re
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
from .models import Property, Offer, PropertyImages, Extras
from users.models import Buyer, Seller, Notification, User, Filter
from typing import List

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

    popular = Property.objects.filter(~Q(status="SOLD"),~Q(status="PROCESSED")).order_by("-looked_at")[:8]
    newest = Property.objects.all().filter(~Q(status="SOLD"),~Q(status="PROCESSED"))[:8]

    listings = Property.objects.all()

    areas = sorted(list(set([f"{x.postal_code} {x.city}" for x in listings])))
    types = sorted(list(set([f"{x.property_type}" for x in listings])))
    
    prices = getPrices()
    filters = Filter.objects.filter(user_id=request.user.id)
    filter = filters.filter(monitor=True)
    filters = fixFilters(filters)

    for item in popular:
        item.listing_price = format_currency(item.listing_price, "", locale="is_is")[:-4]
        if not filter:
            continue
        if comparePropToFilter(item, filter[0]):
            item.monitor = True
    for item in newest:
        item.listing_price = format_currency(item.listing_price, "", locale="is_is")[:-4]
        if not filter:
            continue
        if comparePropToFilter(item, filter[0]):
            item.monitor = True
    return render(request, "home.html", {"newest": newest, "popular": popular, "areas": areas, "types": types, "prices": prices, "filters": filters})

def getPropertiesByWatch(request):
    try:
        filter = Filter.objects.get(user_id=request.user, monitor=True)
        postal = filter.area.split(" ")[0]
        type = filter.re_type
        desc = filter.desc
    except Exception:
        return redirect("search")
    try:
        min, max = filter.price.split("-")
    except Exception:
        min,  max = "", ""
    queries = []
    if postal:
        queries.append(Q(postal_code=postal))
    if type:
        queries.append(Q(property_type=type))
    if desc:
        queries.append(Q(description__icontains=desc))
    if min:
        queries.append(Q(listing_price__gt=min))
    if max:
        queries.append(Q(listing_price__lt=max))
    
    listings = Property.objects.all()
    areas = sorted(list(set([f"{x.postal_code} {x.city}" for x in listings])))
    types = sorted(list(set([f"{x.property_type}" for x in listings])))
    prices = getPrices()

    filters = Filter.objects.filter(user_id=request.user.id)
    filters = fixFilters(filters)

    listings = Property.objects.filter(*queries)
    for item in listings:
        item.listing_price = format_currency(item.listing_price, "", locale="is_is")[:-4]
    
    return render(request, "users/watch.html", {"listings": listings, "areas": areas, "types": types, "prices": prices, "filters": filters})



@require_http_methods(["GET", "POST"])
@fetchNotifications
def getRealEstateById(request, id: int):
    if request.method == "GET":
        try:
            propertyObj = Property.objects.get(id=id)
        except Property.DoesNotExist:
            return redirect('real-estates')
        similars = getSimilars(propertyObj)
        propertyObj.looked_at += 1
        propertyObj.save()
        images = PropertyImages.objects.filter(property=propertyObj)
        for prop in similars:
            prop.listing_price = format_currency(prop.listing_price, "", locale="is_is")[:-4]
        

        #making sure offer returns None for seller / unauthenticated users
        offer = None
        if request.user.is_authenticated:
            if request.user.is_buyer:
                offer = Offer.objects.filter(buyer=request.user.buyer, property=propertyObj).first()
                offer.expired = (offer.offer_expiry < datetime.date.today())
                request.user.has_offer = bool(offer)

        propertyObj.listing_price = format_currency(propertyObj.listing_price, "", locale="is_is")[:-4]
        propertyObj.description = propertyObj.description.splitlines()
        extras = Extras.objects.filter(property_id=propertyObj.id)
        propertyObj.extras = extras

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
            except Exception as e:
                print(e)
                return HttpResponse(403)
        else:
            try:
                propertyObj = Property.objects.get(id=id)
                
                extras = []
                for item in ["garage", "elevator", "wheelchair", "electric", "view"]:
                    extra = request.POST.get(item)
                    if extra:
                        extras.append(extra)
                old = Extras.objects.filter(property_id=propertyObj.id)
                old_descriptions = [x.description for x in old]

                for old_extra in old:
                    if old_extra.description not in extras:
                        old_extra.delete()


                for extra in extras:
                    if extra not in old_descriptions:
                        Extras.objects.create(property_id=propertyObj.id, description=extra)


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
                propertyObj.save()
            except Exception as e:
                print(e)
                return HttpResponse(500)
            
        return HttpResponse(status=200)

@require_safe
@fetchNotifications
def imageGallery(request, id: int):
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
    for key in request.GET.keys():
        value = request.GET.get(key)
        if not value:
            continue
        listings = filterListings(key, value, listings)

    filters = Filter.objects.filter(user_id=request.user.id)
    filters = fixFilters(filters)

    for item in listings:
        item.listing_price = format_currency(item.listing_price, "", locale="is_is")[:-4]


    return render(request, "real_estates/search.html", {"listings": listings, "areas": areas, "types": types, "prices": prices, "filters": filters})

@require_POST
@fetchNotifications
def createOffer(request, id: int):
    
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
def deleteOffer(request, id: int):
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
            if action == "ACCEPT":
                property = Property.objects.get(id=offer.property_id)
                property.status = "SOLD"
                property.save()
            offer.offer_status = f"{action}ED" 
            notify(user=offer.buyer.user, offer=offer)
            offer.save()
        except Exception:
            return HttpResponse(500)
    if action == "CONTINGENT":
        try:
            offer.offer_status = "CONTINGENT"
            offer.offer_contingency_message = request.POST["message"]
            offer.save()
            property = Property.objects.get(id=offer.property_id)
            property.status = "SOLD"
            property.save()
            notify(user=offer.buyer.user, offer=offer)
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
    
    for item in ["garage", "elevator", "wheelchair", "electric", "view"]:
        extra = request.POST.get(item)
        if extra:
            new = Extras.objects.create(property_id=newProperty.id, description=extra)
            new.save()

    filters = Filter.objects.filter(monitor=True)
    for filter in filters:
        if comparePropToFilter(newProperty, filter):
            notify(filter.user, prop=newProperty)

    return redirect(f"/real-estates/{newProperty.id}")

def comparePropToFilter(property: Property, filter: Filter):
    area = f"{property.postal_code} {property.city}"
    if filter.area not in ["", area]:
        return False
    if filter.re_type not in ["", property.property_type]:
        return False
    if filter.desc not in ["", property.description]:
        return False
    if filter.price:
        min, max = filter.price.split("-")
        try:
            if int(min) > property.listing_price:
                return False
        except Exception:
            pass
        try:
            if int(max) < property.listing_price:
                return False
        except Exception:
            pass
    return True

def createImages(images: List[str], property: Property, main: bool=False):
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



def filterListings(key: str, value: str, listings: list[Property]):
    filters = {"areaSelect": "postal_code",
               "typeSelect": "property_type",
               "priceInput": "listing_price",
               "descInput": "description"}
    if key in filters.keys():
        key = filters[key]

    if key == "postal_code":
        value = int(value.split()[0])
    if key == "description":
        temp = [x for x in listings if checkDesc(value, x)]
    elif key == "listing_price":
        values = value.split("-")
        if len(values) == 2:
            min, max = values
            if not min.isnumeric():
                min = 0
            if not max.isnumeric():
                max = 9999999999999999999
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

def getSimilars(prop: Property):
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

def fixFilters(filters: List[Filter]):
    for filter in filters:
        try:
            min, max = filter.price.split("-")
            try: 
                min = int(min)//1000000
                min = f"{str(min)}"
            except Exception:
                min = f"0-"
            try: 
                max = str(int(max)//1000000)
            except Exception:
                max = "+"
            if min != "0-":
                if max != "+":
                    filter.price = f"{min} mkr. - {max} mkr."
                else:
                    filter.price = f"{min} mkr. +"
            else:
                filter.price = f"0-{max} mkr."
        except Exception:
            pass
    return filters

def tester(request):
    offer = Offer.objects.get(id=79)
    offer.offer_expiry = datetime.date(2025,5,12)
    offer.save()
        
    return redirect('profile')


def databaseFiller(request):
    properties = Property.objects.filter(id__gt=58)
    for property in properties:
        url = property.image.split("/")[2]
        property.image = f"/media/visir/{url}"
        property.save()

    users = [ 
        {"address": "Húnavatn 42", "type": "Individual", "city": "Ísafjörður", "postal_code": "400", "bio": "Ég vill leiða þig heim.", "username": "jonjons", "is_seller": True, "is_buyer": False, "image": "/media/jonjons.jpg", "full_name": "Jón Jónsson", "logo": "/media/jonjonslogo.jpg", "password": "pbkdf2_sha256$1000000$LMIDRhZNh70LlXa5BEIT2B$KHJphkLgtw8i69XVMDlySa8lR8/Amd+22DtKyIgzv0Q=" },
        {"address": "Blábrigði 67", "type": "Individual", "city": "Akureyri", "postal_code": "600", "bio": "Rauður blómajakki getur ekki stöðvað mig\ní að veita þér draumaheimilið þitt.", "username": "kallibjarni", "is_seller": True, "is_buyer": False, "image": "/media/kallibjarni.png", "full_name": "Kalli Bjarni", "logo": "/media/bjarniklogo.png", "password": "pbkdf2_sha256$1000000$LMIDRhZNh70LlXa5BEIT2B$KHJphkLgtw8i69XVMDlySa8lR8/Amd+22DtKyIgzv0Q="},
        {"address": "Asparskógar 104", "type": "Individual", "city": "Reykjavík", "postal_code": "101", "bio": "Þitt draumaheimilið þér veita að í\nMig stöðvað ekki getur blómajakki rauður.", "username": "bjarnikalli", "is_seller": True, "is_buyer": False, "image": "/media/bjarnikalli.png", "full_name": "Bjarni Kalli", "logo": "/media/bjarniklogo.png", "password": "pbkdf2_sha256$1000000$LMIDRhZNh70LlXa5BEIT2B$KHJphkLgtw8i69XVMDlySa8lR8/Amd+22DtKyIgzv0Q="},
        {"address": "Vallarbraut 49", "type": "Individual", "city": "Ísafjörður", "postal_code": "400", "bio": "Saman stöndum vér allir.", "username": "jonsi", "is_seller": True, "is_buyer": False, "image": "/media/jonsi.avif", "full_name": "Jón Sigurðsson", "logo": "/media/Althing_Logo.png", "password": "pbkdf2_sha256$1000000$LMIDRhZNh70LlXa5BEIT2B$KHJphkLgtw8i69XVMDlySa8lR8/Amd+22DtKyIgzv0Q=" },
        {"address": "Húnaflói 1", "type": "Individual", "city": "Reykjavík", "postal_code": "101", "bio": "Gætum við staðið, hlið við hlið.\nHeima hjá þér\nMögulega að borða smákökur.", "username": "fridrikdor", "is_seller": True, "is_buyer": False, "image": "/media/fridrikdor.jpg", "full_name": "Friðrik Dór Jónsson", "logo": "/media/realtor1.jpg" , "password": "pbkdf2_sha256$1000000$LMIDRhZNh70LlXa5BEIT2B$KHJphkLgtw8i69XVMDlySa8lR8/Amd+22DtKyIgzv0Q=" },
        {"address": "Vatnagata 14", "type": "Real estate agency", "city": "Ísafjörður", "postal_code": "300", "bio": "Bleikt hár í Bónus, hvað er ekki að elska?", "username": "brothers", "is_seller": True, "is_buyer": False, "image": "/media/brothers.jpg", "full_name": "Bræðraveldi", "logo": "/media/realtor2.jpeg" , "password": "pbkdf2_sha256$1000000$LMIDRhZNh70LlXa5BEIT2B$KHJphkLgtw8i69XVMDlySa8lR8/Amd+22DtKyIgzv0Q=" },
        {"address": "Breiðaflöt 9", "type": "Individual", "city": "Reykjavík", "postal_code": "101", "bio": "Help me help you, fly to the moon.", "username": "aroncan", "is_seller": True, "is_buyer": False, "image": "/media/aroncan.jpg", "full_name": "Aron Can", "logo": "/media/iceguysice.png" , "password": "pbkdf2_sha256$1000000$LMIDRhZNh70LlXa5BEIT2B$KHJphkLgtw8i69XVMDlySa8lR8/Amd+22DtKyIgzv0Q=" },
        {"address": "Akragata 64", "type": "Individual", "city": "Akureyri", "postal_code": "600", "bio": "Það er alltaf hægt að ná í mig í smíðakofanum.", "username": "emil", "is_seller": True, "is_buyer": False, "image": "/media/emil.png", "full_name": "Emil Can", "logo": "/media/realtor4.png" , "password": "pbkdf2_sha256$1000000$LMIDRhZNh70LlXa5BEIT2B$KHJphkLgtw8i69XVMDlySa8lR8/Amd+22DtKyIgzv0Q=" },
        {"address": "Korpustaðir", "type": "Real estate agency", "city": "Akranes", "postal_code": "300", "bio": "Eru ekki allir SEXÝ??", "username": "helgibjorns", "is_seller": True, "is_buyer": False, "image": "/media/helgibjorns.jpg", "full_name": "Reiðmenn vindanna", "logo": "/media/hbrm.jpg" , "password": "pbkdf2_sha256$1000000$LMIDRhZNh70LlXa5BEIT2B$KHJphkLgtw8i69XVMDlySa8lR8/Amd+22DtKyIgzv0Q=" },
        {"address": "Grettisganga 22", "type": "Individual", "city": "Ísafjörður", "postal_code": "400", "bio": "Hvenær byrjaðir þú að selja fasteignir heyri ég þig spyrja.", "username": "laddi", "is_seller": True, "is_buyer": False, "image": "/media/laddi.png", "full_name": "Og Halli", "logo": "/media/ogladdi.jpg" , "password": "pbkdf2_sha256$1000000$LMIDRhZNh70LlXa5BEIT2B$KHJphkLgtw8i69XVMDlySa8lR8/Amd+22DtKyIgzv0Q=" },
         ]
    newSellers = []
    try:
        for user in users:
            logo = user.pop("logo")
            type = user.pop("type")
            city = user.pop("city")
            postal_code = user.pop("postal_code")
            address = user.pop("address")
            bio = user.pop("bio")
            newUser = User(**user)
            seller = Seller(user=newUser, logo=logo, type=type, city=city, postal_code=postal_code, bio=bio, street_name=address)
            newUser.save()
            seller.save()
            newSellers.append(seller)
    except Exception:
        pass
    visir = requests.get("https://fasteignir.visir.is/api/search?onpage=300&page=1").json()
    i = 0
    addresses = []
    for prop in visir:
        if prop["category"] not in ["Fjölbýlishús", "Einbýlishús", "Parhús", "Raðhús"]:
            continue
        address = (prop["zip"]["zip"], prop["street_name"], prop["street_number"])
        if address in addresses:
            continue
        if i == 150:
            break
        images = requests.get(f"https://fasteignir.visir.is/property/{prop['id']}/imagelist")
        htmlText = images.text
        matches = re.findall(r"<img src=\"https://api-beta.fasteignir.is/pictures/\d*/(.*)?\" title", htmlText)
        if not matches:
            continue
        if i%50 == 0:
            print(i)
        i += 1
        newProp = {}
        try:
            addresses.append(address)
            newProp["seller"] = newSellers[random.randint(0,len(newSellers)-1)]
            newProp["street_name"] = f"{prop['street_name']} {prop['street_number']}"
            newProp["city"] = prop["zip"]["town"]
            newProp["postal_code"] = prop["zip"]["zip"]
            newProp["description"] = "edit"
            newProp["property_type"] = prop["category"]
            newProp["listing_date"] = datetime.date.today() - datetime.timedelta(random.randint(0,20))
            newProp["listing_price"] = prop["price"]
            newProp["number_of_bedrooms"] = prop["bedrooms"]
            newProp["number_of_bathrooms"] = prop["bathrooms"]
            newProp["square_meters"] = int(prop["size"].replace(",",".").split(".")[0])
            newProp["status"] = "OPEN"
            newProp["image"] = prop["image"]
        except Exception as e:
            print(e)
            continue
        propertyObj = Property(**newProp)
        for i in range(min(len(matches),6)):
            try:
                match = matches[i]
                if i == 0:
                    propertyObj.image = f"/media/visir/{match}"
                    propertyObj.save()
                url = f"https://api-beta.fasteignir.is/pictures/{prop['id']}/{match}"
                imageText = requests.get(url)
                with open(f"D:\\forritun\HR Tölvunarfræði\\verklegt2\\CastleApartments\\media\\visir\\{match}", "wb") as file:
                    file.write(imageText.content)
                image = {"property": propertyObj, "image_url": f"/media/visir/{match}", "image_description": ""}
                newImage = PropertyImages(**image)
                newImage.save()
            except Exception as e:
                print(e)
                pass
    return redirect("profile")
        



