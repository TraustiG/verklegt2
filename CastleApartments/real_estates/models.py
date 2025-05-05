
from django.db import models


class Property(models.Model):
    
    title = models.CharField(max_length=100)
    street_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=5)
    description = models.TextField()
    property_type = models.CharField(max_length=100)
    listing_date = models.DateField()
    listing_price = models.CharField(max_length = 15)
    number_of_bedrooms = models.CharField(max_length=2)
    number_of_bathrooms = models.CharField(max_length=2)
    square_meters = models.CharField(max_length = 4)
    status = models.CharField(max_length = 100)
    image = models.URLField()

    def __str__(self):
        return f"{self.title}"
    

class Offer(models.Model):

    property = models.ForeignKey(
        "Property", on_delete=models.CASCADE)
    
    offer_amount = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.offer_amount}"
    
class PropertyImages(models.Model):

    property = models.ForeignKey(
        "Property", on_delete=models.CASCADE)
    
    image_url = models.URLField()
    
    def __str__(self):
        return f"{self.image_url}"

