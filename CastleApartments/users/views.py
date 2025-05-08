from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from babel.numbers import format_currency
from .forms import RegistrationForm , SellerForm, SearchForm
from .models import Seller, Buyer, Filter
from real_estates.models import Offer,Property

listing = {
    "id": 1,
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

"""akeUser = {
    "name": "Pétur Hermannsson",
    "inits": "PH",
    "is_authenticated": True,
    "id": 1,
    "image": "https://media.istockphoto.com/id/1171169127/photo/headshot-of-cheerful-handsome-man-with-trendy-haircut-and-eyeglasses-isolated-on-gray.jpg?s=612x612&w=0&k=20&c=yqAKmCqnpP_T8M8I5VTKxecri1xutkXH7zfybnwVWPQ=",
    "username": "PesiiHann",
    "offers": [{
        "expiry": "01.01.2026", w
        "offer_amount": 94000000,
        "status": "Accepted",
        "listing": listing},
        {"expiry": "01.01.2026",
        "offer_amount": 94000000,
        "status": "Open",
        "listing": listing}
    ]
}"""

# Create your views here.


def register(request):

    if request.method == 'POST':
        role = request.POST.get('role')
        form = RegistrationForm(request.POST)
        
        seller_form = SellerForm(request.POST, request.FILES) if role == 'seller' else SellerForm()

        if form.is_valid():
            user = form.save(commit=False)
            
            if role == 'buyer':
                user.is_buyer = True
                user.save()
                Buyer.objects.create(user=user)

            elif role == 'seller':
                user.is_seller=True
                if seller_form.is_valid():
                    user.save()
                    seller = Seller(user=user)
                    seller.type=seller_form.cleaned_data['type']
                    seller.street_name=seller_form.cleaned_data['street_name']
                    seller.city=seller_form.cleaned_data['city']
                    seller.postal_code=seller_form.cleaned_data['postal_code']
                    seller.logo=seller_form.cleaned_data['logo']
                    seller.bio=seller_form.cleaned_data['bio']
                    seller.save()
                
                else:
                    return render(request, 'users/register.html',{
                        'form':form,
                        'seller_form':seller_form
                    })
        
            return redirect('login')
    
        return render(request,'users/register.html', {
            'form': form,
            'seller_form': seller_form
        })

    else: 
        return render(request,'users/register.html',{
            'form': RegistrationForm(),
            'seller_form': SellerForm()
        })
        
    # area = forms.CharField(label="areaSelect", max_length=100, required=False)
    # re_type = forms.CharField(label="typeSelect", max_length=100, required=False)
    # price = forms.CharField(label="priceInput", max_length=100, required=False)
    # desc = forms.CharField(label="descInput", max_length=100, required=False)


def saveFilter(request):
    if request.method == "POST":
        form = SearchForm()
        search = Filter()
        print(search.__dict__)
        search.area = form.area
        search.monitor = form.monitor
        search.name = form.name
        search.re_type = form.re_type
        search.desc = form.desc
        search.price = form.price
        search.user = request.user
        search.save()

    return redirect('search')


def profile(request):

    user = request.user

    if user.is_seller:
        seller = Seller.objects.get(user=user)
        properties = Property.objects.filter(seller=seller)
        bio_lines = seller.bio.splitlines()




        return render(request, 'users/profile.html', {'user': request.user, 'properties':properties, 'seller':seller, 'bio_lines':bio_lines})

    elif user.is_buyer:
        buyer = Buyer.objects.get(user=user)
        offers = Offer.objects.filter(buyer=buyer)
        for offer in offers:
            offer.offer_amount = format_currency(offer.offer_amount, "", locale="is_is")[:-4]
            offer.property.listing_price = format_currency(offer.property.listing_price, "", locale="is_is")[:-4]

        return render(request, 'users/profile.html', {'user': request.user, 'offers':offers, 'buyer':buyer})
        
def seller(request, id):
    # get seller user
    return render(request, 'users/profile.html', {'user': request.user, "seller_id": id})

def my_properties(request):
    seller = Seller.objects.get(user=request.user)
    properties = Property.objects.filter(seller=seller)
    return render(request, 'users/my_properties.html', {"properties": properties})