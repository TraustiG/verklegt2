from django.http import HttpResponse
from django.shortcuts import render

realEstate = {
    "type": "Fjölbýlishús",
    "address": "Maríugata 3, íbúð 203",
    "city": "Garðabær",
    "zip": 210,
    "sqm": 102,
    "baths": 1,
    "beds": 4,
    }

listing = {
    "date": "30.april 2025", 
    "desc": """
            Íbúð 203: 102 fm 4ra herbergja íbúð á 1. hæð með sér  þvottahúsi. Eigninni fylgir sérafnotareitur. Íbúðin er 93,4 fm ásamt 5,3 fm geymslu. 
            Innréttingar og skápir: Hvítt\n
            AFHENDING VIÐ KAUPSAMNING\n\n
            Stofa/alrými með útgengt út á svalir\n
            Eldhús: Raftæki eru frá AEG, bakaraofn og helluborð\n
            Svefnherbergi með fataskáp\n
            Baðherbergi með sturtu, hvítri innréttingu, handlaug, upphengdu salerni og handklæðaofn. Aðstaða fyrir þvottavél og þurrkara.\n
            Geymsla á fyrstu hæð\n\n
            Húsbyggjandi: Breiðahvarf ehf\n
            Aðalhönnuður: Úti inni arkitektar: Baldur Svarvarsson\n
            Verkfræðihönnun: Víðsjá\n
            Raflagnahönnun: Lumex: Helgi Eiríksson
            """, 
    "status": "Open", 
    "price": 96900000, 
}

seller = {
    "id": 1,
    "name": "Kalli Bjarni",
    "image": "",
}

# Create your views here.
def index(request):
    if request.method == "GET":
        item = {"real_estate": realEstate, "listing": listing, "seller": seller}
        return render(request, "real_estates/listings.html", {"listings": [item, item]})
    return HttpResponse("real_estate index")

def getRealEstateById(request, id):
    # get realestate from database - make object to send in render
    if request.method == "GET":
        return render(request, "real_estates/real_estate.html", )