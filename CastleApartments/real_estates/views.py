from django.http import HttpResponse
from django.shortcuts import render,redirect
from babel.numbers import format_currency
import copy
import json
from .models import Property, Offer, PropertyImages
from users.models import Buyer

""""
realEstate = {
    "type": "Fjölbýlishús",
    "address": "Maríugata 3, íbúð 203",
    "city": "Garðabær",
    "zip": 210,
    "sqm": 102,
    "baths": 1,
    "beds": 4,
    "images": [
                {"url": "https://api-beta.fasteignir.is/pictures/811668/547d88356c7c77b207c1d2dcc1d65460-large.jpg",
                "desc": "kitchen"},
                {"url": "https://api-beta.fasteignir.is/pictures/811668/2002e4756c85dffff2794a97acb2f9d7-large.jpg",
                "desc": "living room"},
                {"url": "https://api-beta.fasteignir.is/pictures/811668/753f7a8a0b267f767ba18a3aa369d88a-large.jpg",
                "desc": "bathroom"},
                {"url": "https://api-beta.fasteignir.is/pictures/811668/068aeaf912fa617d3539adec6674ed9e-large.jpg",
                "desc": "layout"},
        ]
    }

listing = {
    "id": 1,
    "date": "30.april 2025", 
    "desc": "Íbúð 203: 102 fm 4ra herbergja íbúð á 1. hæð með sér  þvottahúsi. Eigninni fylgir sérafnotareitur. Íbúðin er 93,4 fm ásamt 5,3 fm geymslu.  Innréttingar og skápir: Hvítt\n AFHENDING VIÐ KAUPSAMNING\n\n Stofa/alrými með útgengt út á svalir\n Eldhús: Raftæki eru frá AEG, bakaraofn og helluborð\n Svefnherbergi með fataskáp\n Baðherbergi með sturtu, hvítri innréttingu, handlaug, upphengdu salerni og handklæðaofn. Aðstaða fyrir þvottavél og þurrkara.\n Geymsla á fyrstu hæð\n\n Húsbyggjandi: Breiðahvarf ehf\n Aðalhönnuður: Úti inni arkitektar: Baldur Svavarsson\n Verkfræðihönnun: Víðsjá\n Raflagnahönnun: Lumex: Helgi Eiríksson", 
    "status": "Open", 
    "price": 96900000, 
}

seller = {
    "id": 1,
    "name": "Kalli Bjarni",
    "image": "",
}


item = {"real_estate": realEstate, "listing": listing, "seller": seller}
item["listing"]["price"] = 96900000
fakelist = [None]*60
for i in range(60):
    fakelist[i] = copy.deepcopy(item)
fakelist[2]["real_estate"]["city"] = "Akranes"
fakelist[2]["real_estate"]["address"] = "Bjarkargata 17"
fakelist[2]["real_estate"]["zip"] = 300
fakelist[8]["real_estate"]["type"] = "Einbýlishús"
fakelist[18]["real_estate"]["type"] = "Sundlaugagarður"
fakelist[32]["listing"]["price"] = 56000000
fakelist[4]["banner"] = "SELD"
fakelist[13]["banner"] = "SELD"

fakeUser = {
    "name": "Pétur Hermannsson",
    "is_authenticated": True,
    "id": 1,
    "photo": "https://media.istockphoto.com/id/1171169127/photo/headshot-of-cheerful-handsome-man-with-trendy-haircut-and-eyeglasses-isolated-on-gray.jpg?s=612x612&w=0&k=20&c=yqAKmCqnpP_T8M8I5VTKxecri1xutkXH7zfybnwVWPQ=",
    "username": "PesiiHann",
    "offers": [{
        "expiry": "01.01.2026",
        "offer_amount": 94000000,
        "status": "Open",
        "listing": listing}
    ]
}
"""

# Create your views here.
def index(request):
    if request.method == "GET":
        # þarf að fa listings og tegundir og postnumer í boði

        listings = Property.objects.all()
        areas = sorted(list(set([f"{x.postal_code} {x.city}" for x in listings])))
        types = sorted(list(set([f"{x.property_type}" for x in listings])))
        filters = []
        for item in listings:
            item.listing_price = format_currency(item.listing_price, "", locale="is_is")
        return render(request, "home.html", {"listings": listings, "areas": areas, "types": types, "filters": filters})

    """ areas = list(set([f"{x['real_estate']['zip']} {x['real_estate']['city']}" for x in fakelist]))
        types = list(set([f"{x['real_estate']['type']}" for x in fakelist]))
        listings = copy.deepcopy(fakelist)
        for item in listings:
            item["listing"]["price"] = format_currency(item["listing"]["price"], "", locale="is_is")[:-4]
        return render(request, "home.html", {"listings": listings, "areas": areas, "types": types})
    if request.method == "POST":
        # posta search form?? 
        return HttpResponse("real_estate index")
        """
def getRealEstateById(request, id):
    # get realestate from database - make object to send in render
    # get list of similar real estates - by zip, size, rooms... put in listings

    try:
        property_obj = Property.objects.get(id=id)
    except Property.DoesNotExist:
        return redirect('real-estates')
    similars = getSimilars(property_obj)
    images = PropertyImages.objects.filter(property=property_obj)
    seller = property_obj.seller

    return render(request, "real_estates/real_estate.html", { "property": property_obj, "images":images,"seller":seller })
    

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
                continue
            listings = filterListings(key, value, listings)

        for item in listings:
            item.listing_price = format_currency(item.listing_price, "", locale="is_is")

        return render(request, "home.html", {"listings": listings, "areas": areas, "types": types, "filters": filters})
      
#### Breyta object paths þegar model er komið ####
def filterListings(key: str, value: str, listings: list[Property]):
    filters = {"areaSelect": "postal_code",
               "typeSelect": "property_type",
               "priceInput": "listing_price",
               "descInput": "description"}
    if key in filters.keys():
        key = filters[key]

    if key == "postal_code":
        postalCode = value.split()[0]
        value = int(postalCode)
    if key == "description":
        temp = [x for x in listings if checkDesc(value, x)]
    elif key == "listing_price":
        values = value.split("-")
        if len(values) == 2:
            min, max = values
            temp = [x for x in listings if getattr(x, key) >= int(min) and getattr(x, key) <= int(max)]
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

def createOffer(request):

    if request.method == 'POST':
        property_id = request.POST.get('property_id')
        amount = request.POST.get('amount')
        expiry = request.POST.get('expiry')

        property_obj = Property.objects.get(id=property_id)
        buyer_obj = Buyer.objects.get(user=request.user)


        Offer.objects.create(
            property = property_obj,
            buyer = buyer_obj,
            offer_amount = amount,
            offer_expiry = expiry
        )
        
        return redirect('real-estate-by-id', id=property_id)
    
    return redirect('real-estates')