from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return HttpResponse("real_estate index")

def getRealEstateById(request, id):
    return HttpResponse(f"real_estate with id {id}")