from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth import login
from django.views.decorators.http import require_http_methods, require_safe, require_POST
from babel.numbers import format_currency
import copy
from .forms import RegistrationForm , SellerForm, SearchForm
from .models import Seller, Buyer, Filter, User, Notification
from real_estates.models import Offer,Property
from real_estates.views import index, fetchNotifications

# Create your views here.

@require_http_methods(["GET", "POST"])
@fetchNotifications
def register(request):

    # illegal = User.objects.filter(full_name="Jón Jónsson")
    # for user in illegal:
    #     user.delete()

    if request.method == 'POST':
        role = request.POST.get('role')
        print(request.POST.get("role"))
        form = RegistrationForm(request.POST, request.FILES)
        seller_form = SellerForm(request.POST, request.FILES) if role == 'seller' else SellerForm()

        if form.is_valid():
            user = form.save(commit=False)
            user.image = form.cleaned_data['image']
            user.save()  

           
            user.image = f"/media/{user.image}"
            user.save()  

            
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
                    seller.logo = seller_form.cleaned_data['logo']
                    print(seller.logo)
                    seller.bio=seller_form.cleaned_data['bio']
                    seller.save()
                    seller.logo = f"/media/{seller.logo}"
                    seller.save()
                
                else:
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


@require_POST
@fetchNotifications
def saveFilter(request):
    if request.method == "POST":
        search = Filter()
        search.area = request.POST["area"]
        search.monitor = request.POST["monitor"]
        search.name = request.POST["name"]
        search.re_type = request.POST["re_type"]
        search.desc = request.POST["desc"]
        search.price = request.POST["price"]
        print(search)
        search.user = request.user
        search.save()

    return redirect('search')


@require_http_methods(["GET", "POST"])
@fetchNotifications
def profile(request):

    if request.method == "GET":
        user = request.user
        if user.is_seller:
            seller = Seller.objects.get(user=user)

            listings = Property.objects.filter(seller=seller)
            for prop in listings:
                prop.listing_price = format_currency(prop.listing_price, "", locale="is_is")[:-4]

            seller.bio = seller.bio.splitlines()

            return render(request, 'users/profile.html', {'profile': seller.user, 'listings': listings })
        elif user.is_buyer:
            load = {}
            buyer = Buyer.objects.get(user=user)
            offers = Offer.objects.filter(buyer=buyer)
            for offer in offers:
                offer.offer_amount = format_currency(offer.offer_amount, "", locale="is_is")[:-4]
                offer.property.listing_price = format_currency(offer.property.listing_price, "", locale="is_is")[:-4]
                notifs = Notification.objects.filter(user=request.user, offer=offer, count__gt=0)
                load[offer] = len(notifs)

                for notif in notifs:
                    notif.count = 0
                    notif.save()

            return render(request, 'users/profile.html', {'profile': request.user, 'offers': offers })
    
    if request.method == "POST":
    
        user = request.user
            
        #allow changes for fullname / image as they are shared , save user
        fullname = request.POST.get("fullname")
        print(request.FILES.keys())
        print(dir(request.FILES))
        profile_image = request.FILES.get("profile_image")

        user.full_name = fullname
        user.image = profile_image

        #saves the picture to media folder
        user.save() 

        
        user.image = f"/media/{user.image}"

        #saves correct path for user.image
        user.save()
            
        #check if user is a seller & edit / save seller object if those fields have been edited
        if user.is_seller:
            seller = Seller.objects.get(user=user)

            seller_type = request.POST.get("seller_type")
            streetname = request.POST.get("streetname")
            city_input = request.POST.get("city_input")
            zip = request.POST.get("zip")
            logo_input = request.FILES.get("logo_input")
            bio_input = request.POST.get("bio_input")

            seller.type= seller_type
            seller.street_name= streetname
            seller.city= city_input
            seller.postal_code= zip
            seller.logo= logo_input
            seller.bio= bio_input

            
            seller.save()

            #save correct path to logo field
            seller.logo= f"/media/{seller.logo}"

            seller.save()
        
        return redirect('profile')
        
@require_safe
@fetchNotifications
def seller(request, id):
    
    if request.user.id == id:
        return redirect('profile')

    seller = Seller.objects.get(user_id=id)
    seller.bio = seller.bio.splitlines()

    listings = Property.objects.filter(seller=seller)
    for prop in listings:
        prop.listing_price = format_currency(prop.listing_price, "", locale="is_is")[:-4]

    return render(request, 'users/profile.html', {'profile': seller.user, 'listings': listings})


@require_http_methods(["GET", "POST"])
@fetchNotifications
def my_properties(request):

    seller = Seller.objects.get(user=request.user)
    properties = Property.objects.filter(seller=seller)
    property_offers = {}
    for property in properties:
        property.raw_price = property.listing_price  #this is for edit property, cant have it on decimal format there
        property.listing_price = format_currency(property.listing_price, "", locale="is_is")[:-4]
        property_offers[property] = {"notifs": 0, "offers": []}

    for prop, list in property_offers.items():
        offers = Offer.objects.filter(property=prop)
        notifs = Notification.objects.filter(user=request.user, property=prop, count__gt=0)
        property_offers[prop]["notifs"] = sum([x.count for x in notifs])
        for notif in notifs:
            notif.count = 0
            notif.save()
        for offer in offers:
            if offer.offer_status == "PROCESSED":
                list["offers"] = [offer]
                break
            offer.offer_amount = format_currency(offer.offer_amount, "", locale="is_is")[:-4]
            list["offers"].append(offer)


    return render(request, 'users/my_properties.html', {"properties": property_offers, })

@require_safe
@fetchNotifications
def property_offers(request):
    return render(request, 'users/seller_property_offers.html')