from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import Seller

class RegistrationForm(UserCreationForm):
    ROLE_CHOICES =(('buyer','Buyer'),('seller','Seller'))

    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect) #svo annaðhvort sé valið

    class Meta : 
        model = User
        fields = ("username","full_name","image", "password1","password2","role")

class SellerForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields=("type","street_name","city","postal_code","logo","bio")