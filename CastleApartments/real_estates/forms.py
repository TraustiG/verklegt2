from django import forms


class SearchForm(forms.Form):
    area = forms.CharField(label="areaSelect", max_length=100, required=False)
    re_type = forms.CharField(label="typeSelect", max_length=100, required=False)
    price = forms.CharField(label="priceInput", max_length=100, required=False)
    desc = forms.CharField(label="descInput", max_length=100, required=False)