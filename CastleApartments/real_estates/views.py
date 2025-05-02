from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return HttpResponse("real_estate index")

def getRealEstateById(request, id):
    # get realestate from database - make object to send in render
    if request.method == "GET":
        # return HttpResponse("test")
        return render(request, "real_estates/real_estate.html", {"id": id})