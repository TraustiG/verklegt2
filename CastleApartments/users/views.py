from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

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
}

fakeUser = {
    "name": "Pétur Hermannsson",
    "inits": "PH",
    "is_authenticated": True,
    "id": 1,
    "image": "https://media.istockphoto.com/id/1171169127/photo/headshot-of-cheerful-handsome-man-with-trendy-haircut-and-eyeglasses-isolated-on-gray.jpg?s=612x612&w=0&k=20&c=yqAKmCqnpP_T8M8I5VTKxecri1xutkXH7zfybnwVWPQ=",
    "username": "PesiiHann",
    "offers": [{
        "expiry": "01.01.2026",
        "offer_amount": 94000000,
        "status": "Accepted",
        "listing": listing},
        {"expiry": "01.01.2026",
        "offer_amount": 94000000,
        "status": "Open",
        "listing": listing}
    ]
}

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return render(request, 'users/register.html', {'form': form})
    else:
        return render(request, 'users/register.html', {'form': UserCreationForm()})

#@login_required
def profile(request, id):
    return render(request, 'users/profile.html', {'user': fakeUser})