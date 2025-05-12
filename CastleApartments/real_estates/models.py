
from django.db import models

class PropertyImages(models.Model):

    property = models.ForeignKey(
        "Property", on_delete=models.CASCADE)
    
    image_url = models.TextField()
    image_description = models.TextField()

    
    def __str__(self):
        return f"{self.image_url}"


class PropertyStatus(models.TextChoices):
        OPEN = 'OPEN', 'Open'
        SOLD = 'SOLD', 'Sold'
        CONTINGENT = 'CONTINGENT', 'Contingent'
        PROCESSED = 'PROCESSED', 'Processed'

class Property(models.Model):
    class Meta:
        ordering = ('-listing_date', '-id')

    seller = models.ForeignKey(
        "users.Seller", on_delete=models.CASCADE, null=True, blank=True)
    
    street_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.IntegerField()
    description = models.TextField()
    property_type = models.CharField(max_length=100)
    listing_date = models.DateField()
    listing_price = models.IntegerField()
    number_of_bedrooms = models.IntegerField()
    number_of_bathrooms = models.IntegerField()
    square_meters = models.IntegerField()
    status = models.CharField(choices=PropertyStatus.choices, default=PropertyStatus.OPEN)
    image = models.TextField()

    def __str__(self):
        return f"{self.street_name}"
    

class OfferStatus(models.TextChoices):
        OPEN = 'OPEN', 'Open'
        REJECTED = 'REJECTED', 'Rejected'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        CONTINGENT = 'CONTINGENT', 'Contingent'
        PROCESSED = 'PROCESSED', 'Processed'

class Offer(models.Model):
    class Meta:
        ordering = ('-offer_date', '-id')

    property = models.ForeignKey(
        "Property", on_delete=models.CASCADE)
    buyer = models.ForeignKey(
        "users.Buyer", on_delete=models.SET_NULL, null=True, blank=True)
    
    offer_amount = models.CharField(max_length=20)
    offer_expiry = models.DateField()
    offer_date = models.DateField(auto_now_add=True)

    offer_status = models.CharField(choices=OfferStatus.choices, default=OfferStatus.OPEN,)
    offer_contingency_message = models.CharField(max_length = 100, blank=True)
    
    def __str__(self):
        return f"{self.offer_amount}"

