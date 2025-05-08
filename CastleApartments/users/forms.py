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
    ROLE_CHOICES =(('individual','Individual'),('agency','Real estate agency'))
    type = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect) #svo annaðhvort sé valið
    class Meta:
        model = Seller
        fields=("type","street_name","city","postal_code","logo","bio")

class SearchForm(forms.Form):
    area = forms.CharField(label="areaSelect", max_length=100, required=False)
    re_type = forms.CharField(label="typeSelect", max_length=100, required=False)
    price = forms.CharField(label="priceInput", max_length=100, required=False)
    desc = forms.CharField(label="descInput", max_length=100, required=False)