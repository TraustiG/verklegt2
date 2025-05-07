from django.http import HttpResponse
from django.shortcuts import render
from babel.numbers import format_currency
import copy
from .forms import SearchForm


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

# Create your views here.
def index(request):
    if request.method == "GET":
        # þarf að fa listings og tegundir og postnumer í boði
        areas = list(set([f"{x['real_estate']['zip']} {x['real_estate']['city']}" for x in fakelist]))
        types = list(set([f"{x['real_estate']['type']}" for x in fakelist]))
        listings = copy.deepcopy(fakelist)
        for item in listings:
            item["listing"]["price"] = format_currency(item["listing"]["price"], "", locale="is_is")[:-4]
        return render(request, "home.html", {"listings": listings, "areas": areas, "types": types})
    if request.method == "POST":
        # posta search form?? 
        return HttpResponse("real_estate index")

def getRealEstateById(request, id):
    # get realestate from database - make object to send in render
    # get list of similar real estates - by zip, size, rooms... put in listings
    listings = []
    item = copy.deepcopy({"real_estate": realEstate, "listing": listing, "seller": seller})
    item["listing"]["desc"] = item["listing"]["desc"].splitlines()
    item["listing"]["price"] = format_currency(item["listing"]["price"], "", locale="is_is")[:-4]
    if request.method == "GET":
        return render(request, "real_estates/real_estate.html", {"item": item, "listings": listings})

def imageGallery(request, id):
    # get realestate from database - make object to send in render
    if request.method == "GET":
        return render(request, "real_estates/gallery.html", {"images": realEstate['images']})

def search(request):
    if request.method == "GET":
        
        areas = list(set([f"{x['real_estate']['zip']} {x['real_estate']['city']}" for x in fakelist]))
        types = list(set([f"{x['real_estate']['type']}" for x in fakelist]))

        listings = copy.deepcopy(fakelist)
        for key in request.GET.keys():
            value = request.GET.get(key)
            print(key, value)
            if not value:
                continue
            listings = filterListings(key, value, listings)
        for item in listings:
            item["listing"]["price"] = format_currency(item["listing"]["price"], "", locale="is_is")[:-4]

        return render(request, "home.html", {"listings": listings, "areas": areas, "types": types})
    

#### Breyta object paths þegar model er komið ####
def filterListings(key, value, listings):
    filters = {"areaSelect": "zip",
               "typeSelect": "type",
               "priceInput": "price",
               "descInput": "desc"}
    if key in filters.keys():
        key = filters[key]

    if key == "zip":
        zip = value.split()[0]
        value = int(zip)
    if key == "desc":
        temp = [x for x in listings if checkDesc(value, x)]
    elif key == "price":
        values = value.split("-")
        if len(values) == 2:
            min, max = values
            temp = [x for x in listings if x["listing"][key] >= int(min) and x["listing"][key] <= int(max)]
    else:
        temp = [x for x in listings if x["real_estate"][key] == value]
    return temp


def checkDesc(search, listing):
    words = search.split()
    for word in words:
        if word.lower() in listing["listing"]["desc"].lower():
            return True
        if word.lower() in listing["real_estate"]["address"].lower():
            return True
    return False
