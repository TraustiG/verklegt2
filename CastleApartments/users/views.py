from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from babel.numbers import format_currency
from .forms import RegistrationForm , SellerForm, SearchForm
from .models import Seller, Buyer, Filter, User
from real_estates.models import Offer,Property
from real_estates.views import index

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
                    print(seller_form.errors)
                    return render(request, 'users/register.html',{
                        'form':form,
                        'seller_form':seller_form
                    })
        
            login(request, user)
            return redirect(index)
    
        return render(request,'users/register.html', {
            'form': form,
            'seller_form': seller_form
        })

    else: 
        return render(request,'users/register.html',{
            'form': RegistrationForm(),
            'seller_form': SellerForm()
        })


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
        listings = Property.objects.filter(seller=seller)
        seller.bio = seller.bio.splitlines()


        return render(request, 'users/profile.html', {'profile': seller.user, 'listings': listings })

    elif user.is_buyer:
        buyer = Buyer.objects.get(user=user)
        offers = Offer.objects.filter(buyer=buyer)
        for offer in offers:
            offer.offer_amount = format_currency(offer.offer_amount, "", locale="is_is")[:-4]
            offer.property.listing_price = format_currency(offer.property.listing_price, "", locale="is_is")[:-4]

        return render(request, 'users/profile.html', {'profile': request.user, 'offers':offers })
        
def seller(request, id):
    # get seller user
    if request.user.id == id:
        return redirect('profile')
    seller = Seller.objects.get(user_id=id)
    seller.bio = seller.bio.splitlines()
    listings = Property.objects.filter(seller=seller)
    return render(request, 'users/profile.html', {'profile': seller.user, 'listings': listings})


def my_properties(request):


    seller = Seller.objects.get(user=request.user)
    properties = Property.objects.filter(seller=seller)
    for property in properties:
        property.raw_price = property.listing_price  #this is for edit property, cant have it on decimal format there
        property.listing_price = format_currency(property.listing_price, "", locale="is_is")[:-4]
    property_offers = {prop: [] for prop in properties}
    offers = Offer.objects.filter(property__seller = seller)

    for offer in offers:
        offer.offer_amount = format_currency(offer.offer_amount, "", locale="is_is")[:-4]
        for prop, list in property_offers.items():
            if offer.property == prop:
                list.append(offer)

    return render(request, 'users/my_properties.html', {"properties": property_offers, })

def property_offers(request, id):
    return render(request, 'users/seller_property_offers.html')